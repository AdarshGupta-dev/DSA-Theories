from collections.abc import Iterable
from typing import Optional, Iterator, Generic, TypeVar, Union, Any

T = TypeVar('T')  # Generic type for queue elements


class Empty(Exception):
    """
    Exception raised when attempting operations on an empty queue.

    This exception is raised when trying to access or remove elements from
    an empty queue, providing clear error handling for queue operations.

    Example:
        >>> queue = LinkedListCircularQueue()
        >>> try:
        ...     item = queue.dequeue()
        ... except Empty:
        ...     print("Queue is empty!")
    """
    pass


class LinkedListCircularQueue(Generic[T]):
    """
    A circular First-In-First-Out (FIFO) queue implementation using a singly linked list.

    This implementation maintains a circular linked structure where the tail node
    points back to the head node, providing efficient O(1) operations for both
    enqueue and dequeue operations. The circular nature allows for efficient
    traversal and manipulation of elements.

    Key Features:
        - O(1) enqueue and dequeue operations
        - Circular structure for efficient traversal
        - Generic type support for type safety
        - Memory-efficient node implementation using __slots__
        - Support for iteration and common container operations

    Attributes:
        _tail: Reference to the back node in the queue (where elements are enqueued)
        _size: Number of elements currently in the queue

    Type Parameters:
        T: The type of elements stored in the queue

    Example:
        >>> queue = LinkedListCircularQueue[int]()
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> queue.dequeue()
        1
        >>> len(queue)
        1
    """

    class Node:
        """
        A private node class for the circular linked list implementation.

        This class represents a single node in the circular linked structure,
        storing both the element and a reference to the next node. It uses
        __slots__ for memory optimization and provides read-only access to
        its properties.

        Attributes:
            _element: The data stored in this node
            _next: Reference to the next node in the circular list

        Note:
            The Node class is implemented with __slots__ to reduce the memory
            footprint of each node instance.
        """
        __slots__ = '_element', '_next'

        def __init__(self, element: T, next_node: Optional['LinkedListCircularQueue.Node'] = None) -> None:
            """
            Initialize a new node in the circular linked list.

            Args:
                element: The data to be stored in this node
                next_node: Reference to the next node in the sequence,
                          defaults to None for the end of the list
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
        def next(self) -> Optional['LinkedListCircularQueue.Node']:
            """
            Get the reference to the next node.

            Returns:
                Reference to the next node in the sequence
            """
            return self._next

    # Core Queue Operations
    def __init__(self, items: Optional[Union[list[T], tuple[T, ...], Iterable[T]]] = None) -> None:
        """
        Initialize a new circular queue, optionally with initial items.

        Args:
            items: Optional sequence of items to initialize the queue with.
                  Can be a list, tuple, or any iterable structure.

        Raises:
            TypeError: If items is provided but is not an iterable type
        """
        self._tail: Optional[LinkedListCircularQueue.Node] = None
        self._size: int = 0

        if items is not None:
            if not isinstance(items, (list, tuple)) and not isinstance(items, Iterable):
                raise TypeError("Items must be a list, tuple, or iterable")

            for item in items:
                self.enqueue(item)

    def is_empty(self) -> bool:
        """
        Check if the queue contains no elements.

        Returns:
            True if the queue has no elements, False otherwise

        Note:
            This operation runs in O(1) time complexity.
        """
        return self._size == 0

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

        return self._tail.next.element

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

    def enqueue(self, element: T) -> None:
        """
        Add a new element to the back of the queue.

        This method maintains the circular structure by properly linking
        the new node into the existing circle of nodes.

        Args:
            element: The item to be added to the queue

        Time Complexity: O(1)
        """
        newest = self.Node(element)

        if self.is_empty():
            newest._next = newest  # Point to itself in empty queue
        else:
            newest._next = self._tail.next  # Link to head
            self._tail._next = newest  # Update current tail's next

        self._tail = newest  # Update tail reference
        self._size += 1

    def dequeue(self) -> T:
        """
        Remove and return the element at the front of the queue.

        This method maintains the circular structure when removing the
        front element by properly updating the necessary links.

        Returns:
            The element that was at the front of the queue

        Raises:
            Empty: If the queue is empty

        Time Complexity: O(1)
        """
        if self.is_empty():
            raise Empty("Cannot dequeue from empty queue")

        old_head = self._tail.next
        result = old_head.element

        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = old_head.next  # Skip the old head

        self._size -= 1
        return result

    # Batch Operations
    def enqueue_many(self, items: Union[list, tuple, Iterable[T]]) -> None:
        """
        Add multiple elements to the queue at once.

        Args:
            items: A sequence of items to add to the queue.
                  Can be a list, tuple, or any iterable structure.

        Raises:
            TypeError: If items is not an iterable type
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

    # Queue Manipulation Operations
    def rotate(self) -> None:
        """
        Rotate the queue one position, moving the front element to the back.

        This operation effectively makes the second element become the first
        while making the first element become the last.

        Time Complexity: O(1)
        """
        if self._size > 1:
            self._tail = self._tail.next

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
        self._tail = None
        self._size = 0

    def copy(self) -> 'LinkedListCircularQueue[T]':
        """
        Create a new queue with the same elements as this one.

        Returns:
            LinkedListCircularQueue: A new queue containing copies of all elements
                       in the same order as this queue

        Note:
            This operation runs in O(n) time complexity where n is the
            number of elements in the queue.
        """
        return LinkedListCircularQueue(list(self))

    # Magic Methods
    def __len__(self) -> int:
        """
        Get the current number of elements in the queue.

        Returns:
            The number of elements currently in the queue

        Note:
            This operation runs in O(1) time complexity.
        """
        return self._size

    def __bool__(self) -> bool:
        """
        Check if the queue contains any elements.

        Returns:
            True if the queue has at least one element, False if empty
        """
        return bool(self._size)

    def __eq__(self, other: Any) -> bool:
        """
        Compare this queue with another for equality.

        Two queues are considered equal if they have the same elements
        in the same order.

        Args:
            other: Another queue to compare with

        Returns:
            bool: True if the queues are equal, False otherwise
        """
        if not isinstance(other, LinkedListCircularQueue):
            return NotImplemented

        if len(self) != len(other):
            return False

        return all(a == b for a, b in zip(self, other))

    def __iter__(self) -> Iterator[T]:
        """
        Create an iterator over the queue's elements from front to back.

        Returns:
            Iterator yielding queue elements in FIFO order (front to back)
        """
        if self.is_empty():
            return

        current = self._tail.next
        while True:
            yield current.element
            if current is self._tail:
                break

            current = current.next

    def __str__(self) -> str:
        """
        Create a string representation of the queue.

        Returns:
            A string showing the queue's contents in a list format
        """
        return f"LinkedQueue([{', '.join(str(item) for item in self)}])"
