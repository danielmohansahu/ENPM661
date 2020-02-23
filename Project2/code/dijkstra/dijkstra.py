#!/usr/bin/env python3
"""Core class implementing optimal path search via Dijkstra's algorithm.

https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
"""
import numpy as np
from queue import PriorityQueue
from collections import namedtuple

class Dijkstra:
    def __init__(self, obstacle_space=None):
        self.obstacle_space = obstacle_space
        
        # default node constructor (used in our queue)
        self.node = namedtuple("node", ["vert", "dist", "prev"])

    def solve(self, graph, source, target):
        """Find the shortest path from source to target in the
        given graph.

        Args:
            graph:  Directed graph of workspace to explore.
            source: Start vertex (2D point)
            target: End vertex (2D point)
        """
        # construct queue of vertices
        Q = PriorityQueue()

        # initialize algorithm variables
        for vert in graph:
            if vert == source:
                temp_node = self.node(vert, 0, None)
            else:
                temp_node = self.node(vert, np.inf, None)
            Q.put(np.inf, temp_node)

        return Q

    def get_dist(self, src, dest):
        """Calculate the distance / cost between neighbor nodes.
        """
        pass

    def is_obstacle(self, node):
        """Check whether the given node is in the obstacle space.
        """
        pass

    def is_goal(self, node):
        """Check whether the given node is the goal node.
        """
        pass

