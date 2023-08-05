# flake8: noqa
# TODO: re-add to flake8
from typing import Final
from typing import Optional
from typing import TypeVar

from ..core import Space


SomeEuclidean = TypeVar("SomeEuclidean", bound="Euclidean")


class Euclidean(Space):
    dim: int

    def __init__(self, dim: int, name: Optional[str] = None) -> None:
        super(Euclidean, self).__init__(name=name)
        self.dim = dim


class Euclidean1d(Euclidean):
    """1D euclidean space.

    Euclidean1D is a sub-class of Euclidean, because any edge that can go from a N-dim Euclidean
    frame can also go from a 1D Euclidean frame.

    """

    dim: Final[int]

    def __init__(self, name: Optional[str] = None) -> None:
        super(Euclidean1d, self).__init__(dim=1, name=name)


class Euclidean2d(Euclidean):
    dim: Final[int]

    def __init__(self, name: Optional[str] = None) -> None:
        super(Euclidean2d, self).__init__(dim=2, name=name)


class Euclidean3d(Euclidean):
    dim: Final[int]

    def __init__(self, name: Optional[str] = None) -> None:
        super(Euclidean3d, self).__init__(dim=3, name=name)
