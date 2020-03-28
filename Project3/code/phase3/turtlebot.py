#!/usr/bin/env python3

import sys
import argparse
from custom.map import FinalMap
from custom import node, graph, search, visualize

# default inputs
DEFAULT_START=[-4, -4, 60]
DEFAULT_GOAL=[4, 4]
DEFAULT_RPM1=100
DEFAULT_RPM2=100
DEFAULT_CLEARANCE=0.1
DEFAULT_RADIUS=0.1
DEFAULT_WHEEL_RADIUS=0.076/2
DEFAULT_WHEEL_SEPARATION=0.354
DEFAULT_TIMESTEP=0.1
DEFAULT_THETA_RES=30
DEFAULT_X_RES=0.1
DEFAULT_Y_RES=0.1

def parse_args():
    parser = argparse.ArgumentParser(description="Solve for an optimal path via A*.") 
    parser.add_argument("-s", "--start", default=DEFAULT_START, nargs='+', type=int, help="Starting node indices.")
    parser.add_argument("-g", "--goal", default=DEFAULT_GOAL, nargs='+', type=int, help="Goal node indices.")
    parser.add_argument("-1", "--rpm1", default=DEFAULT_RPM1, type=float, help="Left wheel RPM.")
    parser.add_argument("-2", "--rpm2", default=DEFAULT_RPM2, type=float, help="Right wheel RPM.")
    parser.add_argument("-c", "--clearance", default=DEFAULT_CLEARANCE, type=float, help="Obstacle avoidance clearance.")
    parser.add_argument("-r", "--radius", default=DEFAULT_RADIUS, type=float, help="Robot radius.")
    parser.add_argument("-t", "--timestep", default=DEFAULT_TIMESTEP, type=float, help="Timestep used in solving action set.")
    parser.add_argument("-w", "--wheel-radius", default=DEFAULT_WHEEL_RADIUS, type=float, help="Wheel radius (meters)")
    parser.add_argument("-S", "--wheel-separation", default=DEFAULT_WHEEL_SEPARATION, type=float, help="Distance between robot wheels (meters).")
    parser.add_argument("-T", "--theta-res", default=DEFAULT_THETA_RES, type=float, help="Theta movement resolution.")
    parser.add_argument("-x", "--x-res", default=DEFAULT_X_RES, type=float, help="X movement resolution.")
    parser.add_argument("-y", "--y-res", default=DEFAULT_Y_RES, type=float, help="Y movemement resolution.")
    return parser.parse_args()

if __name__ == "__main__":
    # get input arguments
    args = parse_args()

    # generate obstacle map
    obstacle_map = FinalMap()

    # Set node class variables based on inputs
    action_set = node.ActionSet(
            [args.rpm1, args.rpm2],
            args.wheel_radius,
            args.wheel_separation,
            args.timestep)
    resolution = (args.x_res, args.y_res, args.theta_res)
    node.Node.set_actionset(action_set)
    node.Node.set_resolution(resolution)
    node.Node.set_hash_offset(obstacle_map.size()+[0])

    # create start and goal nodes
    if len(args.start) != 3 or not obstacle_map.is_valid(args.start, args.radius+args.clearance):
        raise RuntimeError("Invalid start node: {}".format(args.start))
    if len(args.goal) != 2 or not obstacle_map.is_valid(args.goal+[0], args.radius+args.clearance):
        raise RuntimeError("Invalid goal node: {}".format(args.goal))
    start_node = node.Node(args.start)
    goal_node = node.Node(args.goal+[0])

    print("Start node: {}".format(start_node))
    print("Goal  node: {}".format(goal_node))

    # generate graph
    print("Generating graph...")
    graph = graph.Graph(obstacle_map, start_node, buffer_=args.radius + args.clearance)

    # perform search    
    print("Performing A* search...")
    d = search.AStar(graph, start_node)
    if not d.solve(goal_node, goal_tolerance=1.0):
        print("Failed to find a path to the goal node.")
        sys.exit(1)

    # get path to goal node
    optimal_path,_ = d.get_path()

    # visualize optimal path (and make video of exploration)
    visualizer = visualize.ExplorationVisualizer(
            obstacle_map, 
            *d.get_exploration(True, goal_node),
            optimal_path
    ) 
    visualizer.plot()

