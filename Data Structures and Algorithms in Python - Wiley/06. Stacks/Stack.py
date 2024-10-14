class EmptyStack(Exception):
    """Custom exception to indicate that the stack is empty."""
    pass


class ArrayStack:
    def __init__(self) -> None:
        """
        Initialize an empty stack using a list.
        """
        self._data = []

    def __len__(self) -> int:
        """
        Return the number of elements in the stack.
        """
        return len(self._data)

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

        :return: True if the stack is empty, False otherwise.
        """
        return len(self._data) == 0

    def push(self, element) -> None:
        """
        Add an element to the top of the stack.

        :param element: The element to be added to the stack.
        """
        self._data.append(element)

    def top(self):
        """
        Return the top element of the stack without removing it.

        :return: The top element of the stack.
        :raises EmptyStack: If the stack is empty.
        """
        if self.is_empty():
            raise EmptyStack("Stack is empty.")
        return self._data[-1]

    def pop(self):
        """
        Remove and return the top element of the stack.

        :return: The top element of the stack.
        :raises EmptyStack: If the stack is empty.
        """
        if self.is_empty():
            raise EmptyStack("Stack is empty.")
        return self._data.pop()

    def __str__(self) -> str:
        """
        Return a string representation of the stack for printing.

        :return: String representation of the stack.
        """
        return f"Stack: {self._data}"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the stack for debugging.

        :return: Detailed string representation of the stack.
        """
        return f"ArrayStack({self._data})"
