"""Visualization Tools
"""

from .node import Node
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers

def plot_path(map_, path, show=False):
    """Visualize the given optimal path in the given map_.

    Args:
        map_: The workspace map.
        path: A list of Node objects.
    """
    # plot map
    map_.plot()

    # add start end end nodes (with text)
    plt.plot(*path[0].vertices[:2],'*b')
    plt.text(*path[0].vertices[:2],"START")
    plt.plot(*path[-1].vertices[:2],'*r')
    plt.text(*path[-1].vertices[:2],"GOAL")

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
        self.ln = plt.quiver([],[],[],[],angles='xy')
        self.x_data = []
        self.y_data = []
        self.u_data = []
        self.v_data = []

        # misc variables
        self.max_size = 1000

    def plot(self, save=True):
        """Actually perform the visualization.
        """
        ani = FuncAnimation(
                self.fig, 
                self._update,
                interval=1,
                repeat=False,
                repeat_delay=10,
                init_func=self._init,
                frames=range(len(self.nodes)),
                blit=True)

        if save and "ffmpeg" in writers.list():
            # save to a local video file
            print("Saving video to `results.mp4`...")
            Writer = writers["ffmpeg"]
            writer = Writer(fps=30, metadata=dict(artist="Me"), bitrate=1800)
            ani.save("results.mp4", writer=writer)
            return
        elif save and "ffmpeg" not in writers.list():
            print("Unable to create video file; ffmpeg is not installed.")
            
        # if we've made it this far we want to display the video
        plt.show()
   
    def _init(self):
        # add start and end node (with text)
        plt.plot(*self.nodes[0].vertices[:2],'*b')
        plt.text(*self.nodes[0].vertices[:2],"START")
        plt.plot(*self.optimal[-1].vertices[:2],'*r')
        plt.text(*self.optimal[-1].vertices[:2],"GOAL")
        return self.ln,

    def _update(self,frame):
        
        # skip the first node (it has no parent)
        if not self.nodes[frame].parent:
            return self.ln,

        # update X/Y data and plot 
        self.x_data.append(self.nodes[frame].parent.vertices[0])
        self.y_data.append(self.nodes[frame].parent.vertices[1])
        self.u_data.append(self.nodes[frame].vertices[0]-self.x_data[-1])
        self.v_data.append(self.nodes[frame].vertices[1]-self.y_data[-1])
        
        # only keep the last N values 
        if len(self.x_data) > self.max_size:
            self.x_data.pop(0)
            self.y_data.pop(0)
            self.u_data.pop(0)
            self.v_data.pop(0)

        # set updated data
        self.ln = plt.quiver(self.x_data, self.y_data, self.u_data, self.v_data, angles='xy')

        # if this is the goal node also write that text
        #  and plot optimal path
        if frame == len(self.nodes)-1:

            # convert node to X,Y list
            X = [n.vertices[0] for n in self.optimal]
            Y = [n.vertices[1] for n in self.optimal]
            self.ln, = plt.plot(X,Y)
        
        return self.ln,
