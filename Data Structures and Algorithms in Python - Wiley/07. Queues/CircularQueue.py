from typing import Any, List


class Full(Exception):
    """Custom exception to be raised when attempting to add an element to a full queue."""
    pass


class Empty(Exception):
    """Custom exception to be raised when attempting to access an element from an empty queue."""
    pass


class CircularQueue:
    """Circular queue implementation using a Python list with a fixed capacity."""

    DEFAULT_CAPACITY: int = 10  # Default capacity for new queues

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        """
        Initialize an empty queue with a fixed capacity.
        The queue uses a circular buffer to efficiently handle additions and removals.

        :param capacity: The fixed capacity of the circular queue (default is 10).
        """

        self._data: List[Any] = [None] * capacity  # Queue storage
        self._size: int = 0  # Number of elements in the queue
        self._front: int = 0  # Index of the front element
        self._capacity: int = capacity  # Fixed capacity of the queue

    def __len__(self) -> int:
        """
        Return the number of elements in the queue.

        :returns: The current number of elements in the queue.
        :rtype: int
        """

        return self._size

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        :returns: True if the queue is empty, False otherwise.
        :rtype: bool
        """

        return self._size == 0

    def is_full(self) -> bool:
        """
        Check if the queue is full.

        :returns: True if the queue is full, False otherwise.
        :rtype: bool
        """

        return self._size == self._capacity

    def first(self) -> Any:
        """
        Return (but do not remove) the element at the front of the queue.

        :raises Empty: If the queue is empty.
        :returns: The element at the front of the queue.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Queue is empty")

        return self._data[self._front]

    def dequeue(self) -> Any:
        """
        Remove and return the first element of the queue (FIFO order).

        :raises Empty: If the queue is empty.
        :returns: The element removed from the front of the queue.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Queue is empty")

        answer = self._data[self._front]
        self._data[self._front] = None  # Help garbage collection
        self._front = (self._front + 1) % self._capacity  # Circularly shift front
        self._size -= 1
        return answer

    def enqueue(self, element: Any) -> None:
        """
        Add an element to the back of the queue.

        :param element: The element to add to the back of the queue.
        :type element: Any
        :raises Full: If the queue is full.
        """

        if self.is_full():
            raise Full("Queue is full")

        avail = (self._front + self._size) % self._capacity  # Find the next available index
        self._data[avail] = element
        self._size += 1
