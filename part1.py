import numpy as np
import heapq

goal_state = ["AEDCA", "BEACD", "BABCE", "DADBD", "BECBD"]

factory_dist = np.array([[   0, 1064,  673, 1401, 277],
                         [1064,    0,  958, 1934, 337],
                         [ 673,  958,    0, 1001, 399],
                         [1401, 1934, 1001,    0, 387],
                         [ 277,  337,  399,  387,   0]])
class State:
    def __init__(self, factory, goal_state, parent):
        if parent is None:
            self.ws = ["", "", "", "", ""]
            self.cost = 0
            self.factory = factory
        else:
            self.ws = new_ws(parent.ws, factory)
            self.cost = parent.cost + distance(parent.factory, factory)
            self.factory = factory

def new_ws(ws, factor):

def translate(c):
    if c == "A":
        return 0
    if c == "B":
        return 1
    if c == "C":
        return 2
    if c == "D":
        return 3
    if c == "E":
        return 4

    return -1

def distance(a, b):
    x = translate(a)
    y = translate(b)

    return factory_dist[x][y]

def total_distance(widgets):
    dist = [0, 0, 0, 0, 0]
    count = 0
    for w in widgets:
        for i in range(len(w) - 1):
            dist[count] += distance(w[i], w[i+1])
        count += 1

    print dist

def distance_heuristic(state):
    for s in state:
        for g in goal_state:
            dif = len(g) - len(s)


def ayyy():
    start = ["", "", "", "", "", 0, ""]                                         # Last element keeps track of path cost
    dist =  [ 0,  0,  0,  0,  0]

    frontier = []
    front2 = set([])

    heapq.heappush(frontier, (distance_heuristic(start), start))
    front2.add(state)

    while len(frontier) > 0:
        state = heapq.heappop(frontier)
        
        if state[:5] == goal_state:
            # we're done do stuf
            # TODO
            return
