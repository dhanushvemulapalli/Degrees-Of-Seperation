class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

#code for the stack fontier
class StackFrontier():
    def __init__(self):
        self.frontier = []

    #Function for appending a node into the stack fontier
    def add(self, node):
        self.frontier.append(node)

    #Checks id there are any state present in the fontier of the data structure
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    #Checks if the fontier is empty
    def empty(self):
        return len(self.frontier) == 0

    #Removes the last node from the fontier using the empty variable
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
