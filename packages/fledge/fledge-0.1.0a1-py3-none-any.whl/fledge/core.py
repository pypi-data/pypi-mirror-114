"""Core classes of Fledge."""
# flake8: noqa
# TODO: re-add to flake8
from __future__ import annotations

import collections
import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import final
from typing import Generic
from typing import List
from typing import Mapping
from typing import Optional
from typing import Set
from typing import TypeVar
from typing import Union

import networkx as nx
from pyvis.network import Network

from . import utils
from .exceptions import NoPathError
from .named import Named
from .registry import Registry


logger = logging.getLogger(__name__)


# TODO: move typing to its own module.

# Type variables for spaces
Q = TypeVar("Q", bound="Space")
R = TypeVar("R", bound="Space")
S = TypeVar("S", bound="Space")
T = TypeVar("T", bound="Space")

# Type variables for the types of spaces.
Q_t = TypeVar("Q_t")
R_t = TypeVar("R_t")
S_t = TypeVar("S_t")
T_t = TypeVar("T_t")

# Type variables bound to the various core classes.
N = TypeVar("N", bound="Node")
N_new = TypeVar("N_new", bound="Node")
N1 = TypeVar("N1", bound="Node")
N2 = TypeVar("N2", bound="Node")
F = TypeVar("F", bound="Frame")
F_new = TypeVar("F_new", bound="Frame")
B = TypeVar("B", bound="Body")
E = TypeVar("E", bound="Edge")
E_new = TypeVar("E_new", bound="Edge")

# Type variables bound to types of nodes
N_t = TypeVar("N_t")
N1_t = TypeVar("N1_t")
N2_t = TypeVar("N2_t")
F_t = TypeVar("F_t")
F1_t = TypeVar("F1_t")
F2_t = TypeVar("F2_t")
B_t = TypeVar("B_t")


Ref = TypeVar("Ref", bound="Reference")
Ref_new = TypeVar("Ref_new", bound="Reference")
Tr = TypeVar("Tr", bound="Transform")
Tr_new = TypeVar("Tr_new", bound="Transform")
P = TypeVar("P", bound="Projection")
Proj = TypeVar("Proj", bound="Projection")

# registries.
_frame_registry = Registry()
_space_registry = Registry()
_projection_registry = Registry()


def get_space(space: Union[str, S]) -> S:
    """Get a space by name."""
    if is_space(space):
        return space
    elif space in _space_registry:
        return _space_registry[space]
    else:
        raise KeyError(f"unkown space: {space}")


def get_projection(projection: Union[str, S]) -> S:
    """Get a projection by name."""
    if is_projection(projection):
        return projection
    elif projection in _projection_registry:
        return _projection_registry[projection]
    else:
        raise KeyError(f"unkown projection: {projection}")


def is_space(item: Any) -> bool:
    """Return true if the given item is a space."""
    return issubclass(type(item), Space)


def is_frame(item: Any) -> bool:
    """Return true if the given item is a frame."""
    return issubclass(type(item), Frame)


def is_body(item: Any) -> bool:
    """Return true if the given item is a body."""
    return issubclass(type(item), Body)


def is_edge(item: Any) -> bool:
    """Return true if the given item is an edge."""
    return issubclass(type(item), Edge)


def is_projection(item: Any) -> bool:
    """Return true if the given item is a projection."""
    return issubclass(type(item), Projection)


def is_transform(item: Any) -> bool:
    """Return true if the given item is a transform."""
    return issubclass(type(item), Transform)


def is_reference(item: Any) -> bool:
    """Return true if the given item is a reference."""
    return issubclass(type(item), Reference)


