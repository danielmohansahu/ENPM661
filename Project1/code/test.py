#!/usr/bin/env python3

import sys
import argparse
import numpy as np
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

    # define a random start node
    start_node = make_node(np.random.permutation(goal_node.state.flatten()))
    while not start_node.solveable():
        start_node = make_node(np.random.permutation(goal_node.state.flatten()))

    print("Start node: {}".format(start_node))

    # initialize our tree
    tree = Tree(goal_node)

    # build out the brute force search of all paths
    tree = bfs(start_node, tree, verbose=True)

    # find the optimal successful path
    if not tree.successes:
        print("No solution found.")
    
    min_length = np.inf
    optimal = None
    for success in tree.successes:
        path_length = len(tree.backtrack(success))
        if path_length < min_length:
            optimal = success
            min_length = path_length
    print(min_length)

    import code
    code.interact(local=locals())
