"""Obstacle classes (for easy map generation).
"""

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.path as mplPath
from matplotlib import patches

class Obstacle(ABC):
    """Base Obstacle class; defines API"""
    def __init__(self):
        ...

    def __contains__(self, val):
        # convenience python magic to use the "in" method
        return self.within(val)

    @abstractmethod
    def within(self,pt,buffer_):
        """Return True if the given point is within the Obstacle."""
        ...
    
    @abstractmethod
    def plot(self):
        """Plot self."""
        ...

class Polygon(Obstacle):
    def __init__(self, pts):
        super().__init__()
        self.pts = mplPath.Path(np.array(pts))

    def within(self, pt, buffer_=0):
        return self.pts.contains_point(pt, radius=-(buffer_+1))

    def plot(self, ax):
        e = patches.Polygon(xy=self.pts.vertices)
        ax.add_artist(e)
        e.set_facecolor('k')

class Ellipse(Obstacle):
    def __init__(self, center, major, minor):
        super().__init__()
        self.center = center
        self.major = major
        self.minor = minor

    def within(self, pt, buffer_=0):
        # check if the equality is satisfied
        # https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
        val = ((pt[0]-self.center[0])/(self.major+2*buffer_))**2.0 + ((pt[1]-self.center[1])/(self.minor+2*buffer_))**2.0
        return val <= 1

    def plot(self, ax):
        e = patches.Ellipse(xy=self.center,width=self.major,height=self.minor)
        ax.add_artist(e)
        e.set_facecolor('k')

class Circle(Ellipse):
    def __init__(self, center, radius):
        super().__init__(center, radius, radius)
