"""Class representing a single node.

This class also defines the action set of a node.
"""

import numpy as np

class Node:
    """
    """
    # list of all possible discrete actions mapped to cost
    actions_ = {
        (-1,-1): np.sqrt(2),
        (-1, 0): 1,
        (-1, 1): np.sqrt(2),
        ( 0,-1): np.sqrt(2),
        ( 0, 1): 1,
        ( 1,-1): np.sqrt(2),
        ( 1, 0): 1,
        ( 1, 1): np.sqrt(2),
    }
    def __init__(self, vertices, cost2come=0, parent=None):
        # vertices (x,y) position of node
        self.vertices = vertices
        # cost2come; cumulative cost of getting to this node
        self.cost2come = cost2come
        # reference to the parent node
        self.parent = parent

    def __hash__(self):
        """Calculate the unique hash of our vertices (for easier comparison)
        """
        return hash(tuple(self.vertices))

    def __str__(self):
        """String representation (for debugging / convenience)
        """
        return str(self.vertices)
    
    def __eq__(self, rhs):
        """Comparison to other nodes.
        """
        if not isinstance(rhs, Node):
            raise RuntimeError("Cannot compare nodes to non-nodes")
        return all(self.vertices == rhs.vertices)

    def get_children(self):
        """Generate and return a list of all possible child nodes.

        This list is "dumb" in that it ignores workspace bounds
        and obstacles.
        """
        children = []
        for action, cost in self.actions_.items(): 
            # calculate child position and cost and store in a new node
            child = Node(
                self.vertices + np.array(action),
                self.cost2come + cost,
                self
            )

            # small optimization; don't return parent node
            if (not self.parent) or child != self.parent:
                children.append(child)
        return children












