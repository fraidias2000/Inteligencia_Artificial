import math

#----------------------------------------------------------------------

class PriorityQueue:
    """
    This is a heap implementation of a priority queue.  The insert and
    remove operations each take O(log n) time.  To create a new priority
    queue, call the constructor with a function that maps queue elements
    to cost values.  Interface methods:
       q.is_empty() returns True if q is empty
       q.insert(x) inserts x into q according to the cost of x
       q.remove() removes and returns the lowest-cost element from q
       q.contains(x) determines if x is contained in q

    Example:
       q = PriorityQueue(lambda x: x)
       q.insert(5)
       q.insert(1)
       q.insert(3)
       q.insert(8)
       q.insert(2)
       print q.remove()  ==>  1
       print q.remove()  ==>  2
       print q.remove()  ==>  3
       print q.remove()  ==>  5
       print q.remove()  ==>  8
       print q.remove()  ==>  None

    """
    # costFunction is a function that maps queue elements to cost values
    def __init__(self, costFunction):
        # current number of elements in queue
        self.size = 0
        # current maximum size of queue (can be changed - see insert below)
        self.limit = 10
        # the elements themselves (position 0 is not used)
        self.contents = [None] * (self.limit + 1)
        # a function that returns the cost of the element at position i
        self.cost = lambda i: costFunction(self.contents[i])
        
    def contains(self, elem):
        return elem in self.contents
        
    def is_empty(self):
        # returns True if the queue is empty, or else False
        return self.size == 0

    def is_root(self, i):
        # returns True if element i is the root of the heap
        return i == 1
    
    def is_leaf(self, i):
        # returns True if element i is a leaf
        return self.left(i) == None and self.right(i) == None

    def parent(self, i):
        # returns the position of the parent of element i
        return i / 2

    def left(self, i):
        # returns the position of the left child of element i
        child = i * 2
        if child > self.size:
            return None
        else:
            return child

    def right(self, i):
        # returns the position of the right child of element i
        child = i * 2 + 1
        if child > self.size:
            return None
        else:
            return child

    def smallestChild(self, i):
        # returns the position of the smallest child of element i
        leftChild = self.left(i)
        rightChild = self.right(i)
        if leftChild == None:
            return rightChild
        elif rightChild == None:
            return leftChild
        elif self.cost(leftChild) < self.cost(rightChild):
            return leftChild
        else:
            return rightChild

    def swap(self, i, j):
        # swaps elements in positions i and j (using parallel assignment)
        self.contents[i], self.contents[j] = self.contents[j], self.contents[i]

    def insert(self, new):
        # inserts a new element into the heap
        if self.size == self.limit:
            # this doubles the amount of space available in self.contents
            self.contents.extend([None] * self.size)
            self.limit += self.size
        self.size += 1
        self.contents[self.size] = new
        # push new element up toward the root as far as possible
        current = self.size
        while not self.is_root(current):
            parent = self.parent(current)
            if self.cost(current) >= self.cost(parent):
                return
            self.swap(current, parent)
            current = parent

    def remove(self):
        # deletes the current element at the root of the heap and returns it
        if self.size == 0:
            return None
        else:
            min_val = self.contents[1]
            self.contents[1] = self.contents[self.size]
            self.size -= 1
            # push new root element down into the heap as far as possible
            current = 1
            while not self.is_leaf(current):
                child = self.smallestChild(current)
                if self.cost(current) <= self.cost(child):
                    return min_val
                self.swap(current, child)
                current = child
            return min_val

#----------------------------------------------------------------------

class Node:
    """
    This class is used to represent nodes of the search tree.  Each
    node contains a state representation, a reference to the node's
    parent node, a string that describes the action that generated
    the node's state from the parent state, the path cost g from
    the start node to this node, and the estimated path cost h
    from this node to the goal node.
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        if other:
            return self.state == other.state
        else:
            return False
    
    def expand(self, valid):
        successors = []
        x, y = self.state
        actions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        for action in actions:
            dif_x, dif_y = actions[action]
            new_state = (x + dif_x, y + dif_y)
            if new_state in valid:
                new_node = Node(new_state, self, action)
                successors.append(new_node)
        return successors

#----------------------------------------------------------------------

def informed_search(initial_state, goal_state, visited, frontier, heuristic):

    initial_node = Node(initial_state, None, None)
    expanded = 0
    generated = 0
    
    frontier.insert(initial_node)  # initialize the frontier using the initial state of problem
    explored_states = []           # initialize the explored set to be empty
    valid_states = list(visited) + [goal_state]

    # loop do
    while not frontier.is_empty():
        leaf = frontier.remove()   # choose a leaf node and remove it from the frontier
        
        # states must have an __eq__ method defined to test equality
        if leaf.state == goal_state:   # if the node contains a goal state 
            return (leaf, expanded, generated)   # then return the corresponding solution

        explored_states.append(leaf.state)   # add the node to the explored set
        expanded = expanded + 1
        for successor in leaf.expand(valid_states):   # expand the chosen node, adding the resulting nodes to the frontier
            # only if not in the frontier or explored set
            if successor.state not in explored_states and not frontier.contains(successor):
                # set path cost of successor
                successor.g = leaf.g + 1
                successor.h = heuristic(successor.state, goal_state)
                frontier.insert(successor)
                generated = generated + 1
    
    # if the frontier is empty then return failure
    return (None, expanded, generated)

#----------------------------------------------------------------------
# Test functions for informed search

def h_distance(current_state, goal_state):
    """
    Rellenar con el codigo necesario que calcule la distancia euclidea entre el
    estado actual y el objetivo, sabiendo que ambos se representan como tuplas (x,y)
    """
    aux1 = pow((current_state.x - goal_state.x),2)
    aux2 = pow((current_state.y - goal_state.y),2)
    return math.sqrt(aux1 + aux2)


def a_star(initial_state, goal_state, visited, heuristic=h_distance):
    frontier = PriorityQueue(lambda node: node.g + node.h)
    result = informed_search(initial_state, goal_state, visited, frontier, heuristic) 
    return steps(result[0])

def steps(node):
    path = []
    while node.parent != None:
        path.append(node.action)
        node = node.parent
    return path


