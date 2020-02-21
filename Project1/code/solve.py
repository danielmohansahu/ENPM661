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
    parser.add_argument("--size", type=int, default=9, help="Size of puzzle to solve.")
    return parser.parse_args()

if __name__ == "__main__":
    # parse arguments
    args = parse_args()

    # define our goal node and start node
    goal = [*range(1,args.size)] + [0]
    goal_node = make_node(goal)
    print("Goal node: {}".format(goal_node))

    # define a random start node
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