class Space(Named, Mapping[Union[str, F], F]):
    """A space is a set of physical objects.

    All space instances are mutually disjoint.

    A `Space` represents a physical space, like a room or a 2D sheet of paper.

    It contains nodes and can be refered to by a name.

    Spaces are most often created when someone instantiates a Frame using a
    string as a space. If it doesn't exist yet, the appropriate space gets
    created from scratch.

    This means there's never a situation where you'd have a frame that wasn't in
    a space already, so no need to pass frames already created to the space.

    """

    frames: Dict[str, F]

    def __init__(self, name: Optional[str] = None) -> None:
        """TODO: docs."""
        Named.__init__(self, name)
        _space_registry.add(self)

        self.frames = dict()

    @final
    def rename(self, name: str) -> S:
        """TODO: docs."""
        _space_registry.remove(name)
        super(Space, self).rename(name)
        _space_registry.add(self)
        return self

    def get(self, frame: Union[str, F]) -> F:
        """TODO: docs."""
        if is_frame(frame):
            if frame.name not in self.frames:
                raise RuntimeError(f"frame {frame} is not in {self}")
            return frame

        if frame not in self.frames:
            raise KeyError(f"no frame called {frame} in {self}")
        return self.frames[frame]

    def add(self, frame: F):
        """TODO: docs."""
        self.frames[frame.name] = frame

    def remove(self, frame: Union[str, F]) -> None:
        """TODO: docs."""
        if isinstance(frame, str):
            del self.frames[frame]
        elif is_frame(frame):
            del self.frames[frame.name]
        else:
            raise TypeError

    def __contains__(self, item: Union[str, N]) -> bool:
        """Determine whether `item` is in the space.

        In GeoFrame, all nodes must store a reference to their set. Thus, this
        method simply checks whether the node's space IS this one.

        """
        if isinstance(item, str):
            return item in self.frames
        elif is_frame(item):
            return item.name in self.frames
        elif issubclass(type(item), Node):
            return item.space == self
        else:
            return NotImplemented

    def __getitem__(self, frame: Union[str, F]) -> F:
        """TODO: docs."""
        return self.get(frame)

    def __setitem__(self, name: str, frame: F):
        """TODO: docs."""
        if frame.name != name:
            raise ValueError
        self.frames[name] = frame

    def __iter__(self):
        """TODO: docs."""
        return iter(self.frames.values())

    def __len__(self):
        """TODO: docs."""
        return len(self.frames)

    def __str__(self):
        """TODO: docs."""
        return f'{self.__class__.__name__}(name="{self.name}")'


