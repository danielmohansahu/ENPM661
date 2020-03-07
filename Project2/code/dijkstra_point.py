#!/usr/bin/env python3
"""Solve for the optimal path with Dijkstra.
"""
import time
import numpy as np
from dijkstra.map import FinalMap
from dijkstra import node, graph, dijkstra, visualize

if __name__ == "__main__":
    # Timing metadata
    st = time.time()

    # dummy map (for testing)
    obstacle_map = FinalMap()

    # start and goal nodes
    start_node = node.Node(np.array([5,5]))
    goal_node = node.Node(np.array([295,195]))
    print("Start node: {}".format(start_node))
    print("Goal  node: {}".format(goal_node))

    # generate graph
    print("Building search graph...")
    st_graph = time.time()
    graph = graph.Graph(obstacle_map, start_node, buffer_=0)
    print("Took {:.3f}s to build search graph.".format(time.time()-st_graph))
    
    # perform search (via Dijkstra's Algorithm)    
    print("Solving for optimal path...")
    st_solve = time.time()
    d = dijkstra.Dijkstra(graph, start_node)
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

