from typing import TypeVar

from _DoublyLinkedListBase import _DoublyLinkedListBase, Empty

T = TypeVar('T')


class Deque(_DoublyLinkedListBase[T]):
    """
    A double-ended queue implementation using a doubly linked list.

    Supports O(1) operations for adding and removing elements at both ends.
    Inherits the underlying doubly linked list structure from _DoublyLinkedListBase.
    """

    def first(self) -> T:
        """
        Return the element at the front of the deque without removing it.

        Returns:
            The first element in the deque

        Raises:
            Empty: If the deque is empty
        """
        if self.is_empty():
            raise Empty()

        return self._header.next.element

    def last(self) -> T:
        """
        Return the element at the back of the deque without removing it.

        Returns:
            The last element in the deque

        Raises:
            Empty: If the deque is empty
        """
        if self.is_empty():
            raise Empty()

        return self._trailer.prev.element

    def insert_first(self, element: T) -> None:
        """
        Add an element to the front of the deque.

        Args:
            element: The element to add
        """
        self._insert_between(element, self._header, self._header.next)

    def insert_last(self, element: T) -> None:
        """
        Add an element to the back of the deque.

        Args:
            element: The element to add
        """
        self._insert_between(element, self._trailer.prev, self._trailer)

    def delete_first(self) -> T:
        """
        Remove and return the first element from the deque.

        Returns:
            The element removed from the front

        Raises:
            Empty: If the deque is empty
        """
        if self.is_empty():
            raise Empty()

        return self._delete_node(self._header.next)

    def delete_last(self) -> T:
        """
        Remove and return the last element from the deque.

        Returns:
            The element removed from the back

        Raises:
            Empty: If the deque is empty
        """
        if self.is_empty():
            raise Empty()

        return self._delete_node(self._trailer.prev)
