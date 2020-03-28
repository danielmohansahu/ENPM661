#!/usr/bin/env python3
"""Core class implementing optimal path search via A*.

https://en.wikipedia.org/wiki/A*_search_algorithm
"""

import time
import numpy as np
from heapq import heappush, heappop
from collections import defaultdict, OrderedDict
from .node import Node
from .graph import Graph

class AStar:
    def __init__(self, graph, src):
        # sanity checks
        if not isinstance(graph, Graph):
            raise TypeError("graph input must be of class graph.Graph")
        if not isinstance(src, Node):
            raise TypeError("src input must be of class node.Node")
        self.graph = graph
        self.src = src
        self.src_hash = hash(src)

        # initialize solution lists
        self._dist = None
        self._prev = None

    def solve(self, goal_node):
        """Find the shortest path from source to target in the
        given graph.
        """
        st = time.time()

        # construct queue of vertices
        Q = []
        
        # construct dicts of distances / predecessors
        #  dist is cost2come
        dist = defaultdict(lambda: np.inf)
        prev = defaultdict(lambda: None)

        # collect visited nodes (for visualization) 
        visited = OrderedDict()
        
        # initialize source node
        dist[self.src_hash] = 0

        # initialize Queue
        for node_hash in self.graph.nodes.keys():
            heappush(Q, (dist[node_hash], node_hash))
      
        # core dijkstra algorithm
        while len(Q) != 0:

            # get the node with the lowest cost2come + cost2go
            u_cost,u = heappop(Q)
            
            # ignore nodes we've already visited (they're invalid)
            if u in visited.keys():
                continue
            
            # mark as visited
            visited[u] = u_cost

            # get all child nodes (and relative cost)
            for v,v_cost in self.graph.tree[u].items():
                # ignore already processed nodes
                if v in visited.keys():
                    continue

                # update the weights of each child node
                alt = dist[u] + v_cost 
                if alt < dist[v]:
                    dist[v] = alt 
                    prev[v] = u
                    + self.graph.nodes[v].cost2go(goal_node)
                    # update value
                    total_cost = dist[v] + self.graph.nodes[v].cost2go(goal_node)
                    heappush(Q,(total_cost,v))

        # set solution to class variables
        self._dist = dist
        self._prev = prev
        self._visited = visited
        print("Took {:.3f}s to solve for optimal path.".format(time.time()-st))
    
    def get_path(self, dst):
        """Get the optimal path and cost to the given destination node.
        """
        # sanity checks
        current_hash = hash(dst)
        if self._dist is None:
            raise RuntimeError("Cannot return optimal path; call `solve` first.")
        if not isinstance(dst, Node):
            raise TypeError("dst input must be of class node.Node")
        if current_hash not in self.graph.nodes.keys():
            raise RuntimeError("Given destination node not found in graph.")

        # backtrack to start node
        path = []
        cost = self._dist[current_hash]
        while current_hash in self._prev.keys():
            path.append(current_hash)
            current_hash = self._prev[current_hash]
        path.append(self.src_hash)

        # reverse to give path from start to goal
        path.reverse()

        # actually return the node elements (more interesting)
        path = [self.graph.nodes[p] for p in path] 

        return path,cost 

    def get_exploration(self, stop_on_goal=False, dst=None):
        """Returns all the nodes that we explored (in order)
        
        Args:
            stop_on_goal: Bool determining whether to return only up to the goal node.
        """
        # sanity check
        if self._visited is None:
            raise RuntimeError("Cannot return explored nodes; call `solve` first.")
        if stop_on_goal and dst is None:
            raise RuntimeError("If stop_on_goal is True a goal node must be provided.")

        explored_nodes = []
        explored_costs = []
        for hash_, cost in self._visited.items():
            explored_nodes.append(self.graph.nodes[hash_])
            explored_costs.append(cost)

            if stop_on_goal and self.graph.nodes[hash_]==dst:
                break

        return explored_nodes, explored_costs
            

        

