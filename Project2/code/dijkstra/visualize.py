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
        self.fig, self.ax = plt.subplots()
        self.map_xdata, self.map_ydata = [],[]

    def plot(self):
        """Actually perform the visualization.
        """
        ani = FuncAnimation(
                self.fig, 
                self._update,
                interval=0,
                frames=range(len(self.nodes)),
                blit=True)
        plt.show()
    
    def _update(self,frame):
        # perform initialization
        if frame == 0:
            # draw map background
            self.ln, = self.map_.plot()

            # draw start node
            plt.plot(*self.nodes[0].vertices,'*b')
            plt.text(*self.nodes[0].vertices,"START")

            # reset X/Y data and plot 
            self.map_xdata = self.ln.get_xdata()
            self.map_ydata = self.ln.get_ydata()
            
            # set data
            self.ln.set_marker("*")
            self.ln.set_markersize(4)
            self.ln.set_linestyle(" ")

        # update X/Y data and plot 
        new_x = self.map_xdata + [self.nodes[frame].vertices[0]]
        new_y = self.map_ydata + [self.nodes[frame].vertices[1]]
        self.ln.set_data(new_x,new_y)

        # if this is the goal node also write that text
        #  and plot optimal path
        if frame == len(self.nodes)-1:
            plot_path(self.map_, self.optimal)

            # wait for user input
            plt.waitforbuttonpress()
        
        return self.ln,
