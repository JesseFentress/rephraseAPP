class Queue:

    def __init__(self):
        self.list = []

    # Returns true if the list is equivalent to an empty list, false if not
    def is_Empty(self):
        return self.list == []

    # Returns the length of the list
    def size(self):
        return len(self.list)

    # Adds elements to the end of the list (back of the queue)
    def enqueue(self, item):
        self.list.append(item)

    # Removes elements from the first index of the list (front of the queue) as long as the list is not empty
    def dequeue(self):
        if self.is_Empty():
            print("Cannot dequeue an empty queue.")
        else:
            return self.list.pop(0)
