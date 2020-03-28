"""Obstacle map
"""

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.path as mplPath
from matplotlib import pyplot as plt
from .obstacle import Polygon,Ellipse,Circle

class Map(ABC):
    """A base class used to define workspace bounds and obstacles."""
    def __init__(self, min_corner, max_corner):
        # The minimum and maximum bounds of our workspace
        self.min_corner = np.array(min_corner)
        self.max_corner = np.array(max_corner)
        self.xbounds = [self.min_corner[0], self.max_corner[0]]
        self.ybounds = [self.min_corner[1], self.max_corner[1]]
        self.workspace = mplPath.Path(np.array([
            min_corner, 
            [max_corner[0],min_corner[1]],
            max_corner,
            [min_corner[0],max_corner[1]],
            min_corner
        ]))

    def is_in_workspace(self, pt, buffer_=0):
        """Returns True if the given point is within our workspace."""
        return self.workspace.contains_point(pt, radius=-(buffer_+1))

    def is_valid(self, pt, buffer_=0):
        """Returns True if the given point is within our workspace and not an obstacle."""
        xy = pt[:2]
        return self.is_in_workspace(xy, buffer_) and not self.is_obstacle(xy, buffer_)

    def is_obstacle(self, pt, buffer_=0):
        """Returns True if the given point is in an obstacle."""
        return any([obstacle.within(pt,buffer_) for obstacle in self.obstacles])

    def plot(self):
        """Plot our workspace (with obstacles)"""
        fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})

        # plot the workspace
        ws_verts = self.workspace.vertices
        plt.plot(ws_verts[:,0],ws_verts[:,1],'k')

        # plot the obstacles
        for obstacle in self.obstacles:
            obstacle.plot(ax)

        return fig,ax

class FinalMap(Map):
    def __init__(self):
        super().__init__([-5,-5],[5,5])
        
        # add obstacles
        self.obstacles = [
            Polygon([[-2.75,3.75],[-1.25,3.75],[-1.25,2.25],[-2.75,2.25]]),
            Circle((2,3),2),
            Polygon([[-4.75,-0.75],[-4.75,0.75],[-3.25,0.75],[-3.25,-0.75]]),
            Circle((0,0),2),
            Polygon([[3.25,-0.75],[3.25,0.75],[4.75,0.75],[4.75,-0.75]]),
            Circle((-2,-3),2),
            Circle((2,-3),2)
        ]
