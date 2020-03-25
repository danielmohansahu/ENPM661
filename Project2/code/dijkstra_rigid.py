#!/usr/bin/env python3
"""Solve for the optimal path with Dijkstra.
"""
import time
import argparse
import numpy as np
from dijkstra.map import FinalMap
from dijkstra import node, graph, dijkstra, visualize

# default inputs
DEFAULT_START=[5,5]
DEFAULT_GOAL=[295,195]
DEFAULT_CLEARANCE=0
DEFAULT_RADIUS=0

def parse_args():
    parser = argparse.ArgumentParser(description="Solve for an optimal path via Dijkstra.") 
    parser.add_argument("-s", "--start", default=DEFAULT_START, nargs='+', type=int, help="Starting node indices.")
    parser.add_argument("-g", "--goal", default=DEFAULT_GOAL, nargs='+', type=int, help="Goal node indices.")
    parser.add_argument("-c", "--clearance", default=DEFAULT_CLEARANCE, type=float, help="Obstacle avoidance clearance.")
    parser.add_argument("-r", "--radius", default=DEFAULT_RADIUS, type=float, help="Robot radius.")
    return parser.parse_args()

if __name__ == "__main__":
    # Timing metadata
    st = time.time()

    # get args
    args = parse_args()

    # dummy map (for testing)
    obstacle_map = FinalMap()

    # start and goal nodes
    if len(args.start) != 2 or not obstacle_map.is_valid(args.start):
        raise RuntimeError("Invalid start node: {}".format(args.start))
    if len(args.goal) != 2 or not obstacle_map.is_valid(args.goal):
        raise RuntimeError("Invalid goal node: {}".format(args.goal))
    start_node = node.Node(np.array(args.start))
    goal_node = node.Node(np.array(args.goal))
    print("Start node: {}".format(start_node))
    print("Goal  node: {}".format(goal_node))

    # generate graph
    print("Building search graph...")
    st_graph = time.time()
    graph = graph.Graph(obstacle_map, start_node, buffer_=args.clearance + args.radius)
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

