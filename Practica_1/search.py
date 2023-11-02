import math

from datastructures import *


# ----------------------------------------------------------------------

class Node:

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

    def expand(self):
        successors = []
        for (newState, action) in self.state.next_states():
            newNode = Node(newState, self, action)
            successors.append(newNode)
        return successors


# ----------------------------------------------------------------------

def uninformed_search(initial_state, goal_state, frontier):
    initial_node = Node(initial_state, None, None)
    explored = []
    expanded = 0
    generated = 0

    frontier.insert(initial_node)

    while True:
        if frontier.is_empty():
            return None
        explored_node = frontier.remove()
        if explored_node.state == goal_state:
            return explored_node, expanded, generated
        explored.append(explored_node.state)
        expanded = expanded + 1
        expand = explored_node.expand()
        for node in expand:
            if node.state not in explored and not frontier.contains(node):
                frontier.insert(node)
                generated += 1

    return None, expanded, generated
# ----------------------------------------------------------------------
# Test functions for uninformed search

def breadth_first(initial_state, goal_state):
    frontier = Queue()  # Indicar estructura de datos adecuada para breadth_first
    return uninformed_search(initial_state, goal_state, frontier)


def depth_first(initial_state, goal_state):
    frontier = Stack()  # Indicar estructura de datos adecuada para depth_first
    return uninformed_search(initial_state, goal_state, frontier)


def uniform_cost(initial_state, goal_state):
    frontier = PriorityQueue(lambda x: x.g)  # Indicar estructura de datos adecuada para uniform_cost
    return uninformed_search(initial_state, goal_state, frontier)


# ----------------------------------------------------------------------

def informed_search(initial_state, goal_state, frontier, heuristic):
    initial_node = Node(initial_state, None, None)
    explored = []
    expanded = 0
    generated = 0

    frontier.insert(initial_node)
    while True:
        if frontier.is_empty():
            return None
        explored_node = frontier.remove()
        if explored_node.state == goal_state:
            return explored_node, expanded, generated
        explored.append(explored_node.state)
        expanded = expanded + 1
        expand = explored_node.expand()
        for node in expand:
            if node.state not in explored and not frontier.contains(node):
                frontier.insert(node) 
                node.h = heuristic(node.state, goal_state)
                generated += 1
    return None, expanded, generated

# ----------------------------------------------------------------------
# Test functions for informed search


def greedy(initial_state, goal_state, heuristic):
    frontier = PriorityQueue(lambda x: x.h)  # Indicar estructura de datos adecuada para greedy
    return informed_search(initial_state, goal_state, frontier, heuristic)


def a_star(initial_state, goal_state, heuristic):
    frontier = PriorityQueue(lambda x: x.g + x.h)  # Indicar estructura de datos adecuada para A*
    return informed_search(initial_state, goal_state, frontier, heuristic)


# ---------------------------------------------------------------------
# Heuristica

#Heuristica 1: Distancia Manhattan -> int distance = Math.abs(x1-x0) + Math.abs(y1-y0)
def h1(current_state, goal_state):
    return abs(current_state.miss[1] - goal_state.miss[1]) + abs(current_state.cann[1] - goal_state.cann[1])

#Heuristica 2: distancia en linea recta hasta el objetivo
def h2(current_state, goal_state):
    aux1 = pow((current_state.miss[1] - goal_state.miss[1]),2)
    aux2 = pow((current_state.cann[1] - goal_state.cann[1]),2)
    return math.sqrt(aux1 + aux2)


# ----------------------------------------------------------------------


def show_solution(node, expanded, generated):
    path = []
    while node is not None:
        path.insert(0, node)
        node = node.parent
    if path:
        print "Solution took %d steps" % (len(path) - 1)
        print path[0].state
        for n in path[1:]:
            print '%s %d %d' % (n.action[0], int(n.action[1]), int(n.action[2]))
            print n.state
    print "Nodes expanded:  %d" % expanded
    print "Nodes generated: %d\n" % generated

