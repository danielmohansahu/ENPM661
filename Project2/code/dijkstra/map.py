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
        return self.is_in_workspace(pt, buffer_) and not self.is_obstacle(pt, buffer_)

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

class TestMap(Map):
    def __init__(self):
        super().__init__([0,0],[200,100])

        # add obstacles
        self.obstacles = [
            Polygon([[90,40],[90,60],[110,60],[110,40],[90,40]]),
            Circle((160,50), 15)
        ]

class FinalMap(Map):
    def __init__(self):
        super().__init__([0,0],[300,200])
        
        # add obstacles
        self.obstacles = [
            Polygon([[20,120],[25,185],[75,185],[100,150],[75,120],[50,150],[20,120]]),
            Polygon([[95,30],[95-75*np.cos(np.radians(30)), 30+75*np.sin(np.radians(30))],
                     [95-75*np.cos(np.radians(30))+10*np.cos(np.radians(60)), 
                        30+75*np.sin(np.radians(30))+np.sin(np.radians(60))],
                     [95+10*np.cos(np.radians(60)), 30+10*np.sin(np.radians(60))],[95,30]]),
            Ellipse((150,100),40,20),
            Circle((225,150),25),
            Polygon([[200,25],[225,40],[250,25],[225,10],[200,25]])
        ]
