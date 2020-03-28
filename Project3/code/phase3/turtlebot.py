#!/usr/bin/env python3

import sys
import argparse
from custom.map import FinalMap
from custom.node import Node, ActionSet
from custom.graph import Graph
from custom.search import AStar
from custom.options import Options
from custom.visualize import ExplorationVisualizer

# default input args
DEFAULT_START = [-4, -4, 60]
DEFAULT_GOAL = [4, 4]
DEFAULT_RPM = [100, 100]
DEFAULT_CLEARANCE = 0.01

def parse_args():
    parser = argparse.ArgumentParser(description="Solve for an optimal path via A*.") 
    parser.add_argument("-s", "--start", 
        default=DEFAULT_START, nargs='+', type=int, help="Starting node indices.")
    parser.add_argument("-g", "--goal", 
        default=DEFAULT_GOAL, nargs='+', type=int, help="Goal node indices.")
    parser.add_argument("-r", "--rpm", 
        default=DEFAULT_RPM, nargs='+', type=float, help="Input RPM")
    parser.add_argument("-c", "--clearance", 
        default=DEFAULT_CLEARANCE, type=float, help="Obstacle avoidance clearance.")
    
    args = parser.parse_args()
    options = Options(args.start, args.goal, args.rpm, args.clearance)
    return options

if __name__ == "__main__":
    # get input arguments
    options = parse_args()

    # generate obstacle map
    obstacle_map = FinalMap()

    # Set node class variables based on inputs
    action_set = ActionSet(
            options.rpm,
            options.wheel_radius,
            options.wheel_separation,
            options.timestep)
    resolution = action_set.calc_resolution()
    print("Using graph resolution {}".format(resolution))
    Node.set_actionset(action_set)
    Node.set_resolution(resolution)
    Node.set_hash_offset(obstacle_map.size()+[0])

    # create start and goal nodes
    buffer_ = options.radius + options.clearance
    if not obstacle_map.is_valid(options.start, buffer_):
        raise RuntimeError("Invalid start node: {}".format(options.start))
    if not obstacle_map.is_valid(options.goal+[0], buffer_):
        raise RuntimeError("Invalid goal node: {}".format(options.goal))
    start_node = Node(options.start)
    goal_node = Node(options.goal+[0])

    print("Start node: {}".format(start_node))
    print("Goal  node: {}".format(goal_node))

    # generate graph
    print("Generating graph...")
    graph = Graph(obstacle_map, start_node, buffer_=buffer_)

    # perform search    
    print("Performing A* search...")
    d = AStar(graph, start_node)
    if not d.solve(goal_node, goal_tolerance=10*resolution[0]):
        print("Failed to find a path to the goal node.")
        sys.exit(1)

    # get path to goal node
    optimal_path,_ = d.get_path()

    # visualize optimal path (and make video of exploration)
    visualizer = ExplorationVisualizer(
            obstacle_map, 
            *d.get_exploration(True, goal_node),
            optimal_path
    ) 
    visualizer.plot(False)

