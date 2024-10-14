from typing import Any, List


class Empty(Exception):
    """Custom exception raised when attempting to access an element from an empty deque."""
    pass


class ArrayDeque:
    """Double-ended queue implementation using a Python list as underlying storage."""

    DEFAULT_CAPACITY: int = 10  # Default capacity for new deque

    def __init__(self) -> None:
        """
        Initialize an empty deque with a fixed capacity.
        The deque uses a circular buffer to efficiently handle additions and removals.
        """
        self._data: List[Any] = [None] * ArrayDeque.DEFAULT_CAPACITY  # Deque storage
        self._size: int = 0  # Number of elements in the deque
        self._front: int = 0  # Index of the first element (front of the deque)
        self._last: int = -1  # Index of the last element (end of the deque)

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
        Return (but do not remove) the element at the end of the deque.

        :raises Empty: If the deque is empty.
        :returns: The element at the end of the deque.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Deque is empty")
        return self._data[self._last]

    def add_first(self, element: Any) -> None:
        """
        Add an element to the front of the deque.

        If the deque is full, resize the underlying list to double its current capacity.

        :param element: The element to add to the front of the deque.
        :type element: Any
        """

        if self._size == len(self._data):  # Deque is full
            self._resize(2 * len(self._data))  # Double the array size

        # Wrap the front to the end if it reaches the start
        self._front = (self._front - 1) % len(self._data)
        self._data[self._front] = element
        self._size += 1

        if self._last == -1:  # If it was empty, update last index
            self._last = self._front

    def add_last(self, element: Any) -> None:
        """
        Add an element to the back of the deque.

        If the deque is full, resize the underlying list to double its current capacity.

        :param element: The element to add to the back of the deque.
        :type element: Any
        """

        if self._size == len(self._data):  # Deque is full
            self._resize(2 * len(self._data))  # Double the array size

        # Move last pointer circularly
        self._last = (self._last + 1) % len(self._data)
        self._data[self._last] = element
        self._size += 1

    def delete_first(self) -> Any:
        """
        Remove and return the first element of the deque.

        :raises Empty: If the deque is empty.
        :returns: The element removed from the front of the deque.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Deque is empty")

        answer = self._data[self._front]
        self._data[self._front] = None  # Help garbage collection
        self._front = (self._front + 1) % len(self._data)  # Move front forward circularly
        self._size -= 1

        if self.is_empty():  # Reset pointers if the deque becomes empty
            self._front, self._last = 0, -1

        return answer

    def delete_last(self) -> Any:
        """
        Remove and return the last element of the deque.

        :raises Empty: If the deque is empty.
        :returns: The element removed from the end of the deque.
        :rtype: Any
        """

        if self.is_empty():
            raise Empty("Deque is empty")

        answer = self._data[self._last]
        self._data[self._last] = None  # Help garbage collection
        self._last = (self._last - 1) % len(self._data)  # Move last backward circularly
        self._size -= 1

        if self.is_empty():  # Reset pointers if the deque becomes empty
            self._front, self._last = 0, -1

        return answer

    def _resize(self, new_capacity: int) -> None:
        """
        Resize the internal list to a new capacity.

        The elements are realigned so that the front of the deque is at index 0.

        :param new_capacity: The new capacity of the deque.
        :type new_capacity: int
        """

        old_data = self._data  # Keep track of existing list
        self._data = [None] * new_capacity  # Allocate list with the new capacity

        # Realign elements from front to last in the new list
        walk = self._front
        for k in range(self._size):
            self._data[k] = old_data[walk]
            walk = (walk + 1) % len(old_data)

        self._front = 0  # Reset front
        self._last = self._size - 1  # Reset last index
