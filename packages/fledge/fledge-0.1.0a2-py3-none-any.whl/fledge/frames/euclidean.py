"""Simple coordinate frames which could contain points or vectors."""
# flake8: noqa
# TODO: re-add to flake8
from typing import Optional
from typing import TypeVar

from ..core import F
from ..core import F_new
from ..core import Frame
from ..core import get_space
from ..core import R
from ..core import R_t
from ..core import S
from ..core import S_t
from ..core import T
from ..spaces.euclidean import Euclidean
from ..spaces.euclidean import Euclidean1d
from ..spaces.euclidean import Euclidean2d
from ..spaces.euclidean import Euclidean3d
from ..spaces.euclidean import SomeEuclidean


SomeEuclideanFrame = TypeVar("SomeEuclideanFrame", bound="EuclideanFrame")


class EuclideanFrame(Frame[SomeEuclidean]):
    """A frame in a euclidean space, which has some dimension."""

    space_type_bound = Euclidean

    @property
    def dim(self):
        return self.space.dim


class Cartesian1d(EuclideanFrame[Euclidean1d]):
    space_type_bound = Euclidean1d


class Cartesian2d(EuclideanFrame[Euclidean2d]):
    """Cartesian plane with (x,y) references."""

    space_type_bound = Euclidean2d


class Cartesian3d(EuclideanFrame[Euclidean3d]):
    space_type_bound = Euclidean3d


class Polar(EuclideanFrame[Euclidean2d]):
    """Polar coordinate frame with (r, phi)."""

    space_type_bound = Euclidean2d


class Spherical(EuclideanFrame[Euclidean3d]):
    """Spherical coordinate frame with (r, theta, phi).

    As defined [here](https://en.wikipedia.org/wiki/Spherical_coordinate_system).

    """

    space_type_bound = Euclidean3d


class Cylindrical(EuclideanFrame[Euclidean3d]):
    """Cylindrical coordinate system with (r, phi, z) coordinates."""

    space_type_bound = Euclidean3d


class HomogeneousCoordinateFrame(EuclideanFrame[SomeEuclidean]):
    """A homogeneous coordinate frame for all your points and vectors."""

    pass


class HFrame1d(HomogeneousCoordinateFrame[Euclidean1d]):
    space_type_bound = Euclidean1d


class HFrame2d(HomogeneousCoordinateFrame[Euclidean2d]):
    space_type_bound = Euclidean2d


class HFrame3d(HomogeneousCoordinateFrame[Euclidean3d]):
    space_type_bound = Euclidean3d


HFrame = HFrame3d
