#!/usr/bin/env python3

import sys
import numpy as np
from dijkstra.node import Node
from dijkstra.map import Map
from dijkstra.graph import Graph
from dijkstra.dijkstra import Dijkstra

if __name__ == "__main__":

    # start node
    start_node = Node(np.array([19,33]))

    # dummy map (for testing)
    obstacle_map = Map(xbounds=[0,300],ybounds=[0,200])

    # generate graph
    sys.setrecursionlimit(1500)
    graph = Graph(obstacle_map, start_node)
    
    
    # d = Dijkstra()

    import code
    code.interact(local=locals())
