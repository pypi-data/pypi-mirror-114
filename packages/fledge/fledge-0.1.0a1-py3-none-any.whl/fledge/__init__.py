"""Fledge: Spatial Programming with Reference Graphs."""
import importlib.metadata as importlib_metadata

from .core import Body
from .core import Edge
from .core import Frame
from .core import get_graph
from .core import get_projection
from .core import get_space
from .core import Identity
from .core import is_body
from .core import is_edge
from .core import is_frame
from .core import is_projection
from .core import is_reference
from .core import is_space
from .core import is_transform
from .core import Node
from .core import Projection
from .core import Reference
from .core import show
from .core import Space
from .core import Transform

__version__ = importlib_metadata.version(__name__)


__all__ = [
    "get_space",
    "get_projection",
    "is_space",
    "is_frame",
    "is_body",
    "is_edge",
    "is_projection",
    "is_transform",
    "is_reference",
    "Space",
    "Node",
    "Frame",
    "Body",
    "Edge",
    "Identity",
    "Reference",
    "Transform",
    "Projection",
    "get_graph",
    "show",
    "__version__",
]
