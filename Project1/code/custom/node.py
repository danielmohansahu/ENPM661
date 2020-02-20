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
    if not isinstance(state,list):
        raise RuntimeError("Expected state to be of type 'list'")
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

        # also keep a list of "correct" node hashes
        self.goal_node = goal_node
        self.goal_hash = hash(goal_node)
        self.successes = []

    def __len__(self):
        return len(self.nodes)

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

    def success(self, node_hash):
        """Check if the given node matches our goal state.
        """
        success = node_hash == self.goal_hash
        return success

    def add(self,node):
        """Add a single node to the tree.

        Args:
            node: A custom.Node object

        Returns:
            bool indicating if the traversal should continue
        """
        node_hash = hash(node)
        
        # check if this is a successful node.
        if self.success(node_hash):
            self.successes.append(node)
            return False
        
        # check if node already exists; if so ignore
        if node_hash in self.nodes.keys():
            return False

        # add to dict
        self.nodes[node_hash] = node
        return True

class Node:
    """A simple data structure to handle node information.

    No error checking is done in this class.
    """
    def __init__(self, state, parent=None):
        # assume state is square np array
        self.state = state
        # assume parent is a reference to another node
        self.parent = parent

    def solveable(self):
        """Returns true if this node is solveable
        https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
        """
        state = self.state.flatten().tolist()
        inv = sum(sum(1 for j in range(i+1,len(state)) if state[j] > val) for i,val in enumerate(state))
        return not bool(inv%2)

    def __hash__(self):
        return hash(tuple(self.state.flatten()))

    def __str__(self):
        return " ".join([str(v) for v in self.state.flatten()])

