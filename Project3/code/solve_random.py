#!/usr/bin/env python3

import code
import numpy as np
import random
import time
from custom.map import TestMap,FinalMap
from custom import node, graph, search, visualize

def get_random_node(map_):
    """Get a random valid node within our workspace. 
    """
    x = y = theta = -1
    bounds = map_.workspace.get_extents()
    while not map_.is_valid([x,y,theta]):
        x = random.randint(bounds.x0,bounds.x1) 
        y = random.randint(bounds.y0,bounds.y1) 
        theta = random.randint(0,360)*np.pi/180
    return node.Node(np.array([x,y]))

if __name__ == "__main__":
    # Timing metadata
    st = time.time()

    # dummy map (for testing)
    obstacle_map = TestMap()

    # get a random start and goal
    start_node = get_random_node(obstacle_map)
    goal_node = get_random_node(obstacle_map)

    print("Start node: {}".format(start_node))
    print("Goal  node: {}".format(goal_node))

    # generate graph
    print("Building search graph...")
    st_graph = time.time()
    graph = graph.Graph(obstacle_map, start_node)
    print("Took {:.3f}s to build search graph.".format(time.time()-st_graph))
    
    # perform search    
    print("Solving for optimal path...")
    st_solve = time.time()
    d = search.AStar(graph, start_node)
    d.solve()
    print("Took {:.3f}s to solve for optimal path.".format(time.time()-st_solve))

    # get path to goal node
    optimal_path,_ = d.get_path(goal_node)
    print("Took {:.3f} for all operations.".format(time.time()-st))

    # visualize optimal path (and make video of exploration)
    visualizer = visualize.ExplorationVisualizer(
            obstacle_map, 
            *d.get_exploration(True, goal_node),
            optimal_path
    ) 
    visualizer.plot()