class Node(Generic[S]):
    """A node represents an object in a physical space.

    A node can only belong to one space. All nodes contain references to the
    space they are in, but only frames are referenced by their space.

    The Node class itself can be used, but it almost never should be. It is a
    starting point for more restrictive classes: Frame and Body. It contains
    functions which are common to all nodes.

    Args:
        space: the name of the space this node is in. If not provided, or name
            does not already refer to this space, a new space is created of type
            `self.space_type_bound`.


    Attributes:
        space: the space this node is in. If a name is provided, and the name is
            not used, a new
            space is created. If None, and `defining_frame` is provided as an
            instance, defining_frame.space is used.
        defining_frame: the frame which defines this node, if it exists.
        defining_edge: the edge from `defining_frame` to `self`, if it exists.
        incoming_projections: mapping from projection

    """

    # Class variables
    space_type_bound: S_t = Space

    # Attributes
    space: S
    defining_frame: Optional[F] = None
    defining_edge: Optional[E] = None

    def __init__(
        self,
        defining_edge: Optional[E] = None,
        defining_frame: Optional[Union[str, F]] = None,
        space: Optional[Union[str, S]] = None,
    ) -> None:
        """TODO: docs."""
        if space is None and defining_frame is not None:
            if not is_frame(defining_frame):
                raise ValueError(
                    f"if space is not provided, `defining_frame` must be the "
                    f"Frame instance. Got: {defining_frame}"
                )
            space = defining_frame.space
        elif space is None or (isinstance(space, str) and space not in _space_registry):
            space = self.space_type_bound(name=space)
        else:
            space = get_space(space)

        if not issubclass(type(space), self.space_type_bound):
            raise TypeError(
                f"{self.__class__.__name__} nodes must be in a space that inherit from "
                f"{self.space_type_bound.__name__}"
            )

        if is_frame(defining_frame) and defining_frame not in space:
            raise ValueError("defining frame not in space")
        elif isinstance(defining_frame, str):
            defining_frame = space.get(defining_frame)

        if defining_edge is not None and not isinstance(
            self, defining_edge.output_type
        ):
            raise TypeError(
                f"tried to define a {self.__class__.__name__} object with "
                f"{defining_edge}"
            )

        if (defining_frame is None) != (defining_edge is None):
            raise RuntimeError(
                "must provide both a defining edge and a frame or neither"
            )

        self.space = space
        self.defining_edge = defining_edge
        self.defining_frame = defining_frame

    def connect(  # noqa: C901
        self,
        edge: E,
        frame: Optional[Union[str, F]] = None,
        space: Optional[Union[str, S]] = None,
    ) -> N:
        """Add or modify an incoming edge to this frame.

        Reposition this frame by redefining its incoming edge, possibly in
        another frame.

        Note that this does not create a new frame but rather redefines this
        existing one. To create a new frame, use
        `defining_frame.connect(defining_edge)`.

        Args:
            edge: The new incoming edge which will define the frame.
            frame: The frame to define this frame in. If None, `self.defining_frame` is
                used. If `self.defining_frame is None` (i.e. `self` is a source node), then an
                existing frame or the name of an existing frame must be provided.
            space: Must be provided if edge is a projection and only the name of the source frame is
                provided, to find the instance of the frame. Otherwise not needed.

        Returns:
            N: returns self, for convenience. `locate()` is still in-place.

        Raises:
            RuntimeError: If the space is not provided for frame lookup by string.
            TypeError: If the types being connected do not align.
            ValueError: If insufficient args are provided.

        """
        # TODO: isn't this a frame method?
        #
        if self.defining_frame is None and frame is None:
            raise ValueError(
                f"cannot connect a node without a frame to form the source of the connection. "
                f"Provide `frame` to form an edge from that frame to this one."
            )

        if is_projection(edge):
            if frame is None:
                raise RuntimeError(
                    "the source frame must be provided when connecting an incoming projection"
                )
            if isinstance(frame, str):
                assert (
                    space is not None
                ), "must provide the space of the input frame for lookup"
                space = get_space(space)
                frame = space.get(frame)
            if not issubclass(type(frame), edge.input_type_bound):
                raise TypeError(
                    f"input nodes to {edge} must subclass {edge.input_type_bound.__name__}, got: {frame}"
                )
            if not isinstance(self, edge.output_type):
                raise TypeError(
                    f"{edge} produces {edge.ouput_type.__name__} nodes, cannot connect to: {self}"
                )

            self.incoming_projections[edge] = frame
            if edge.reversible():
                frame.incoming_projections[edge.reverse()] = self

        elif is_transform(edge):
            self.defining_edge = edge
            if frame is not None:
                frame = self.space.get(frame)

                if not issubclass(frame, edge.input_type_bound):
                    raise TypeError(
                        f"input nodes to {edge} must subclass {edge.input_type_bound.__name__}, got: {frame}"
                    )
                if not isinstance(self, edge.output_type):
                    raise TypeError(
                        f"{edge} produces {edge.ouput_type.__name__} nodes, cannot connect to: {self}"
                    )

                if self.defining_frame is None or self.defining_frame != frame:
                    self.defining_frame.defined_frames.remove(self)
                    frame.defined_frames.add(self)
                    self.defining_frame = frame

        elif is_reference(edge):
            self.defining_edge = edge
            if frame is not None:
                frame = self.space.get(frame)

                if not issubclass(frame, edge.input_type_bound):
                    raise TypeError(
                        f"input nodes to {edge} must subclass {edge.input_type_bound.__name__}, got: {frame}"
                    )
                if not isinstance(self, edge.output_type):
                    raise TypeError(
                        f"{edge} produces {edge.ouput_type.__name__} nodes, cannot connect to: {self}"
                    )
                self.defining_frame = frame
        else:
            raise TypeError

        return self

    @final
    def in_frame(
        self,
        frame: Union[str, F],
        projection: Union[None, str, P, List[Union[str, P]]] = None,
    ) -> E:  # F[R], P -> E[R_t, S_t]
        """Get the representation of the object in the given frame.

        If no projection is provided, `in_frame()` will return a new edge which leads to the same
        node (theoretically) but from the given frame, in the same space.

        If a projection is provided, `in_frame()` will return a new node by taking that projection
        from the projection's input space to `self.space`, returning an edge to a *wholly different*
        node in `frame.space`.

        If multiple projections are provided, only one is considered at a time. This is useful if
        the path to the desired frame passes through more than one intermediate space.

        If the desired frame is reachable *without* traversing the given projection,

        In general, the projection needs to be provided that links `self.space` to `frame.space`.
        This is because multiple projections might link the spaces, each of which would lead to a
        `different` end-node. GeoFrame resolves this ambiguity by only allowing one projection to be
        allowed to be traversed at a time.

        TODO: don't combine edges unless you need to, just keep a list of the edges and then combine
        the ones on the chosen path.

        Args:
            frame: the desired frame to represent `self` in, or the name of the frame.
            projection: a projection or list of projections which are valid to cross, in order.

        Raises:
            NoPathError: if there is no path to the desired frame utilizing the projection. This is
                also raised if the desired frame is reachable without using a projection provided,
                to prevent confusion about which space a frame is in.
            KeyError: if the desired frame is not in the space reachable using projection(s)

        """
        if projection is None:
            projections = collections.deque()
        else:
            projections = collections.deque(
                [get_projection(p) for p in utils.listify(projection)]
            )

        if len(projections) == 0:
            # There are no projections, so the frame must be in the starting space
            desired_frame = self.space.get_frame(frame)
        else:
            # We may not know the desired frame yet. Only when projections is empty
            desired_frame = None

        if is_frame(self):
            edge = self.identity()
            discovered = set([self])
            queue = collections.deque([(self, edge)])
        elif self.defining_edge is None or self.defining_frame is None:
            raise NoPathError(f"node has no frame of reference: {self}")
        else:
            edge = self.defining_edge
            discovered = set([self.defining_frame])
            queue = collections.deque([(self.defining_frame, self.defining_edge)])

        while len(queue) > 0:

            f, e = queue.popleft()
            assert is_frame(f), f"not a frame: {f}"

            # We have finally arrived at the desired space. Get the desired frame.
            if len(projections) == 0 and desired_frame is None:
                desired_frame = f.space.get_frame(frame)

            # There are no more projections to traverse, and the desired frame is found.
            if len(projections) == 0 and f == desired_frame:
                return e

            # Enqueue the frame that f is in, if it is not a source.
            if not f.is_source() and f.defining_frame not in discovered:
                assert f.defining_frame.space == f.space
                discovered.add(f.defining_frame)
                queue.append((f.defining_frame, f.defining_edge @ e))

            # enqueue all frames that are defined by f
            for df in f.defined_frames:
                if df not in discovered and df.defining_edge.invertible():
                    assert df.space == f.space
                    discovered.add(df)
                    queue.append((df, df.defining_edge.inverse() @ e))

            # Check if projections[0] is among the projections coming into f.
            for p, incoming_f in self.incoming_projections.items():
                if p == projections[0]:
                    # Follow the projection into the new space. (Search starts over)
                    assert incoming_f.space != f.space
                    queue.clear()
                    queue.append((incoming_f, p @ e))
                    projections.popleft()
                    break

    @final
    def into(
        self,
        frame: Union[str, F],
        projection: Union[str, P, List[Union[str, P]]],
        **kwargs,
    ) -> F:
        """Creates a new node defined in the new frame in the same location as this one.

        The difference between `in_frame()` and `into()` is that `in_frame()` returns the edge
        representation without creating a new node. `into()` returns a new node which could be
        manipulated independently of the old one.

        """
        return frame.traverse(self.in_frame(frame, projection), **kwargs)

    def orphan(self) -> None:
        """Orphan this node by disconnecting it from all other nodes.

        Sub-classes should override this.

        """
        self.defining_frame = None
        self.defining_edge = None

    def is_source(self) -> bool:
        """Whether the node has a defining edge (and frame)."""
        return self.defining_edge is None or self.defining_frame is None

    def is_orphan(self) -> bool:
        """Should encompass any other incoming or outgoing edges for a frame."""
        return self.is_source()

    def vis_properties(self) -> Dict[str, Any]:
        return dict(shape="dot")

    #
    # Convenience methods
    #

    # TODO: use x[f] to mean x.in_frame(f) and x.over(p) to mean x.in_frame(<frame pointed to by p>,
    # p). This means spaces must contain a mapping from the named projections to the frames they
    # point to.
    #
    def __getitem__(
        self,
        frame: Union[str, F],
        projection: Union[None, str, P, List[Union[str, P]]] = None,
    ) -> E:
        pass


