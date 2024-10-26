from collections.abc import Iterable
from typing import Optional, Iterator, Generic, TypeVar, Union

T = TypeVar('T')  # Generic type for stack elements


class Empty(Exception):
    """
    Exception raised when attempting operations on an empty stack.

    This custom exception provides clear error messaging when trying to
    access or remove elements from an empty stack structure.
    """
    pass


class LinkedStack(Generic[T]):
    """
    A Last-In-First-Out (LIFO) stack implementation using a singly linked list.

    This implementation uses a linked list as the underlying storage structure,
    which allows for O(1) push and pop operations. The stack can hold elements
    of any type and provides type safety through generic type hints.

    Attributes:
        _head: Reference to the top node in the stack
        _size: Number of elements currently in the stack

    Type Parameters:
        T: The type of elements stored in the stack
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

        def __init__(self, element: T, next_node: Optional['LinkedStack.Node'] = None) -> None:
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
        def next(self):
            return self._next

        @property
        def element(self):
            return self._element

    def __init__(self, items: Optional[Union[list, tuple, Iterable[T]]] = None) -> None:
        """
        Initialize a new stack, optionally with initial items.

        Creates an empty stack or a stack pre-populated with elements from
        the provided iterable. If items are provided, they are pushed onto
        the stack in the order they appear in the iterable.

        Args:
            items: Optional sequence of items to initialize the stack with.
                  Can be a list, tuple, or any iterable structure.

        Raises:
            TypeError: If items is provided but is not an iterable type

        Note:
            When initialized with items, the last item in the sequence will
            be at the top of the stack (first to be popped).
        """
        self._head: Optional[LinkedStack.Node] = None
        self._size: int = 0

        if items is not None:
            # Validate that items is iterable
            if not isinstance(items, (list, tuple)) and not isinstance(items, Iterable):
                raise TypeError("Items must be a list, tuple, or iterable")

            # Convert items to list to handle any iterable type
            items_list = list(items)
            for item in items_list:
                self.push(item)

    def __len__(self) -> int:
        """
        Get the current number of elements in the stack.

        Returns:
            int: The number of elements currently in the stack

        Note:
            This method enables the use of the len() function on the stack
            and operates in O(1) time complexity.
        """
        return self._size

    def __iter__(self) -> Iterator[T]:
        """
        Create an iterator over the stack's elements from top to bottom.

        Yields:
            Elements in the stack in LIFO order (top to bottom)

        Note:
            This implementation allows for using the stack in for loops
            and other iterator contexts without modifying the stack.
        """
        current = self._head
        while current is not None:
            yield current.element
            current = current.next

    def __str__(self) -> str:
        """
        Create a string representation of the stack.

        Returns:
            str: A string showing the stack's contents in a list format

        Note:
            Elements are displayed from left to right, where the rightmost
            element represents the top of the stack.
        """
        return f"LinkedStack([{', '.join(str(item) for item in self)}])"

    def __bool__(self) -> bool:
        """
        Check if the stack contains any elements.

        Returns:
            bool: True if the stack has at least one element, False if empty

        Note:
            This method enables using the stack directly in boolean contexts,
            such as if statements.
        """
        return bool(self._size)

    def is_empty(self) -> bool:
        """
        Check if the stack contains no elements.

        Returns:
            bool: True if the stack has no elements, False otherwise

        Note:
            This operation runs in O(1) time complexity.
        """
        return self._size == 0

    def push(self, element: T) -> None:
        """
        Add a new element to the top of the stack.

        This method creates a new node containing the element and places it
        at the top of the stack. The previous top element becomes second.

        Args:
            element: The item to be pushed onto the stack

        Note:
            This operation runs in O(1) time complexity.
        """
        self._head = self.Node(element, self._head)
        self._size += 1

    def push_many(self, items: Union[list, tuple, Iterable[T]]) -> None:
        """
        Push multiple elements onto the stack at once.

        Args:
            items: A sequence of items to push onto the stack.
                  Can be a list, tuple, or any iterable structure.

        Raises:
            TypeError: If items is not an iterable type

        Note:
            Elements are pushed in the order they appear in the iterable,
            so the last element will be at the top of the stack.
        """
        # Validate that items is iterable
        if not isinstance(items, (list, tuple)) and not isinstance(items, Iterable):
            raise TypeError("Items must be a list, tuple, or iterable")

        # Convert items to list to handle any iterable type
        items_list = list(items)
        for item in items_list:
            self.push(item)

    def top(self) -> T:
        """
        Retrieve the element at the top of the stack without removing it.

        Returns:
            The element at the top of the stack

        Raises:
            Empty: If the stack has no elements

        Note:
            This operation runs in O(1) time complexity and does not
            modify the stack's structure.
        """
        if self.is_empty():
            raise Empty("Cannot get top element from empty stack")

        return self._head.element

    def pop(self) -> T:
        """
        Remove and return the element at the top of the stack.

        This method removes the top element from the stack and returns it,
        making the next element the new top of the stack.

        Returns:
            The element that was at the top of the stack

        Raises:
            Empty: If the stack has no elements

        Note:
            This operation runs in O(1) time complexity.
        """
        if self.is_empty():
            raise Empty("Cannot pop from empty stack")

        result = self._head.element
        self._head = self._head.next
        self._size -= 1
        return result

    def pop_many(self, n: int) -> list[T]:
        """
        Remove and return multiple elements from the top of the stack.

        Args:
            n: The number of elements to remove and return

        Returns:
            list: The n top elements from the stack, in order of removal
                 (first element popped is first in the list)

        Raises:
            ValueError: If n is negative or greater than the stack size
            Empty: If the stack is empty

        Note:
            This operation runs in O(n) time complexity where n is the
            number of elements to pop.
        """
        if self.is_empty():
            raise Empty("Cannot pop from empty stack")
        if n > self._size:
            raise ValueError(f"Cannot pop {n} elements from stack of size {self._size}")
        if n < 0:
            raise ValueError("Number of elements to pop must be non-negative")

        result = []
        for _ in range(n):
            result.append(self.pop())

        return result

    def clear(self) -> None:
        """
        Remove all elements from the stack.

        This method resets the stack to its initial empty state by removing
        all elements. The removed elements are left for garbage collection.

        Note:
            This operation runs in O(1) time complexity as it simply
            drops the reference to the head node.
        """
        self._head = None
        self._size = 0

    def copy(self) -> 'LinkedStack[T]':
        """
        Create a new stack with the same elements as this one.

        Returns:
            LinkedStack: A new stack containing copies of all elements
                       in the same order as this stack

        Note:
            This operation runs in O(n) time complexity where n is the
            number of elements in the stack. The new stack contains the
            same elements but is a completely separate structure.
        """
        return LinkedStack(reversed(list(self)))

    def reverse(self) -> None:
        """
        Reverse the order of elements in the stack.

        This method reverses the order of all elements in the stack in-place,
        so that the top element becomes the bottom element and vice versa.

        Note:
            This operation runs in O(n) time complexity where n is the
            number of elements in the stack. The reversal is performed
            by rewiring the links between nodes, not by creating new nodes.
        """
        if self._size <= 1:
            return

        prev = None
        current = self._head
        while current is not None:
            next_node = current.next
            current._next = prev
            prev = current
            current = next_node

        self._head = prev
