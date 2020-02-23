#!/usr/bin/env python3

import sys
import argparse
import numpy as np
from custom.utils import to_file
from custom.node import Tree, Node, make_node
from custom.traverse import get_children, bfs, backtrack

def parse_args():
    """Parse command line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=9, help="Size of puzzle to solve.")
    parser.add_argument("-r", "--random", type=bool, default=True, help="Solve a random puzzle.")
    parser.add_argument("-s", "--start", nargs="+", type=int, required=False, help="Initial start node (as a list).")

    # parse args
    args = parser.parse_args()

    # determine run mode based on input flags
    if args.start:
        # if we're given an argument list, ignore other args
        args.size = len(args.start)
        args.random = False
    elif not args.random:
        raise RuntimeError("Cannot run with --random False and no --start node given.")

    return args

if __name__ == "__main__":
    # parse arguments
    args = parse_args()

    # define our goal node and start node
    goal = [*range(1,args.size)] + [0]
    goal_node = make_node(goal)
    print("Goal node: {}".format(goal_node))

    # define a random start node
    if args.start:
        # use the user input node
        start_node = make_node(args.start)
        if not start_node.solveable():
            raise RuntimeError("Given node {} is not solveable.".format(args.start))       
    else:
        # make a random starting node
        start_node = make_node(np.random.permutation(goal_node.state.flatten()))
        while not start_node.solveable():
            start_node = make_node(np.random.permutation(goal_node.state.flatten()))
    print("Start node: {}".format(start_node))

    # initialize our tree
    tree = Tree(goal_node)

    # build out the brute force search of all paths
    tree = bfs(start_node, tree, verbose=False)

    # find the optimal successful path
    if not tree.successes:
        print("No solution found.")
    else:
        print("Optimal solution length: {}".format(tree.optimal_path_length))

    # print our results
    to_file(tree.print_soln(), "nodePath.txt")
    to_file(tree.print_all(), "Nodes.txt")
    to_file(tree.print_info(), "NodesInfo.txt")

    # import code
    # code.interact(local=locals())