class Frame(Node[S]):
    """A Frame provides a frame of reference to describe an object or `Body` in that space.

    A Frame has in-degree <= 1 (not counting the self-loop, which all Frames have) and any
    out-degree. Frames are similar to Bodies, in that they usually have one incoming edge and can be
    referenced in other frames, but they are not the same. A frame may have no incoming edges, and
    Frames cannot be projected onto other spaces.

    since they will be defined in connection to another frame, except for the "world" frame, which
    has no incoming edges. (There may be more than one world frame.)

    That is, most Frames are also Bodies, from the perspective of their own reference frame.

    Frames can be sources in the graph, a "world frame". A "world" is a connected component of the
    overall universe, which is directed and acyclic, where the "world frame" is the source node.

    Frames can be subclassed to specify how a point would be represented in that frame, and to have
    non-generic frames that only exist in one kind of space (e.g. CartesianFrame3D, which only
    exists in Euclidean3D space.) Sub-classes are responsible for calling super().

    Sub-classes may wish to override:
    * `identity()`
    * `space_type_bound`, a class variable.

    Args
        defining_frame: The reference frame defining this one, if it exists. (A Frame does not need to be defined in terms of another frame). Defaults to None.
        defining_edge: the edge from `defining_frame` to self. Must be provided if frame is not None.
        space: The space (or name of the space) that this frame is in. This is only needed when `defining_frame` is a `str`,
            or if this Frame is an orphan, but its space has already been created. Then it should be specified, or else a new space is created using.
            If `space` and `defining_frame` are not provided, a new space is created using self.space_type_bound. If `defining_frame`
            is provided, that space is used. If both provided, they must match.

    """

    # Attributes
    defined_frames: Set[F]
    incoming_projections: Dict[P, F] = dict()

    def __init__(
        self,
        defining_edge: Optional[E] = None,
        defining_frame: Optional[Union[str, F]] = None,
        space: Optional[Union[str, S]] = None,
        name: Optional[str] = None,
    ) -> None:

        if space is None and defining_frame is not None:
            assert is_frame(
                defining_frame
            ), "If `space` is not provided, the Frame instance must be provided direclty."
            space = defining_frame.space

        # creates the space, if it doesn't exist or is None
        super(Frame, self).__init__(
            defining_edge=defining_edge,
            defining_frame=defining_frame,
            space=space,
        )

        # Make a unique name, if not provided.
        if name is None:
            name = f"{self.__class__.__name__}_{len(self.space.frames)}"
        self.name = name
        self.space.add(self)

        # initialize internal graph connections
        self.defined_frames = set()
        self.incoming_projections = dict()

    def __hash__(self):
        return hash(self.space.name + self.name)

    def rename(self, name: str) -> F:
        """Rename the frame and update the space.

        Sub-classes may wish to modify the name somehow. They are responsible for calling
        `super().rename(name)`.

        """
        self.space.remove(self)
        self.name = name
        self.space.add(self)
        return self

    def identity(self: S) -> Identity[S_t]:
        """Get an identity transform on edges from this frame.

        Should be overridden by sub-classes to get identities on those frame types.

        """
        return Identity(self)

    def orphan(self):
        """Orphan this frame by removes all edges to/from it, except to bodies."""
        self.frame.defined_frames.remove(self)
        for f in self.defined_frames:
            f.defining_frame = None
            f.defining_edge = None

    def is_orphan(self) -> bool:
        """Whether the frame is completely unconnected."""
        return (
            self.is_source
            and len(self.defined_frames) == 0
            and len(self.incoming_projections) == 0
        )

    def traverse(self, edge: Union[str, E], **kwargs) -> Union[F, B]:
        """Define new bodies or frames in the same space as this one, by traversing an edge.

        Sub-classes may wish to implement wrappers around connect, like `CartesianFrame3D.point()`,
        which would create a new point, but they should not override connect.

        The traverse method is unique to Frame nodes, since edges can only begin at frames.

        TODO: traverse should use the `^` character.

        Args:
            edge: the edge to follow. If a transform or reference, this is the defining edge of
                the resulting node. If a projection, it is one of the incoming projections.
            kwargs: can include the name of a new frame, or other information to pass to the output
                node constructor.
            name: a name to use if the resulting object is a frame.

        """
        if not issubclass(type(self), edge.input_type_bound):
            raise TypeError(
                f"cannot connect {self} using {edge}, because the edge requires nodes that subclass"
                f" {edge.input_frame_type}"
            )

        if is_projection(edge):
            raise TypeError(
                f"projections cannot be traversed because they require knowing both endpoints"
            )

        new_node = edge.output_type(
            space=self.space, defining_edge=edge.copy(), defining_frame=self, **kwargs
        )

        if is_frame(new_node):
            self.defined_frames.add(new_node)
        return new_node

    def full_name(self):
        """A full name for the frame, guaranteed to be unique."""
        return f"{self.space.name}/{self.name}"

    def vis_properties(self) -> Dict[str, Any]:
        return dict(shape="box")


