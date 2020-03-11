"""Class representing a single node.

This class also defines the action set of a node.
"""

import numpy as np

class ActionSet:
    """
    """
    def __init__(self, step_size=1, angles=[-np.pi/3, -np.pi/6, 0, np.pi/6, np.pi/3]):
        """
        """
        self.angles = angles
        self.step_size = step_size

    def get_actions(self, vertices):
        """Calculate the potential actions from the given position.
        """
        actions = {}
        for angle in self.angles:
            new_angle = vertices[2] + angle
            new_x = vertices[0] + step_size * np.cos(new_angle)
            new_y = vertices[1] + step_size * np.sin(new_angle)
            actions[(new_x, new_y, new_angle)] = step_size
        return actions

class Node:
    """
    """
    # resolution of node directions (for binning)
    resolution_ = (0.5, 0.5, 30*np.pi/180)

    # action set
    action_set_ = ActionSet()

    def __init__(self, vertices, cost2come=0, parent=None):
        # vertices (x,y,theta) position of node
        self.vertices = vertices
        self.rounded_vertices = self.round(vertices)

        # cost2come; cumulative cost of getting to this node
        self.cost2come = cost2come

        # reference to the parent node
        self.parent = parent

    def __hash__(self):
        """Calculate the unique hash of our vertices (for easier comparison)

        Note that this uses our rounded vertices, to allow binning.
        """
        return hash(tuple(self.rounded_vertices))

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

    @classmethod
    def round(cls, vertices):
        """Round the given vertices (x,y,theta) to the class's resolution.
        """
        result = [] 
        for val, res in zip(vertices, cls.resolution_):
            result.append(round(val/res)*res)
        return result

    def get_children(self):
        """Generate and return a list of all possible child nodes.

        This list is "dumb" in that it ignores workspace bounds
        and obstacles.
        """
        children = []
        for action, cost in self.action_set_.get_actions(self.vertices).items(): 
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












