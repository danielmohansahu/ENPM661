#!/usr/bin/env python3

import sys
import numpy as np
from custom.node import Tree, Node, make_node
from custom.traverse import get_children, bfs, backtrack

if __name__ == "__main__":

    # define our goal node and start node
    goal = [*range(16)]
    goal_node = make_node(goal)
    
    a = goal[0:2]
    a.reverse()
    b = goal
    b[0:2] = a

    start_node = make_node(b)

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

    import code
    code.interact(local=locals())