class Body(Node[S]):
    """A Body is an object in space, connected to a frame in the same space.

    In GeoFrame, a Body has in-degree == 1 and out-degree == 0. This means it is defined precisely
    by exactly one reference frame (although it may have cached references to others).

    Bodies are usually not created directly but rather by their defining edges via `traverse()`.

    """

    defining_edge: E  # E[F_t, B_t]
    defining_frame: F  # F[S]

    def __init__(
        self, defining_edge: E, defining_frame: Union[str, F], space: Optional[S] = None
    ) -> None:
        if defining_edge is None or defining_frame is None:
            raise ValueError(f"bodies must be defined in a frame with an edge")

        super(Body, self).__init__(
            defining_edge=defining_edge, defining_frame=defining_frame, space=space
        )

    def is_source(self) -> bool:
        return False

    def is_orphan(self) -> bool:
        return False


class Edge(ABC, Generic[F, N]):
    """An Edge exists as a mathematical description of spatial objects (Nodes).

    An edge doesn't know about the particular instances of the nodes that it goes between, only the
    types of those nodes, as class variables. These are upper bounds on the type of nodes that the
    edge can go between. The nodes, in turn have upper bounds on the type of space they can be in.

    Edges usually have numrical representations. At least one of these should be implemented in the
    `__array__()` method.

    Sub-classes must define `input_type_bound` and `output_type`, and they must implement `copy()`
    and `join`, which is used by `__matmul__`. `join` defines how the edge interracts with other
    edges. `copy()` and `output_type` are used by a frame's `traverse()` method to traverse the
    edge.

    Sub-classes may also wish to implement `inverse()`, which finds the inverse of the edge. The
    `invertible()` method simply checks whether inverse() returns None, in which case the edge is
    not invertible.

    Broadly, there are two types of edges:
    - Defining edges: which are the unique descriptions of a node in space. There is only one per
      node.
    - Projection edges: which go between spaces and result in new nodes to be created.

    There are four types of edges.
    * An Identity is a self-loop. It isn't very useful except as a building block for other edges.
    * A Reference is a defining Edge for a Body, where `R == S` is true.
       * References originate in Frames and are only stored in the Body's they reference.
       * A search only traverses a reference if it starts at a Body.
       * References are not invertible or reveresible, since Body's cannot have outgoing edges.
    * A Transform is a defining Edge for a Frame.
       * Transform edges go from a Frame to a different Frame in the same space.
       * References may be invertible.
    * A Projection is an Edge from a Frame in one space to a Frame in a different space.
       * An `onto()` search is limited to traversing one projection at a time.
       * Strictly speaking, projections are not invertible by definition, since they cannot be
         idempotent. However, for simplicity, we consider a projection to be invertible if there is
         a known projection in the opposite direction, even though it cannot return the original
         node exactly.

    Edges can be composed together to form a shortcut over the path they form. This is done with the
    `@` operator, as with matrix multiplication. Conceptually, edges can transform other edges but not
    non-edge nodes.

    If an edge is invertible, it is responsible for handling its own inverse. For example, if a
    point is actually moved, so that the edge to it is changed, the edge must change its own inverse
    as well to match.

    """

    input_type_bound: F_t = Frame
    output_type: N_t = Node

    def __init__(self):
        # TODO type checks
        pass

    def __matmul__(self, other: E) -> E_new:
        """The matmul operator returns a new edge equivalent to traversing self and other.

        Say I have a world frame W, frames A and B both defined in W, and a body x in frame B.

        ```
        A <----- W -----> B ----> x
           T_WA     T_WB     x_B
        ```

        where T_WA is A.incoming_edge, T_WB is B.incoming_edge, and x_B is x.incoming_edge.

        The numerical representation of x in frame A would be:

        ```
        T_WA.inv @ T_WB @ x_B
        ```

        A reference edge can only be placed at the end of this chain.

        Sub-classes should implement matmul to be a new edge equivalent to traversing both edges.

        TODO: gracefully handle cases where other is some other type (e.g. an array) that can be
        interpreted as an edge in context.

        """
        if not issubclass(self.output_type, other.input_type_bound):
            raise TypeError(
                f"cannot join {self} (output type {self.output_type.__name__}) "
                f"with {other} (input type bound {other.input_type_bound.__name__})"
            )

        return self.join(other)

    @abstractmethod
    def join(self, other: E) -> E_new:
        """Join the two edges together.

        This is the functional representation of the edge, meant to be overwritten by the user.

        """
        pass

    @abstractmethod
    def copy(self) -> E:
        """Copy self. For named edges (projections), this will require creating a new name.

        Sub-classes are responsible for implementing `copy()` so that the Identity edge functions
        properly. In most cases, this will just involve copying the edge's array.

        """
        pass

    def __rmatmul__(self, other: E) -> E_new:  # E[Q_t, R_t] -> E_new[Q_t, S_t]
        if is_edge(other):
            return other @ self
        else:
            return NotImplemented

    def inverse(self) -> Optional[E_new]:  # E[R_t, S_t]:
        return None

    def invertible(self) -> bool:
        """Determine whether the edge is invertible.

        Sub-classes may wish to override this method if the invertibility is known without
        attempting to actually compute the inverse.

        """
        return self.inverse() is not None

    def __array__(self):
        """Edges usually have at least one numerical representation.

        Some edges may have more than one natural representation (e.g. rotations). These should have
        a natural default and implement the others as methods.

        """
        raise NotImplementedError()


