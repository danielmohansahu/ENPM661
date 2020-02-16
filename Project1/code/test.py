#!/usr/bin/env python3

import sys
import numpy as np
from custom.node import Tree, Node, make_node
from custom.traverse import get_children, bfs, backtrack

if __name__ == "__main__":

    # define our goal node and start node
    goal_node = make_node([*range(9)])
    start_node = make_node([1,0,2,3,4,5,6,7,8])

    # initialize our tree
    tree = Tree(goal_node)

    # build out the brute force search of all paths
    tree = bfs(start_node, tree, verbose=False)

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

    import code
    code.interact(local=locals())
