class Stack:

    def __init__(self):
        self.list = []

    # Returns true if the list is equivalent to an empty list, false if not
    def is_Empty(self):
        return self.list == []

    # Returns the length of the list
    def size(self):
        return len(self.list)

    # Adds elements to the end of the list (top of th stack)
    def push(self, item):
        self.list.append(item)

    # Removes elements from the end of the list (top of the stack) as long as the list is not empty
    def pop(self):
        if self.is_Empty():
            print("You cannot pop an empty stack")
        else:
            return self.list.pop()

    # Returns the element at the last index of the list (at the top of the stack)
    def peek(self):
        return self.list[-1]