class Identity(Edge[N_t, N_t]):
    """The generic identity edge, which is a self-loop.

    Sub-classes may wish to implement __array__ to represent numerically meaningful identity
    functions.

    """

    def __init__(self) -> None:
        super(Identity, self).__init__(inverse=None)

    def join(self, other: E) -> E_new:  # E[S_t, T_t] -> E_new[S_t, T_t]
        return other.copy()

    def copy(self):
        return Identity()

    def inverse(self):
        return self

    def invertible(self):
        return True


class Reference(Edge[F_t, B_t]):
    """A Reference is a Edge that terminates at a Body.

    References are not invertible, and they cannot be joined together with matmul.

    Note that the bodies these references describe *may* implement matmul, such as vectors being
    multiplied, but edges are descriptions, and only edges between frames can be joined.

    The base reference is a so-called "generic" reference, because it can be used to connect nodes
    but it doesn't contain any data.

    TODO: decide whether these base classes should be generic or abstract.

    """

    input_type_bound = Frame
    output_type = Body

    def __init__(self):
        super(Reference, self).__init__()

    @final
    def join(self, other):
        raise ValueError(f"cannot join reference with any other edge")

    def copy(self):
        return Reference()

    def inverse(self):
        return None

    def invertible(self):
        return False


class Transform(Edge[F1_t, F2_t]):
    """A Transform is an edge to a frame in the same space.

    The base transform is invertible, defines only generic relationship, and stores no information.
    When joined with more sophisticated edges, it makes them generic.

    """

    input_type_bound = Frame
    output_type = Frame

    def __init__(self) -> None:
        if not issubclass(self.output_type, Frame):
            raise TypeError(
                f"transforms must map between frames. got output_type: {self.output_type.__name__}"
            )

        super(Transform, self).__init__()

    def join(self, other):
        if is_reference(other):
            return Reference()
        elif is_transform(other):
            return Transform()
        elif is_projection(other):
            return Projection()
        else:
            return NotImplemented

    def copy(self):
        return Transform()

    def inverse(self):
        return Transform()

    def invertible(self):
        return True


