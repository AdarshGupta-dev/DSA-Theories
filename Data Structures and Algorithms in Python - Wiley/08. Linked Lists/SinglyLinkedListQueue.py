from collections.abc import Iterable
from typing import Optional, Iterator, Generic, TypeVar, Union

T = TypeVar('T')  # Generic type for queue elements


class Empty(Exception):
    """
    Exception raised when attempting operations on an empty queue.

    This custom exception provides clear error messaging when trying to
    access or remove elements from an empty queue structure.
    """
    pass


class LinkedQueue(Generic[T]):
    """
    A First-In-First-Out (FIFO) queue implementation using a singly linked list.

    This implementation uses a linked list as the underlying storage structure,
    which allows for O(1) enqueue and dequeue operations. The queue can hold
    elements of any type and provides type safety through generic type hints.

    Attributes:
        _head: Reference to the front node in the queue (where elements are dequeued)
        _tail: Reference to the back node in the queue (where elements are enqueued)
        _size: Number of elements currently in the queue

    Type Parameters:
        T: The type of elements stored in the queue
    """

    class Node:
        """
        A private node class for the linked list implementation.

        This lightweight class represents a single node in the linked list,
        storing both the element and a reference to the next node. It uses
        __slots__ to optimize memory usage.

        Attributes:
            _element: The data stored in this node
            _next: Reference to the next node in the list
        """
        __slots__ = '_element', '_next'

        def __init__(self, element: T, next_node: Optional['LinkedQueue.Node'] = None) -> None:
            """
            Initialize a new node in the linked list.

            Args:
                element: The data to be stored in this node
                next_node: Reference to the next node in the sequence,
                          defaults to None for the end of the list

            Note:
                The node is initially created with the given element and an
                optional link to the next node. If no next node is specified,
                this node is assumed to be the end of the sequence.
            """
            self._element = element
            self._next = next_node

        @property
        def element(self) -> T:
            """
            Get the element stored in this node.

            Returns:
                The element stored in the node
            """
            return self._element

        @property
        def next(self) -> Optional['LinkedQueue.Node']:
            """
            Get the reference to the next node.

            Returns:
                Reference to the next node in the sequence
            """
            return self._next

    def __init__(self, items: Optional[Union[list, tuple, Iterable[T]]] = None) -> None:
        """
        Initialize a new queue, optionally with initial items.

        Creates an empty queue or a queue pre-populated with elements from
        the provided iterable. If items are provided, they are added to
        the queue in the order they appear in the iterable.

        Args:
            items: Optional sequence of items to initialize the queue with.
                  Can be a list, tuple, or any iterable structure.

        Raises:
            TypeError: If items is provided but is not an iterable type

        Note:
            When initialized with items, the first item in the sequence will
            be at the front of the queue (first to be dequeued).
        """
        self._head: Optional[LinkedQueue.Node] = None
        self._tail: Optional[LinkedQueue.Node] = None
        self._size: int = 0

        if items is not None:
            if not isinstance(items, (list, tuple)) and not isinstance(items, Iterable):
                raise TypeError("Items must be a list, tuple, or iterable")

            items_list = list(items)
            for item in items_list:
                self.enqueue(item)

    def enqueue(self, element: T) -> None:
        """
        Add a new element to the back of the queue.

        This method creates a new node containing the element and places it
        at the back of the queue.

        Args:
            element: The item to be added to the queue

        Note:
            This operation runs in O(1) time complexity.
        """
        newest = self.Node(element)

        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest

        self._tail = newest
        self._size += 1

    def dequeue(self) -> T:
        """
        Remove and return the element at the front of the queue.

        Returns:
            The element that was at the front of the queue

        Raises:
            Empty: If the queue is empty

        Note:
            This operation runs in O(1) time complexity.
        """
        if self.is_empty():
            raise Empty("Cannot dequeue from empty queue")

        result = self._head.element
        self._head = self._head.next
        self._size -= 1

        if self.is_empty():  # Queue is now empty
            self._tail = None

        return result

    def first(self) -> T:
        """
        Retrieve the element at the front of the queue without removing it.

        Returns:
            The element at the front of the queue

        Raises:
            Empty: If the queue is empty

        Note:
            This operation runs in O(1) time complexity.
        """
        if self.is_empty():
            raise Empty("Queue is empty")

        return self._head.element

    def last(self) -> T:
        """
        Retrieve the element at the back of the queue without removing it.

        Returns:
            The element at the back of the queue

        Raises:
            Empty: If the queue is empty

        Note:
            This operation runs in O(1) time complexity.
        """
        if self.is_empty():
            raise Empty("Queue is empty")

        return self._tail.element

    def enqueue_many(self, items: Union[list, tuple, Iterable[T]]) -> None:
        """
        Add multiple elements to the queue at once.

        Args:
            items: A sequence of items to add to the queue.
                  Can be a list, tuple, or any iterable structure.

        Raises:
            TypeError: If items is not an iterable type

        Note:
            Elements are added in the order they appear in the iterable.
        """
        if not isinstance(items, (list, tuple)) and not isinstance(items, Iterable):
            raise TypeError("Items must be a list, tuple, or iterable")

        for item in items:
            self.enqueue(item)

    def dequeue_many(self, n: int) -> list[T]:
        """
        Remove and return multiple elements from the front of the queue.

        Args:
            n: The number of elements to remove and return

        Returns:
            list: The n front elements from the queue, in order of removal

        Raises:
            ValueError: If n is negative or greater than the queue size
            Empty: If the queue is empty

        Note:
            This operation runs in O(n) time complexity.
        """
        if self.is_empty():
            raise Empty("Cannot dequeue from empty queue")
        if n > self._size:
            raise ValueError(f"Cannot dequeue {n} elements from queue of size {self._size}")
        if n < 0:
            raise ValueError("Number of elements to dequeue must be non-negative")

        result = []
        for _ in range(n):
            result.append(self.dequeue())
        return result

    def reverse(self) -> None:
        """
        Reverse the order of elements in the queue.

        This method reverses the order of all elements in the queue in-place,
        making the front element the back element and vice versa.

        Note:
            This operation runs in O(n) time complexity where n is the
            number of elements in the queue.
        """
        if self._size <= 1:
            return

        # Convert to a list, reverse it, and rebuild the queue
        items = list(self)
        self.clear()

        for item in reversed(items):
            self.enqueue(item)

    def clear(self) -> None:
        """
        Remove all elements from the queue.

        This method resets the queue to its initial empty state by removing
        all elements. The removed elements are left for garbage collection.

        Note:
            This operation runs in O(1) time complexity.
        """
        self._head = None
        self._tail = None
        self._size = 0

    def copy(self) -> 'LinkedQueue[T]':
        """
        Create a new queue with the same elements as this one.

        Returns:
            LinkedQueue: A new queue containing copies of all elements
                       in the same order as this queue

        Note:
            This operation runs in O(n) time complexity where n is the
            number of elements in the queue.
        """
        return LinkedQueue(list(self))

    def __len__(self) -> int:
        """
        Get the current number of elements in the queue.

        Returns:
            The number of elements currently in the queue

        Note:
            This operation runs in O(1) time complexity.
        """
        return self._size

    def __iter__(self) -> Iterator[T]:
        """
        Create an iterator over the queue's elements from front to back.

        Returns:
            Iterator yielding queue elements in FIFO order (front to back)
        """
        current = self._head
        while current is not None:
            yield current.element
            current = current.next

    def __str__(self) -> str:
        """
        Create a string representation of the queue.

        Returns:
            A string showing the queue's contents in a list format

        Note:
            Elements are displayed from left (front) to right (back).
        """
        return f"LinkedQueue([{', '.join(str(item) for item in self)}])"

    def __bool__(self) -> bool:
        """
        Check if the queue contains any elements.

        Returns:
            True if the queue has at least one element, False if empty
        """
        return bool(self._size)

    def is_empty(self) -> bool:
        """
        Check if the queue contains no elements.

        Returns:
            True if the queue has no elements, False otherwise

        Note:
            This operation runs in O(1) time complexity.
        """
        return self._size == 0
