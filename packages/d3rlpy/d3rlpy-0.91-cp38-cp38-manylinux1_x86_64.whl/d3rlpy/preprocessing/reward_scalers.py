from typing import Any, ClassVar, Dict, List, Optional, Type

import gym
import numpy as np
import torch

from ..dataset import Episode, MDPDataset
from ..decorators import pretty_repr
from ..logger import LOG


@pretty_repr
class RewardScaler:

    TYPE: ClassVar[str] = "none"

    def fit(self, episodes: List[Episode]) -> None:
        """Estimates scaling parameters from dataset.

        Args:
            episodes: list of episodes.

        """
        raise NotImplementedError

    def fit_with_env(self, env: gym.Env) -> None:
        """Gets scaling parameters from environment.

        Note:
            ``RewardScaler`` does not support fitting with environment.

        Args:
            env: gym environment.

        """
        raise NotImplementedError("Please initialize with dataset.")

    def transform(self, reward: torch.Tensor) -> torch.Tensor:
        """Returns processed rewards.

        Args:
            reward: reward.

        Returns:
            processed reward.

        """
        raise NotImplementedError

    def reverse_transform(self, reward: torch.Tensor) -> torch.Tensor:
        """Returns reversely processed rewards.

        Args:
            reward: reward.

        Returns:
            reversely processed reward.

        """
        raise NotImplementedError

    def transform_numpy(self, reward: np.ndarray) -> np.ndarray:
        """Returns transformed rewards in numpy array.

        Args:
            reward: reward.

        Returns:
            transformed reward.

        """
        raise NotImplementedError

    def get_type(self) -> str:
        """Returns a scaler type.

        Returns:
            scaler type.

        """
        return self.TYPE

    def get_params(self, deep: bool = False) -> Dict[str, Any]:
        """Returns scaling parameters.

        Args:
            deep: flag to deeply copy objects.

        Returns:
            scaler parameters.

        """
        raise NotImplementedError


class ClipRewardScaler(RewardScaler):
    r"""Reward clipping preprocessing.

    .. code-block:: python

        from d3rlpy.preprocessing import ClipRewardScaler

        # clip rewards within [-1.0, 1.0]
        reward_scaler = ClipRewardScaler(low=-1.0, high=1.0)

        cql = CQL(reward_scaler=reward_scaler)

    Args:
        low (float): minimum value to clip.
        high (float): maximum value to clip.

    """

    TYPE: ClassVar[str] = "clip"
    _low: Optional[float]
    _high: Optional[float]

    def __init__(
        self, low: Optional[float] = None, high: Optional[float] = None
    ):
        self._low = low
        self._high = high

    def fit(self, episodes: List[Episode]) -> None:
        if self._low is None and self._high is None:
            LOG.warning("Please initialize ClipRewardScaler manually.")

    def transform(self, reward: torch.Tensor) -> torch.Tensor:
        return reward.clamp(self._low, self._high)

    def reverse_transform(self, reward: torch.Tensor) -> torch.Tensor:
        return reward

    def transform_numpy(self, reward: np.ndarray) -> np.ndarray:
        return np.clip(reward, self._low, self._high)

    def get_params(self, deep: bool = False) -> Dict[str, Any]:
        return {"low": self._low, "high": self._high}


