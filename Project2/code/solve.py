#!/usr/bin/env python3

import code
import numpy as np
import random
import time
from dijkstra.map import Map
from dijkstra import node, graph, dijkstra, visualize
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def get_random_node(map_):
    """Get a random valid node within our workspace. 
    """
    x = y = -1 
    while not map_.isvalid([x,y]):
        x = random.randint(*map_.xbounds) 
        y = random.randint(*map_.ybounds) 
    return node.Node(np.array([x,y]))


if __name__ == "__main__":

    # dummy map (for testing)
    obstacle_map = Map(xbounds=[0,30],ybounds=[0,20])

    # get a random start and goal
    start_node = get_random_node(obstacle_map)
    goal_node = get_random_node(obstacle_map)

    print("Start node: {}".format(start_node))
    print("Goal  node: {}".format(goal_node))

    # generate graph
    print("Building search graph...")
    graph = graph.Graph(obstacle_map, start_node)
    
    # perform search (via Dijkstra's Algorithm)    
    print("Solving for optimal path...")
    d = dijkstra.Dijkstra(graph, start_node)
    d.solve()

    # get path to goal node
    path, cost = d.get_path(goal_node)

    # visualize optimal path (and make video of exploration)
    visualizer = visualize.ExplorationVisualizer(
            obstacle_map, 
            *d.get_exploration(True, goal_node)
    ) 
    visualizer.plot()
    visualize.plot_path(obstacle_map, path) 

