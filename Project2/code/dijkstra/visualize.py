"""Visualization Tools
"""

from .node import Node
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_path(map_, path):
    """Visualize the given optimal path in the given map_.

    Args:
        map_: The workspace map.
        path: A list of Node objects.
    """
    # plot map
    map_.plot()

    # add start end end nodes (with text)
    plt.plot(*path[0].vertices,'*b')
    plt.text(*path[0].vertices,"START")
    plt.plot(*path[-1].vertices,'*r')
    plt.text(*path[-1].vertices,"GOAL")

    # convert node to X,Y list
    X = [n.vertices[0] for n in path]
    Y = [n.vertices[1] for n in path]

    plt.plot(X,Y)
    plt.show()


class ExplorationVisualizer:
    """Helper class to generate visualization of node exploration.
    """
    def __init__(self, map_, nodes, costs):
        # search variables
        self.map_ = map_
        self.nodes = nodes
        self.costs = costs

        # visualization variables
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [],[]

    def plot(self):
        """Actually perform the visualization.
        """
        ani = FuncAnimation(
                self.fig, 
                self._update, 
                frames=len(self.nodes), 
                init_func=self._init, 
                blit=True)
        plt.show()
    
    def _init(self):
        self.ln, = self.map_.plot()
        plt.plot(*self.nodes[0].vertices,'*b')
        plt.text(*self.nodes[0].vertices,"START")
        self.ln.set_marker('.')
        self.ln.set_linestyle(' ')
        return self.ln,
    
    def _update(self,frame):
        self.xdata.append(self.nodes[frame].vertices[0]) 
        self.ydata.append(self.nodes[frame].vertices[1]) 
        self.ln.set_data(self.xdata, self.ydata)
        return self.ln,
    
