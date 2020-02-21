import numpy as np

def make_node(state, parent=None):
    """Perform some sanity checks on state information.
    This is for parsing input lists, not internal operation.

    Args:
        state:  A list of integers of length int^2
        parent: (Optional) parent node.

    Returns:
        A custom.Node object containing state info.
    """
    
    # get shape information
    shape = int(np.sqrt(len(state)))

    # sanity checks:
    if not shape*shape == len(state):
        raise RuntimeError("Square root of the length of input list must be an integer!.")
    if not isinstance(parent,(Node, type(None))):
        raise RuntimeError("Expected parent to be of type 'custom.Node'")

    # if we've passed all our sanity checks, return a node:
    state = np.array(state, dtype=np.uint8)
    state.resize([shape]*2)
    return Node(np.array(state,dtype=np.uint8), parent)

class Tree:
    """A tree (basically just a dict of Nodes)
    """
    def __init__(self, goal_node):
        # nodes: flat dict of (hash: object) for Nodes.
        self.nodes = {}

        # also keep a list of "correct" nodes (not hashes!!)
        self.successes = []
        self.optimal_path_length = np.inf
        self.optimal_node = None

        # keep track of our target node
        self.goal_node = goal_node
        self.goal_hash = hash(goal_node)

    def solved(self):
        return len(self.successes) > 0

    def backtrack(self, node):
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

    def check_optimal(self):
        """Check which of our successes is the optimal path.
        """
        for node in self.successes:
            path_length = len(self.backtrack(node))
            if path_length < self.optimal_path_length:
                self.optimal_node = node
                self.optimal_path_length = path_length

    def success(self, node_hash):
        """Check if the given node matches our goal state.
        """
        success = node_hash == self.goal_hash
        return success

    def add(self,node):
        """Add a single node to the tree.

        Returns:
            bool indicating if the traversal should continue
        """
        node_hash = hash(node)
        
        # check if this is a successful node.
        if self.success(node_hash):
            print("Success found!")
            self.successes.append(node)
            if node_hash not in self.nodes.keys():
                self.nodes[node_hash] = node
            self.check_optimal()
            return False
        
        # check if node already exists; if so ignore
        if node_hash in self.nodes.keys():
            return False

        # add to dict
        self.nodes[node_hash] = node
        return True
    
    def __len__(self):
        # define length as the length of nodes
        return len(self.nodes)

    #-------------------- PRINTING API ------------------------#

    def print_soln(self):
        """ String representation of the solution.
        """
        result = ""
        if self.solved():
            for node_hash in self.backtrack(self.optimal_node):
                result += str(self.nodes[node_hash]) + "\n"
        return result
    
    def print_all(self):
        """ String representation of all explored nodes..
        """
        result = ""
        for _,node in self.nodes.items():
            result += str(node) + "\n"
        return result

    def print_info(self):
        """String representation of parent/child relationship of nodes.
        This is really slow....
        """
        result = ""
        for _,node in self.nodes.items():
            parent_idx = 0 if not node.parent else node.parent.index
            result += "{} {} 0\n".format(node.index, parent_idx)
        return result

class Node:
    """A simple data structure to handle node information.

    No error checking is done in this class.
    """
    def __init__(self, state, parent=None, index=0):
        # assume state is square np array
        self.state = state
        # assume parent is a reference to another node
        self.parent = parent
        # index (order in which this was found)
        self.index = index

    def solveable(self):
        """Returns true if this node is solveable
        https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
        """
        state = self.state.flatten().tolist()
        size = len(state)
        inv_count = 0 
        for i in range(size):
            for j in range(i+1,size): 
                if (state[j] and state[i] and state[i] > state[j]):
                  inv_count += 1
        return inv_count%2 == 0
    
    def __hash__(self):
        return hash(tuple(self.state.flatten()))

    def __str__(self):
        return " ".join([str(v) for v in self.state.flatten()])

