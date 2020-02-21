"""Classes and scripts used in Tree Traversal.
"""
import time
import numpy as np
from .node import Node

def bfs(start_node, tree, verbose=False):
    """Perform a Brute Force Search, appending data to the 
    given `tree` and starting from the given `node`

    This was initially written to be recursive, by python is
    kinda squeamish about recursion limits.
    """
    # timing info
    st = time.time()

    current_nodes = [start_node]
    index = 0
    while current_nodes:
        if verbose:
            loop_time = time.time()

        new_nodes = []
        for node in current_nodes:
            # Add the node to the tree
            if not tree.add(node):
                continue

            # find the children of the given node:
            children = get_children(node.state)
            for child in children:
                index += 1
                new_nodes += [Node(child, node, index)]
        
        # update our list
        current_nodes = new_nodes
        
        if verbose:
            msg = "Processed {} nodes in {:.3f} seconds, {} more found."
            print(msg.format(len(tree),time.time()-loop_time,len(new_nodes)))

    print("Tree traversed in {:.3f} seconds".format(time.time()-st))
    
    # this really isn't necessary, but it's for nice function flow
    return tree

def backtrack(tree, node):
    """Walk back up the given tree, returning the sequential set 
    of parent nodes.
    """
    sequence = [hash(node)]
    child = node
    while child.parent is not None:
        sequence.append(hash(child.parent))
        child = child.parent

    # we actually want the reverse of this sequence
    sequence.reverse()
    return sequence

def get_children(node, action_dist=1):
    """Return all child permutations of the given Node.

    Arguments:
        node: A square array of state values. The zero element
            is assumed to be the empty ("action") element.
        action_dist: The distance which an element can move;
            1: The "action" element can move to 1 tangential space.
            2: The "action" element can move to 2 tangential spaces (or 1 diagonal).
            etc.
    """
    # deliberately eschewing sanity checks for speed
    size = node.shape[0]
    xi,yi = np.where(node==0)

    # build up action set (all "actions" possible)
    action_set = []
    for i in range(action_dist+1):
        for j in range(action_dist-i+1):
            if i == j == 0:
                continue
            action_set.append((i,j))
            action_set.append((-i,j))
            action_set.append((i,-j))
            action_set.append((-i,-j))

    # get the unique set: (very inefficient way of doing this!)
    action_set = set(action_set)

    children = []
    for action in action_set:
        # index of new child:
        xf = action[0] + xi
        yf = action[1] + yi

        # ignore actions that put us out of bounds
        if not 0 <= xf < size:
            continue
        if not 0 <= yf < size:
            continue

        # return permuted child
        child = node.copy()
        child[xi,yi],child[xf,yf] = child[xf,yf], child[xi,yi]

        children.append(child)

    return children

















