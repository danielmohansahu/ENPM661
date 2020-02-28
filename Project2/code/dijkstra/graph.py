"""Class representing the Graph of Nodes (derived via BFS)
"""

from collections import defaultdict
from .node import Node

class Graph:
    """Iteratively build and store a graph of Nodes from a given start.
    """
    def __init__(self, map_, start_node):
        # map of obstacle space; used to in collision detection
        self.map_ = map_
        
        # sanity check input
        if not isinstance(start_node, Node):
            raise ValueError("Start node given to Graph isn't a Node object.")

        # nodes: dict of explored nodes (key: value) -> (hash: node)
        # tree: hierarchical relationships between nodes (parent: children)
        self.nodes, self.tree = self.construct(start_node)
        
        # dict of hierarchical relationships between nodes (parent: children)
        self.tree = defaultdict(list)

    def construct(self, start_node):
        """Build out the set of Nodes, starting from our start node.
        """
        tree = defaultdict(list)
        nodes = {}
        
        current_nodes = [start_node] 
        while len(current_nodes) != 0:
            print("Processing {} new nodes".format(len(current_nodes)))
            new_nodes = []
            for node in current_nodes:
                node_hash = hash(node)
               
                # check return conditions
                if node_hash in nodes.keys():
                    # we've already explored this node
                    continue
                elif not self.map_.isvalid(node.vertices):
                    # invalid node (obstacle or outside bounds)
                    continue

                # valid node; add it to our visited nodes
                nodes[node_hash] = node
                children = node.get_children()
                tree[hash(node.parent)].append(node_hash)
                
                # add children to be processed next round
                new_nodes += children

            current_nodes = new_nodes
        return nodes, tree













