from typing import Optional, Generic, TypeVar, Iterator

T = TypeVar('T')


class Empty(Exception):
    """
    Exception raised when attempting operations on an empty list.
    """

    def __init__(self) -> None:
        super().__init__("Cannot perform operation on empty list")


class _DoublyLinkedListBase(Generic[T]):
    """
    Base class for doubly linked list data structure implementation.

    Provides a memory-efficient implementation with O(1) insertions and deletions
    at both ends. Uses sentinel nodes (header and trailer) to simplify boundary
    conditions.
    """

    class _Node:
        __slots__ = '_element', '_next', '_prev'

        def __init__(self, element: Optional[T], prev_node: Optional['_DoublyLinkedListBase._Node'] = None, next_node: Optional['_DoublyLinkedListBase._Node'] = None) -> None:
            """
            Create a new node with given element and optional links.
            """
            self._element = element
            self._prev = prev_node
            self._next = next_node

        @property
        def element(self) -> Optional[T]:
            """
            Return the element stored in this node.
            """
            return self._element

        @property
        def next(self) -> Optional['_DoublyLinkedListBase._Node']:
            """
            Return the next node reference.
            """
            return self._next

        @property
        def prev(self) -> Optional['_DoublyLinkedListBase._Node']:
            """
            Return the previous node reference.
            """
            return self._prev

        def invalidate(self) -> None:
            """
            Invalidate node references to help garbage collection.
            """
            self._prev = None
            self._next = None
            self._element = None

    def __init__(self) -> None:
        """
        Initialize an empty list with sentinel nodes.
        """
        self._header = self._Node(None)
        self._trailer = self._Node(None)

        self._header._next = self._trailer
        self._trailer._prev = self._header

        self._size = 0

    def __len__(self) -> int:
        """
        Return the number of elements in the list.
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Return True if the list is empty.
        """
        return self._size == 0

    def _insert_between(self, element: T, predecessor: '_Node', successor: '_Node') -> '_Node':
        """
        Insert a new node containing element between two existing nodes.

        Args:
            element: The element to insert
            predecessor: Node that should precede the new node
            successor: Node that should follow the new node

        Returns:
            The newly created node
        """
        newest = self._Node(element, predecessor, successor)

        predecessor._next = newest
        successor._prev = newest

        self._size += 1
        return newest

    def _delete_node(self, node: '_Node') -> T:
        """
        Remove a node from the list and return its element.

        Args:
            node: The node to delete

        Returns:
            The element that was stored in the deleted node

        Raises:
            Empty: If attempting to delete from an empty list
        """
        if self.is_empty():
            raise Empty()

        predecessor = node.prev
        successor = node.next

        predecessor._next = successor
        successor._prev = predecessor

        self._size -= 1
        element = node.element

        node.invalidate()
        return element

    def __iter__(self) -> Iterator[T]:
        """
        Return an iterator over the elements in the list.
        """
        cursor = self._header.next

        while cursor is not self._trailer:
            yield cursor.element
            cursor = cursor.next
