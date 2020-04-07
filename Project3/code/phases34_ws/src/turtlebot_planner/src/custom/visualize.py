"""Visualization Tools
"""

import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from .node import Node

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
        self.x_data = [self.nodes[i].vertices[0] for i in range(len(self.nodes)-1)]
        self.y_data = [self.nodes[i].vertices[1] for i in range(len(self.nodes)-1)]
        self.u_data = [0]*len(self.x_data)
        self.v_data = [0]*len(self.x_data)

        self.ln = self.ax.quiver(
            self.x_data,
            self.y_data,
            self.u_data,
            self.v_data, 
            color='b', 
            angles='xy',
            scale=10)

        # misc variables
        self.max_size = 500

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
                blit=False)

        if save and "ffmpeg" in writers.list():
            # save to a local video file
            print("Saving video to `results.mp4`...")
            Writer = writers["ffmpeg"]
            writer = Writer(fps=100, metadata=dict(artist="Me"), bitrate=1800)
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
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('='*int(20*frame/len(self.nodes)), int(100*frame/len(self.nodes))))
        sys.stdout.flush()

        if frame == len(self.nodes)-1:
            # convert node to X,Y list
            X = [n.vertices[0] for n in self.optimal]
            Y = [n.vertices[1] for n in self.optimal]
            self.ln, = plt.plot(X,Y)
            return self.ln,

        # update X/Y data and plot 
        self.u_data[frame] = self.nodes[frame+1].vertices[0]-self.nodes[frame].vertices[0]
        self.v_data[frame] = self.nodes[frame+1].vertices[1]-self.nodes[frame].vertices[1]
        
        # set updated data
        self.ln.set_UVC(self.u_data, self.v_data)
        return self.ln,
