from typing import Optional, TypeVar, Iterator

from _DoublyLinkedListBase import _DoublyLinkedListBase

T = TypeVar('T')


class PositionalList(_DoublyLinkedListBase[T]):
    """
    A sequential container of elements allowing positional access.

    This class implements a positional list ADT using a doubly linked list as the
    underlying data structure. It provides position-based access and modification
    of elements, supporting efficient insertions and deletions at any position.

    Type Parameters:
        T: The type of elements stored in the list

    Attributes:
        _header: Reference to the header sentinel node
        _trailer: Reference to the trailer sentinel node
        _size: Number of elements in the list

    Performance:
        - Access at a known position: O(1)
        - Insertion at a known position: O(1)
        - Deletion at a known position: O(1)
        - Forward/Backward traversal: O(n)
    """

    class Position:
        """
        An abstraction representing the location of a single element.

        The Position class provides a layer of abstraction over the underlying node
        structure, allowing users to work with positions rather than directly with nodes.
        This helps maintain encapsulation and prevents invalid list modifications.

        Attributes:
            _container: Reference to the PositionalList instance containing this position
            _node: Reference to the node object representing this position
        """

        __slots__ = '_container', '_node'

        def __init__(self, container: "PositionalList[T]", node: _DoublyLinkedListBase._Node) -> None:
            """
            Initialize a new Position instance.

            Args:
                container: The PositionalList instance containing this position
                node: The node object representing this position

            Note:
                This constructor should not be invoked by users directly.
                Positions should only be created by the PositionalList class.
            """
            self._container = container
            self._node = node

        def element(self) -> T:
            """
            Return the element stored at this Position.

            Returns:
                The element stored in the node at this position.

            Note:
                This is the primary method for accessing the element at this position.
            """
            return self._node.element

        def __eq__(self, other: object) -> bool:
            """
            Return True if other represents the same Position.

            Args:
                other: Another object to compare with
                      (typically a Position instance, but must accept any object)

            Returns:
                bool: True if other is a Position instance and represents the same location
                NotImplemented: If other is not a Position instance

            Note:
                Two positions are equal if they refer to the same node in memory.
                Following Python's equality protocol, this method accepts any object type
                and returns NotImplemented for non-Position types.
            """
            if not isinstance(other, PositionalList.Position):
                return NotImplemented

            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other: object) -> bool:
            """
            Return True if other does not represent the same Position.

            Args:
                other: Another object to compare with
                      (typically a Position instance, but must accept any object)

            Returns:
                bool: True if other is a Position instance but represents a different location
                NotImplemented: If other is not a Position instance

            Note:
                Two positions are not equal if they refer to different nodes in memory.
                Following Python's equality protocol, this method accepts any object type
                and returns NotImplemented for non-Position types.
                This method is the logical inverse of __eq__.
            """
            if not isinstance(other, PositionalList.Position):
                return NotImplemented

            return not (self == other)

        @property
        def container(self):
            return self._container

        @property
        def node(self):
            return self._node

    def _validate(self, p: Position) -> _DoublyLinkedListBase._Node:
        """
        Validate position and return associated node.

        Args:
            p: A Position instance to validate

        Returns:
            The node at position p if valid

        Raises:
            TypeError: If p is not a Position instance
            ValueError: If p does not belong to this list or is no longer valid

        Note:
            This is an internal method used to verify position validity before operations.
        """
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')

        if p.container is not self:
            raise ValueError('p does not belong to this container')

        if p.node.next is None:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')

        return p.node

    def _make_position(self, node: Optional[_DoublyLinkedListBase._Node]) -> Optional[Position]:
        """
        Return Position instance for given node (or None if sentinel).

        Args:
            node: The node to create a position for

        Returns:
            A new position instance, or None if node is a sentinel

        Note:
            Returns None for sentinel nodes (header and trailer) to maintain list bounds.
        """
        if node is self._header or node is self._trailer:
            return None

        return self.Position(self, node)

    def first(self) -> Optional[Position]:
        """
        Return the first Position in the list.

        Returns:
            The position of the first element, or None if list is empty

        Note:
            This method provides O(1) access to the first position in the list.
        """
        return self._make_position(self._header.next)

    def last(self) -> Optional[Position]:
        """
        Return the last Position in the list.

        Returns:
            The position of the last element, or None if list is empty

        Note:
            This method provides O(1) access to the last position in the list.
        """
        return self._make_position(self._trailer.prev)

    def before(self, p: Position) -> Optional[Position]:
        """
        Return the Position just before Position p.

        Args:
            p: A valid Position instance

        Returns:
            The position before p, or None if p is the first position

        Raises:
            TypeError: If p is not a Position instance
            ValueError: If p is invalid or does not belong to this list
        """
        node = self._validate(p)
        return self._make_position(node.prev)

    def after(self, p: Position) -> Optional[Position]:
        """
        Return the Position just after Position p.

        Args:
            p: A valid Position instance

        Returns:
            The position after p, or None if p is the last position

        Raises:
            TypeError: If p is not a Position instance
            ValueError: If p is invalid or does not belong to this list
        """
        node = self._validate(p)
        return self._make_position(node.next)

    def __iter__(self) -> Iterator[T]:
        """
        Generate a forward iteration of the elements of the list.

        Yields:
            The element at each position in the list, from first to last

        Note:
            This makes the class iterable, allowing for use in for loops.
            The iteration is performed in O(n) time.
        """
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def _insert_between(self, element: T, predecessor: _DoublyLinkedListBase._Node, successor: _DoublyLinkedListBase._Node) -> Position:
        """
        Add element between existing nodes and return new Position.

        Args:
            element: The element to insert
            predecessor: Node that should precede the new node
            successor: Node that should follow the new node

        Returns:
            The position of the newly inserted element

        Note:
            This private method is used by public insertion methods.
        """
        node = super()._insert_between(element, predecessor, successor)
        return self._make_position(node)

    def add_first(self, element: T) -> Position:
        """
        Insert element at the front of the list.

        Args:
            element: The element to insert

        Returns:
            The position of the newly inserted element

        Note:
            Operation is performed in O(1) time.
        """
        return self._insert_between(element, self._header, self._header.next)

    def add_last(self, element: T) -> Position:
        """
        Insert element at the back of the list.

        Args:
            element: The element to insert

        Returns:
            The position of the newly inserted element

        Note:
            Operation is performed in O(1) time.
        """
        return self._insert_between(element, self._trailer.prev, self._trailer)

    def add_before(self, p: Position, element: T) -> Position:
        """
        Insert element before Position p.

        Args:
            p: The position before which to insert
            element: The element to insert

        Returns:
            The position of the newly inserted element

        Raises:
            TypeError: If p is not a Position instance
            ValueError: If p is invalid or does not belong to this list

        Note:
            Operation is performed in O(1) time after position validation.
        """
        original = self._validate(p)
        return self._insert_between(element, original.prev, original)

    def add_after(self, p: Position, element: T) -> Position:
        """
        Insert element after Position p.

        Args:
            p: The position after which to insert
            element: The element to insert

        Returns:
            The position of the newly inserted element

        Raises:
            TypeError: If p is not a Position instance
            ValueError: If p is invalid or does not belong to this list

        Note:
            Operation is performed in O(1) time after position validation.
        """
        original = self._validate(p)
        return self._insert_between(element, original, original.next)

    def delete(self, p: Position) -> T:
        """
        Remove and return the element at Position p.

        Args:
            p: The position of the element to remove

        Returns:
            The element that was removed

        Raises:
            TypeError: If p is not a Position instance
            ValueError: If p is invalid or does not belong to this list
            Empty: If attempting to delete from an empty list

        Note:
            Operation is performed in O(1) time after position validation.
            The position p becomes invalid after this operation.
        """
        original = self._validate(p)
        return self._delete_node(original)

    def replace(self, p: Position, element: T) -> T:
        """
        Replace the element at Position p with element.

        Args:
            p: The position of the element to replace
            element: The new element to store at position p

        Returns:
            The element formerly at Position p

        Raises:
            TypeError: If p is not a Position instance
            ValueError: If p is invalid or does not belong to this list

        Note:
            Operation is performed in O(1) time after position validation.
            The position p remains valid after this operation.
        """
        original = self._validate(p)
        old_value = original.element
        original._element = element
        return old_value

    def __str__(self) -> str:
        """
        Return a string representation of the list.

        Returns:
            A string containing all elements in order, separated by spaces

        Note:
            This method performs a complete traversal of the list in O(n) time.
        """
        return ' '.join(str(element) for element in self)

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the list.

        Returns:
            A string representation showing the list type and elements

        Note:
            This method performs a complete traversal of the list in O(n) time.
        """
        return f"{self.__class__.__name__}([{', '.join(repr(element) for element in self)}])"