class Projection(Named, Edge[F1_t, F2_t]):
    """A Projection is an edge that goes to a different space.

    Projections are not invertible, by definition. However, they may be reversible. If this is the
    case, the frame is responsible for adding the projection's reverse to the graph.

    The base Projection is generic.

    Projections are named because they are uniquely identified paths between spaces and have no
    guarantee of maintaining spatial relationships with one another.

    """

    input_type_bound = Frame
    ouput_type = Frame

    def __init__(self, name: Optional[str] = None):
        Edge.__init__(self)
        Named.__init__(self, name=name)

    def join(self, other):
        if is_reference(other):
            return Reference()
        elif is_transform(other):
            return Projection()
        elif is_projection():
            return Projection()
        else:
            return NotImplemented

    def copy(self):
        return Projection()

    @final
    def inverse(self):
        return None

    @final
    def invertible(self):
        return False

    def reverse(self, name: Optional[str] = None) -> Optional[P]:
        """Get the reverse of the projection.

        This is used to add the projection that goes in the opposite direction. This is not the same
        as the inverse, since extra information would be needed to get the same object, but it is
        similar.

        For example, a camera projection takes points in 3D and projections them onto 2D image
        indices. The reverse would be a projection that takes a 2D point on the image and returns
        the line connecting that point and the focal point.

        Args:
            name: the name for the reversed Projection.

        """
        return None

    def reversible(self) -> bool:
        """Determine whether the projection is reversible.

        Sub-classes may wish to implement a version that doesn't require actually creating the
        reverse.

        """
        return self.reverse() is not None


