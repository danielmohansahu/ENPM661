"""Class representing the Graph of Nodes (derived via BFS)
"""
import time
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

        # nodes: dict of explored nodes (key: value) -> (hash: node)
        # tree: hierarchical relationships between nodes (parent: children)
        self.nodes, self.tree = self.construct(start_node)

    def construct(self, start_node):
        """Build out the set of Nodes, starting from our start node.
        """
        tree = defaultdict(dict)
        nodes = {}
        
        current_nodes = [start_node] 
        while len(current_nodes) != 0:
            st = time.time()
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

            print("Processed {}/{} nodes in {}, {} more found.".format(len(current_nodes),len(nodes),time.time()-st,len(new_nodes)))
            current_nodes = new_nodes
        return nodes, tree













