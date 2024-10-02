from Stacks import ArrayStack


def get_precedence(operator: str) -> int:
    """Return precedence of a given operator."""
    precedence = {'*': 2, '/': 2, '+': 1, '-': 1}
    return precedence.get(operator, -1)


def convert_infix_to_postfix(expression: str) -> str:
    """Convert an infix expression to a postfix expression."""
    operator_stack = ArrayStack()  # Stack to hold operators
    operand_stack = ArrayStack()  # Stack to hold output (operands and operators in postfix order)

    for char in expression:
        # Ignore spaces
        if char == ' ':
            continue

        # If character is an operand (variable or digit), push it to operand_stack
        if char.isalnum():  # Checks for alphanumeric characters (variables or numbers)
            operand_stack.push(char)

        # If character is an opening parenthesis, push it to operator_stack
        elif char == '(':
            operator_stack.push(char)

        # If character is a closing parenthesis, pop to operand_stack until '(' is found
        elif char == ')':
            while not operator_stack.is_empty() and operator_stack.top() != '(':
                operand_stack.push(operator_stack.pop())
            operator_stack.pop()  # Remove the '(' from stack

        # If character is an operator, pop from stack based on precedence
        elif char in '+-*/^':
            while not operator_stack.is_empty() and get_precedence(char) <= get_precedence(operator_stack.top()):
                operand_stack.push(operator_stack.pop())
            operator_stack.push(char)

    # Pop all remaining operators to operand_stack
    while not operator_stack.is_empty():
        operand_stack.push(operator_stack.pop())

    # Convert operand_stack to string and reverse it for proper output
    postfix_expression = ''.join([operand_stack.pop() for _ in range(len(operand_stack))])[::-1]

    return postfix_expression


def evaluate_postfix(expression: str):
    """Evaluate a postfix expression."""
    stack = ArrayStack()  # Stack to store operands during evaluation

    for char in expression:
        # If the character is a digit, push it to the stack
        if char.isdigit():
            stack.push(int(char))  # Convert char to int for proper evaluation

        # If the character is an operator, pop the top two operands from the stack, evaluate and push the result
        elif char in '+-*/^':
            operand_2 = stack.pop()
            operand_1 = stack.pop()

            # Evaluate based on the operator and push the result
            if char == '+':
                stack.push(operand_1 + operand_2)
            elif char == '-':
                stack.push(operand_1 - operand_2)
            elif char == '*':
                stack.push(operand_1 * operand_2)
            elif char == '/':
                stack.push(operand_1 / operand_2)  # Perform float division

    # Return the final result from the top of the stack
    return stack.top()
