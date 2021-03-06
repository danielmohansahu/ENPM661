"""Class representing a single node.

This class also defines the action set of a node.
"""

import math
import numpy as np

class ActionSet:
    """Class containing all the available node actions.
    """
    def __init__(self, RPM=[1,1], r=0.5, L=0.5, dt=0.01):
        # time step (in minutes)
        self.dt = dt
        self.r = r
        self.L = L
        self.actions = [
            [0,RPM[0]],
            [RPM[0],0],
            [RPM[0],RPM[0]],
            [0,RPM[1]],
            [RPM[1],0],
            [RPM[1],RPM[1]],
            [RPM[0],RPM[1]],
            [RPM[1],RPM[0]]
        ]

    def calc_resolution(self, start_theta):
        """Calculate necessary X/Y/Theta resolution
        """
        _,moves,_ = self.get_moves([0,0,0])
        X = set([abs(m[0]) for m in moves if m[0]!=0])
        T = [m[2] for m in moves]
        T = set([m for m in T+[start_theta] if m!=0])

        # get recommended resolution:
        leading_digit = lambda x: -int(math.floor(math.log10(abs(x))))
        round_to_first = lambda x,d: np.floor(x*10**d)/10.0**d
        res_x = min([round_to_first(v,leading_digit(v)) for v in X]) 
        res_t = min([round_to_first(v,leading_digit(v)) for v in T]) 
        
        # set some more reasonable limits
        res_x = max(res_x, 0.1)
        res_t = max(res_t, 15)

        return [res_x, res_x, res_t]

    def get_moves(self, current_pos):
        """Calculate the potential moves from the given position.
        """
        actions = []
        moves = []
        costs = []

        for action in self.actions:
            cur_angle = current_pos[2]*np.pi/180

            # calcute deltas
            dtheta = self.r*(action[1]-action[0])*self.dt/self.L
            dx = 0.5*self.r*(action[0]+action[1])*np.cos(dtheta+cur_angle)*self.dt
            dy = 0.5*self.r*(action[0]+action[1])*np.sin(dtheta+cur_angle)*self.dt

            # calculate new absolute positions
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            new_angle = (current_pos[2] + dtheta*180/np.pi)%360

            # assume that cost is measured in time
            actions.append(action)
            moves.append((new_x, new_y, new_angle))
            costs.append(self.dt)
        return actions, moves, costs

class Node:
    """
    """
    # default resolution of node directions (for binning)
    resolution_ = None

    # hash offset (a hack to handle the hashing of negative tuples
    hash_offset_ = None

    # default action set
    action_set_ = None

    def __init__(self, vertices, cost2come=0, parent=None, parent_action=None):
        # vertices (x,y,theta) position of node
        self.vertices = np.array(vertices)
        self.rounded_vertices = self.round(vertices)

        # cost2come; cumulative cost of getting to this node
        self.cost2come = cost2come

        # reference to the parent node
        self.parent = parent
        self.parent_action = parent_action

    def __hash__(self):
        """Calculate the unique hash of our vertices (for easier comparison)

        Note that this uses our rounded vertices, to allow binning.
        """
        return hash(tuple(self.rounded_vertices+self.hash_offset_))

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
    def set_hash_offset(cls, offset):
        """Set the hash offset (for all Nodes)
        """
        cls.hash_offset_ = np.array(offset)

    @classmethod
    def set_actionset(cls, actionset):
        """Set the action set (for all Nodes)
        """
        if not isinstance(actionset, ActionSet):
            raise RuntimeError("Given actionset is of the wrong class.")
        cls.action_set_ = actionset

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

    def cost2go(self, target_node):
        """Calculate the euclidean distance to the target node.
        """
        return np.linalg.norm(self.vertices[:2]-target_node.vertices[:2])

    def is_goal(self, goal_node, tolerance):
        """Check whether this is the goal node.
        """
        return self.cost2go(goal_node) < tolerance 

    def get_children(self):
        """Generate and return a list of all possible child nodes.

        This list is "dumb" in that it ignores workspace bounds
        and obstacles.
        """
        children = []
        actions,moves,costs = self.action_set_.get_moves(self.vertices)

        for action, move, cost in zip(actions,moves,costs): 
            child = Node(np.array(move), self.cost2come + cost, self, action)

            # small optimization; don't return parent node
            if (not self.parent) or child != self.parent:
                children.append(child)
        return children












