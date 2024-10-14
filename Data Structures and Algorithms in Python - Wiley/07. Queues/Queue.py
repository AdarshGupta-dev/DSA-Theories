from typing import Any, List


class Empty(Exception):
    """Custom exception to be raised when attempting to access an element from an empty queue."""
    pass


class ArrayQueue:
    """FIFO queue implementation using a Python list as underlying storage."""

    DEFAULT_CAPACITY: int = 10  # Default capacity for new queues

    def __init__(self) -> None:
        """
        Initialize an empty queue with a fixed capacity.
        The queue uses a circular buffer to efficiently handle additions and removals.
        """

        self._data: List[Any] = [None] * ArrayQueue.DEFAULT_CAPACITY  # Queue storage
        self._size: int = 0  # Number of elements in the queue
        self._front: int = 0  # Index of the first element (front of the queue)

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

        # removing element from start of list is computationally heavy.
        # so, replacing it with None and moving pointer to right.
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)  # Circularly shift front
        self._size -= 1
        return answer

    def enqueue(self, element: Any) -> None:
        """
        Add an element to the back of the queue.

        If the queue is full, resize the underlying list to double its current capacity.

        :param element: The element to add to the back of the queue.
        :type element: Any
        """

        # Here list is not shrinking and expanding as we go. We have fixed length.
        # len(self._data) will always give DEFAULT_CAPACITY * n (10, 20, ...) as None are also valid elements of list.
        # self._size is number of valid elements. If both are equal we have a full queue and needs to expand the list.
        if self._size == len(self._data):  # Queue is full
            self._resize(new_capacity=2 * len(self._data))  # Double the array size

        avail = (self._front + self._size) % len(self._data)  # Find the next available index
        self._data[avail] = element
        self._size += 1

    def _resize(self, new_capacity: int) -> None:
        """
        Resize the internal list to a new capacity.

        The elements are realigned so that the front of the queue is at index 0.

        :param new_capacity: The new capacity of the queue.
        :type new_capacity: int
        """

        old_data = self._data  # Keep track of existing list
        self._data = [None] * new_capacity  # Allocate list with the new capacity

        # we are circularly storing data. Front of queue can be at any index.
        walk = self._front
        for k in range(self._size):  # Copy existing elements to the new list
            self._data[k] = old_data[walk]
            walk = (walk + 1) % len(old_data)  # Circularly shift indices

        self._front = 0  # Realign front to 0
