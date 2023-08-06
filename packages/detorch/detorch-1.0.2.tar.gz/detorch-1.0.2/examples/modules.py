from typing import Callable, List, Optional
from itertools import tee
from functools import lru_cache

from detorch import Policy

import torch
import torch.nn.functional as F
from torch import nn
import numpy as np


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


@lru_cache(maxsize=1)
def make_env(env_id):
    import gym
    return gym.make(env_id)


@lru_cache(maxsize=1)
def get_loaders(data_path='.'):
    from torchvision import datasets, transforms
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    dataset1 = datasets.MNIST(data_path, train=True, download=True,
                       transform=transform)
    dataset2 = datasets.MNIST(data_path, train=False,
                       transform=transform)
    train_loader = torch.utils.data.DataLoader(dataset1, batch_size=64)
    test_loader = torch.utils.data.DataLoader(dataset2, batch_size=128)
    return train_loader, test_loader


class GymAgent(Policy):
    def __init__(self, env_id: str, hidden_layers: List[int],
                 hidden_act: Optional[nn.Module] = None,
                 output_act: Optional[nn.Module] = None,
                 bias: bool = True, n_rollout: int = 1,
                 seed: Optional[int] = None):
        super().__init__()
        import gym

        self.n_rollout = n_rollout
        self.env: gym.Env = make_env(env_id)
        self.env.seed(seed)
        self.env.action_space.seed(seed)
        self.output_func: Callable[[int], int]
        output_size: int
        input_size: int = self.env.observation_space.shape[0]

        if isinstance(self.env.action_space, gym.spaces.Discrete):
            output_size: int = self.env.action_space.n
            self.output_func = lambda x: x.argmax().item()
        else:
            output_size: int = self.env.action_space.shape[0]
            self.output_func = lambda x: x.detach().numpy()

        layers: List[nn.Module] = []
        layer_sizes = [input_size] + hidden_layers + [output_size]
        for idx, (layer1, layer2) in enumerate(pairwise(layer_sizes)):
            layers.append(nn.Linear(layer1, layer2, bias=bias))
            if hidden_act is not None:
                if idx < len(layer_sizes) - 2:
                    layers.append(hidden_act())
        if output_act is not None:
            layers.append(output_act())
        self.seq = nn.Sequential(*layers)

    def evaluate(self):
        total_reward = 0
        for _ in range(self.n_rollout):
            done = False
            obs = self.env.reset()
            while not done:
                obs_tensor = torch.from_numpy(obs).float()
                action = self.seq(obs_tensor).argmax().item()
                obs, reward, done, _ = self.env.step(action)
                total_reward += reward
        return total_reward / self.n_rollout


class MNISTAgent(Policy):
    def __init__(self, batch_size=32, reward_type='loss', data_path='.'):
        super(MNISTAgent, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
        self.train_loader, self.test_loader = get_loaders(data_path)
        self.reward_type = reward_type

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

    def evaluate(self):
        data, target = next(iter(self.train_loader))
        output = self.forward(data)
        if self.reward_type == 'loss':
            loss = F.nll_loss(output, target)
            return -loss.item()
        elif self.reward_type == 'accuracy':
            pred = output.argmax(dim=1, keepdim=True)
            accuracy = pred.eq(target.view_as(pred)).sum().item()
            return accuracy / len(target)
        else:
            raise NotImplementedError
