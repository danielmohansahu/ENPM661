"""Visualization Tools
"""

from .node import Node
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_path(map_, path, show=False):
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
    if show:
        plt.show()


class ExplorationVisualizer:
    """Helper class to generate visualization of node exploration.
    """
    def __init__(self, map_, nodes, costs, optimal):
        # search variables
        self.map_ = map_
        self.nodes = nodes
        self.costs = costs
        self.optimal = optimal

        # visualization variables
        self.fig,self.ax = self.map_.plot()
        self.ln, = plt.plot([],[],' .b')
        self.map_xdata, self.map_ydata = [],[]

    def plot(self):
        """Actually perform the visualization.
        """
        ani = FuncAnimation(
                self.fig, 
                self._update,
                interval=1,
                init_func=self._init,
                frames=range(len(self.nodes)),
                blit=True)
        plt.show()
   
    def _init(self):
        # self.fig, self.ax = self.map_.plot()
        plt.plot(*self.nodes[0].vertices,'*b')
        plt.text(*self.nodes[0].vertices,"START")
        return self.ln,

    def _update(self,frame):
        if frame==0:
            # zero out data and start fresh
            self.map_xdata = []
            self.map_ydata = []
        
        # update X/Y data and plot 
        self.map_xdata.append(self.nodes[frame].vertices[0])
        self.map_ydata.append(self.nodes[frame].vertices[1])
        self.ln.set_data(self.map_xdata, self.map_ydata)

        # if this is the goal node also write that text
        #  and plot optimal path
        if frame == len(self.nodes)-1:
            self.ln.set_data([],[])

            # add end node (with text)
            plt.plot(*self.optimal[-1].vertices,'*r')
            plt.text(*self.optimal[-1].vertices,"GOAL")

            # convert node to X,Y list
            X = [n.vertices[0] for n in self.optimal]
            Y = [n.vertices[1] for n in self.optimal]
            plt.plot(X,Y)

            plt.pause(60)
        
        return self.ln,
