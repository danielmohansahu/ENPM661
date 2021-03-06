#!/usr/bin/env python3

import argparse
from custom.map import TestMap,FinalMap
from custom import node, graph, search, visualize

# default inputs
DEFAULT_START=[50, 30, 60]
DEFAULT_GOAL=[150, 150, 60]
DEFAULT_CLEARANCE=1
DEFAULT_RADIUS=1
DEFAULT_STEP_SIZE=1
DEFAULT_THETA_RES=30
DEFAULT_X_RES=0.5
DEFAULT_Y_RES=0.5

def parse_args():
    parser = argparse.ArgumentParser(description="Solve for an optimal path via A*.") 
    parser.add_argument("-s", "--start", default=DEFAULT_START, nargs='+', type=int, help="Starting node indices.")
    parser.add_argument("-g", "--goal", default=DEFAULT_GOAL, nargs='+', type=int, help="Goal node indices.")
    parser.add_argument("-c", "--clearance", default=DEFAULT_CLEARANCE, type=float, help="Obstacle avoidance clearance.")
    parser.add_argument("-r", "--radius", default=DEFAULT_RADIUS, type=float, help="Robot radius.")
    parser.add_argument("-S", "--step-size", default=DEFAULT_STEP_SIZE, type=int, help="Movement step size.")
    parser.add_argument("-t", "--theta-res", default=DEFAULT_THETA_RES, type=float, help="Theta movement resolution.")
    parser.add_argument("-x", "--x-res", default=DEFAULT_X_RES, type=float, help="X movement resolution.")
    parser.add_argument("-y", "--y-res", default=DEFAULT_Y_RES, type=float, help="Y movemement resolution.")
    return parser.parse_args()

if __name__ == "__main__":
    # get input arguments
    args = parse_args()

    # generate obstacle map
    obstacle_map = FinalMap()

    # Set node class variables based on inputs
    action_set = node.ActionSet(args.step_size,[args.theta_res*v for v in [-2,-1,0,1,1]])
    resolution = (args.x_res, args.y_res, args.theta_res)
    node.Node.set_actionset(action_set)
    node.Node.set_resolution(resolution)

    # create start and goal nodes
    if len(args.start) != 3 or not obstacle_map.is_valid(args.start):
        raise RuntimeError("Invalid start node: {}".format(args.start))
    if len(args.goal) != 3 or not obstacle_map.is_valid(args.goal):
        raise RuntimeError("Invalid goal node: {}".format(args.goal))
    start_node = node.Node(args.start)
    goal_node = node.Node(args.goal)

    print("Start node: {}".format(start_node))
    print("Goal  node: {}".format(goal_node))

    # generate graph
    print("Generating graph...")
    graph = graph.Graph(obstacle_map, start_node, buffer_=args.radius + args.clearance)

    # perform search    
    print("Performing A* search...")
    d = search.AStar(graph, start_node)
    d.solve(goal_node)

    # get path to goal node
    optimal_path,_ = d.get_path(goal_node)

    # visualize optimal path (and make video of exploration)
    visualizer = visualize.ExplorationVisualizer(
            obstacle_map, 
            *d.get_exploration(True, goal_node),
            optimal_path
    ) 
    visualizer.plot()

