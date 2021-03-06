"""Class representing a single node.

This class also defines the action set of a node.
"""

import random
import numpy as np

def get_random_node(map_):
    """Get a random valid node within our workspace. 
    """
    x = y = theta = -1
    bounds = map_.workspace.get_extents()
    while not map_.is_valid([x,y,theta]):
        x = random.randint(bounds.x0,bounds.x1) 
        y = random.randint(bounds.y0,bounds.y1) 
        theta = random.randint(0,360)
    return node.Node(np.array([x,y,theta]))

class ActionSet:
    """Class containing all the available node actions.
    """
    def __init__(self, step_size=1, angles=[-60, -30, 0, 30, 60]):
        """
        """
        self.angles = angles
        self.step_size = step_size

    def get_actions(self, vertices):
        """Calculate the potential actions from the given position.
        """
        actions = {}
        for angle in self.angles:
            new_angle = (vertices[2] + angle)%360
            x_diff = self.step_size * np.cos(new_angle*np.pi/180)
            y_diff = self.step_size * np.sin(new_angle*np.pi/180)
            actions[(x_diff, y_diff, angle)] = self.step_size
        return actions

class Node:
    """
    """
    # default resolution of node directions (for binning)
    resolution_ = (1, 1, 30)

    # default action set
    action_set_ = ActionSet()

    def __init__(self, vertices, cost2come=0, parent=None):
        # vertices (x,y,theta) position of node
        self.vertices = np.array(vertices)
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
        return str(self.rounded_vertices)
    
    def __eq__(self, rhs):
        """Comparison to other nodes.
        """
        if not isinstance(rhs, Node):
            raise RuntimeError("Cannot compare nodes to non-nodes")
        return self.rounded_vertices == rhs.rounded_vertices

    @classmethod
    def set_actionset(cls, actionset):
        """Set the action set (for all Nodes)
        """
        if not isinstance(actionset, ActionSet):
            raise RuntimeError("Given actionset is of the wrong class.")
        cls.action_set = actionset

    @classmethod
    def set_resolution(cls, resolution):
        """Set the class resolution.
        """
        if len(resolution) != 3:
            raise RuntimeError("Expected resolution to have length 3 (x, y, theta).")
        cls.resolution_ = resolution

    def round(self, vertices):
        """Round the given vertices (x,y,theta) to the class's resolution.
        """
        result = [] 
        for val, res in zip(vertices, self.resolution_):
            result.append(round(val/res)*res)
        return result

    def cost2go(self, goal_node):
        """Calculate the euclidean distance to the target node.
        """
        return np.linalg.norm(self.vertices[:2]-goal_node.vertices[:2])

    def get_children(self):
        """Generate and return a list of all possible child nodes.

        This list is "dumb" in that it ignores workspace bounds
        and obstacles.
        """
        children = []
        actions = self.action_set_.get_actions(self.vertices)

        for action, cost in actions.items(): 
            # calculate child position and cost and store in a new node
            new_vertices = self.vertices + np.array(action)
            new_vertices[2] %= 360
            child = Node(new_vertices, self.cost2come + cost, self)

            # small optimization; don't return parent node
            if (not self.parent) or child != self.parent:
                children.append(child)
        return children












