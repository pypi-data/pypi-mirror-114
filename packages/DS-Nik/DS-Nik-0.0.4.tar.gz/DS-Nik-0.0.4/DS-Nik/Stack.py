class Stack:
    def __init__(self):
        self.data = []
        self.top = -1

    def is_empty(self):
        return self.top == -1

    def push(self, data):
        self.top = self.top + 1
        self.data.append(data)

    def pop(self):
        if self.top == -1:
            return
        
        popped_item = self.data[-1]
        self.data = self.data[:-1]
        return popped_item