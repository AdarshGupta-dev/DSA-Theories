from typing import Any, List


class Full(Exception):
    """Custom exception to be raised when attempting to add an element to a full deque."""
    pass


class Empty(Exception):
    """Custom exception to be raised when attempting to access an element from an empty deque."""
    pass


class CircularDeque:
    """Double-ended circular queue implementation using a Python list with fixed capacity."""

    DEFAULT_CAPACITY: int = 10  # Default capacity for new deque

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        """
        Initialize an empty deque with a fixed capacity.
        The deque uses a circular buffer to efficiently handle additions and removals from both ends.

        :param capacity: The fixed capacity of the circular deque (default is 10).
        """

        self._data: List[Any] = [None] * capacity  # Deque storage
        self._size: int = 0  # Number of elements in the deque
        self._front: int = 0  # Index of the front element
        self._capacity: int = capacity  # Fixed capacity of the deque

    def __len__(self) -> int:
        """
        Return the number of elements in the deque.

        :returns: The current number of elements in the deque.
        :rtype: int
        """

        return self._size

    def is_empty(self) -> bool:
        """
        Check if the deque is empty.

        :returns: True if the deque is empty, False otherwise.
        :rtype: bool
        """

        return self._size == 0

    def is_full(self) -> bool:
        """
        Check if the deque is full.

        :returns: True if the deque is full, False otherwise.
        :rtype: bool
        """

        return self._size == self._capacity

    def first(self) -> Any:
        """
        Return (but do not remove) the element at the front of the deque.

        :raises Empty: If the deque is empty.
        :returns: The element at the front of the deque.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Deque is empty")

        return self._data[self._front]

    def last(self) -> Any:
        """
        Return (but do not remove) the element at the rear of the deque.

        :raises Empty: If the deque is empty.
        :returns: The element at the rear of the deque.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Deque is empty")

        rear = (self._front + self._size - 1) % self._capacity
        return self._data[rear]

    def enqueue_first(self, element: Any) -> None:
        """
        Add an element to the front of the deque.

        :param element: The element to add to the front of the deque.
        :type element: Any
        :raises Full: If the deque is full.
        """

        if self.is_full():
            raise Full("Deque is full")

        self._front = (self._front - 1) % self._capacity  # Circularly shift front left
        self._data[self._front] = element
        self._size += 1

    def enqueue_last(self, element: Any) -> None:
        """
        Add an element to the rear of the deque.

        :param element: The element to add to the rear of the deque.
        :type element: Any
        :raises Full: If the deque is full.
        """

        if self.is_full():
            raise Full("Deque is full")

        avail = (self._front + self._size) % self._capacity  # Find the next available index
        self._data[avail] = element
        self._size += 1

    def dequeue_first(self) -> Any:
        """
        Remove and return the element from the front of the deque.

        :raises Empty: If the deque is empty.
        :returns: The element removed from the front of the deque.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Deque is empty")

        answer = self._data[self._front]
        self._data[self._front] = None  # Help garbage collection
        self._front = (self._front + 1) % self._capacity  # Circularly shift front right
        self._size -= 1
        return answer

    def dequeue_last(self) -> Any:
        """
        Remove and return the element from the rear of the deque.

        :raises Empty: If the deque is empty.
        :returns: The element removed from the rear of the deque.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Deque is empty")

        rear = (self._front + self._size - 1) % self._capacity
        answer = self._data[rear]
        self._data[rear] = None  # Help garbage collection
        self._size -= 1
        return answer
