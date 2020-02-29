#!/usr/bin/env python3

import code
import numpy as np
from dijkstra.map import Map
from dijkstra import node, graph, dijkstra, visualize

if __name__ == "__main__":

    # start and goal
    start_node = node.Node(np.array([19,33]))
    goal_node = node.Node(np.array([111,23]))

    # dummy map (for testing)
    obstacle_map = Map(xbounds=[0,300],ybounds=[0,200])

    # generate graph
    graph = graph.Graph(obstacle_map, start_node)
    
    # perform search (via Dijkstra's Algorithm)    
    d = dijkstra.Dijkstra(graph, start_node)
    d.solve()

    # get path to goal node
    path, cost = d.get_path(goal_node)

    # visualize path
    visualize.plot_path(path) 
    

    # code.interact(local=locals())