class MinMaxRewardScaler(RewardScaler):
    r"""Min-Max reward normalization preprocessing.

    .. math::

        r' = (r - \min(r)) / (\max(r) - \min(r))

    .. code-block:: python

        from d3rlpy.algos import CQL

        cql = CQL(reward_scaler="min_max")

    You can also initialize with :class:`d3rlpy.dataset.MDPDataset` object or
    manually.

    .. code-block:: python

        from d3rlpy.preprocessing import MinMaxRewardScaler

        # initialize with dataset
        scaler = MinMaxRewardScaler(dataset)

        # initialize manually
        scaler = MinMaxRewardScaler(minimum=0.0, maximum=10.0)

        cql = CQL(scaler=scaler)

    """
    TYPE: ClassVar[str] = "min_max"
    _minimum: Optional[float]
    _maximum: Optional[float]

    def __init__(
        self,
        dataset: Optional[MDPDataset] = None,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
    ):
        self._minimum = None
        self._maximum = None
        if dataset:
            self.fit(dataset.episodes)
        elif minimum is not None and maximum is not None:
            self._minimum = minimum
            self._maximum = maximum

    def fit(self, episodes: List[Episode]) -> None:
        if self._minimum is not None and self._maximum is not None:
            return

        rewards = []
        for episode in episodes:
            rewards += episode.rewards[1:].tolist()

        self._minimum = float(np.min(rewards))
        self._maximum = float(np.max(rewards))

    def transform(self, reward: torch.Tensor) -> torch.Tensor:
        assert self._minimum is not None and self._maximum is not None
        return (reward - self._minimum) / (self._maximum - self._minimum)

    def reverse_transform(self, reward: torch.Tensor) -> torch.Tensor:
        assert self._minimum is not None and self._maximum is not None
        return reward * (self._maximum - self._minimum) + self._minimum

    def transform_numpy(self, reward: np.ndarray) -> np.ndarray:
        assert self._minimum is not None and self._maximum is not None
        return (reward - self._minimum) / (self._maximum - self._minimum)

    def get_params(self, deep: bool = False) -> Dict[str, Any]:
        return {"minimum": self._minimum, "maximum": self._maximum}


class StandardRewardScaler(RewardScaler):
    r"""Reward standardization preprocessing.

    .. math::

        r' = (r - \mu) / \sigma

    .. code-block:: python

        from d3rlpy.algos import CQL

        cql = CQL(reward_scaler="standard")

    You can also initialize with :class:`d3rlpy.dataset.MDPDataset` object or
    manually.

    .. code-block:: python

        from d3rlpy.preprocessing import StandardRewardScaler

        # initialize with dataset
        scaler = StandardRewardScaler(dataset)

        # initialize manually
        scaler = StandardRewardScaler(mean=0.0, std=1.0)

        cql = CQL(scaler=scaler)

    """
    TYPE: ClassVar[str] = "standard"
    _mean: Optional[float]
    _std: Optional[float]
    _eps: float

    def __init__(
        self,
        dataset: Optional[MDPDataset] = None,
        mean: Optional[float] = None,
        std: Optional[float] = None,
        eps: float = 1e-3,
    ):
        self._mean = None
        self._std = None
        self._eps = eps
        if dataset:
            self.fit(dataset.episodes)
        elif mean is not None and std is not None:
            self._mean = mean
            self._std = std

    def fit(self, episodes: List[Episode]) -> None:
        if self._mean is not None and self._std is not None:
            return

        rewards = []
        for episode in episodes:
            rewards += episode.rewards[1:].tolist()

        self._mean = float(np.mean(rewards))
        self._std = float(np.std(rewards))

    def transform(self, reward: torch.Tensor) -> torch.Tensor:
        assert self._mean is not None and self._std is not None
        return (reward - self._mean) / (self._std + self._eps)

    def reverse_transform(self, reward: torch.Tensor) -> torch.Tensor:
        assert self._mean is not None and self._std is not None
        return reward * (self._std + self._eps) + self._mean

    def transform_numpy(self, reward: np.ndarray) -> np.ndarray:
        assert self._mean is not None and self._std is not None
        return (reward - self._mean) / (self._std + self._eps)

    def get_params(self, deep: bool = False) -> Dict[str, Any]:
        return {"mean": self._mean, "std": self._std, "eps": self._eps}


REWARD_SCALER_LIST: Dict[str, Type[RewardScaler]] = {}


def register_reward_scaler(cls: Type[RewardScaler]) -> None:
    """Registers reward scaler class.

    Args:
        cls: scaler class inheriting ``RewardScaler``.

    """
    is_registered = cls.TYPE in REWARD_SCALER_LIST
    assert not is_registered, "%s seems to be already registered" % cls.TYPE
    REWARD_SCALER_LIST[cls.TYPE] = cls


def create_reward_scaler(name: str, **kwargs: Any) -> RewardScaler:
    assert name in REWARD_SCALER_LIST, f"{name} seems not to be registered."
    reward_scaler = REWARD_SCALER_LIST[name](**kwargs)  # type: ignore
    assert isinstance(reward_scaler, RewardScaler)
    return reward_scaler


register_reward_scaler(ClipRewardScaler)
register_reward_scaler(MinMaxRewardScaler)
register_reward_scaler(StandardRewardScaler)
