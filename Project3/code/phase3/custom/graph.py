"""Class representing the Graph of Nodes (derived via BFS)
"""
import time
import sys
from collections import defaultdict
from .node import Node

class Graph:
    """Iteratively build and store a graph of Nodes from a given start.
    """
    def __init__(self, map_, start_node, buffer_=0):
        # map of obstacle space; used to in collision detection
        self.map_ = map_

        # buffer size to use (i.e. robot radius
        self.buffer_ = buffer_
        
        # sanity check input
        if not isinstance(start_node, Node):
            raise ValueError("Start node given to Graph isn't a Node object.")

        # calculate total possible number of nodes (for reference)
        self.max_nodes = map_.size()[0]/start_node.resolution_[0]\
                         * map_.size()[1]/start_node.resolution_[1]\
                         * 360/start_node.resolution_[2]

        # nodes: dict of explored nodes (key: value) -> (hash: node)
        # tree: hierarchical relationships between nodes (parent: children)
        st = time.time()
        self.nodes, self.tree = self.construct(start_node)
        print("Took {:.3f}s to build search graph.".format(time.time()-st))

    def construct(self, start_node):
        """Build out the set of Nodes, starting from our start node.
        """
        tree = defaultdict(dict)
        nodes = {}
        
        current_nodes = [start_node] 
        while len(current_nodes) != 0:
            new_nodes = []
            for node in current_nodes:
                node_hash = hash(node)

                # we've already explored this node
                if node_hash in nodes.keys():
                    continue

                # invalid node (obstacle or outside bounds)
                if not self.map_.is_valid(node.vertices, self.buffer_):
                    continue
                
                # add valid nodes to our tree
                if node.parent:
                    tree[hash(node.parent)][node_hash] = node.cost2come - node.parent.cost2come
               
                # valid node; add it to our visited nodes
                nodes[node_hash] = node
                children = node.get_children()
                
                # add children to be processed next round
                new_nodes += children

            # update status bar
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%% (worst case)" % ('='*int(20*len(nodes)/self.max_nodes), int(100*len(nodes)/self.max_nodes)))
            sys.stdout.flush()

            current_nodes = new_nodes
        print()
        return nodes, tree