def get_graph(*bodies: B) -> nx.MultiGraph:
    """Show the reference graph, with the provided bodies shown.

    TODO: re-implemented using NetworkX rather than pyvis (more general).

    TODO: simply iterate over the set of frames and add them all as nodes, then add their edges.
    Don't do a graph traversal.

    Multiple edges might exist between two frames. Use nx.MultiGraph to allow this.

    Invertible/reversible edges should have their inverse/reverse drawn in dashed lines.

    Projections, Transforms, and References should all be different colors.

    Projections, frames, and spaces should have their names on the graph.

    Spaces should be represented as group:
    https://pyvis.readthedocs.io/en/latest/tutorial.html#node-properties.

    """
    g = nx.MultiGraph()

    # First, add all the nodes in all the spaces
    for space in _space_registry.values():
        for frame in space:
            g.add_node(
                frame.full_name(),
                name=frame.name,
                space=space.name,
                **frame.vis_properties(),
            )

    # add all the edges
    for space in _space_registry.values():
        for frame in space:
            # add the defining edge
            if not frame.is_source():
                g.add_edge(frame.defining_frame.full_name(), frame.full_name())

            for p, f in frame.incoming_projections.items():
                g.add_edge(f.full_name(), frame.full_name(), key=p.name, label=p.name)

    # add all the bodies provided
    for i, body in enumerate(bodies):
        bid = f"bodies[{i}]"
        g.add_node(bid, space=body.space.name, **body.vis_properties())
        g.add_edge(bid, body.defining_frame.full_name())

    return g


def show(*bodies: B, path: str = "fledge_graph.html") -> None:
    """Get the reference graph and show it in an interactive window."""
    g = get_graph(*bodies)
    nt = Network("500px", "500px", directed=True)
    nt.set_edge_smooth("dynamic")
    nt.from_nx(g)
    nt.show(path)
