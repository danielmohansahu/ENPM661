"""Obstacle map
"""

#placeholder
class Map:
    def __init__(self, xbounds=[0,100], ybounds=[0,100]):
        self.xbounds = xbounds
        self.ybounds = ybounds

    def isvalid(self, vertex):
        # return true if the given vertex is not an obstacle and is
        #  within the workspace bounds
        return (self.xbounds[0] < vertex[0] < self.xbounds[1]) and (self.ybounds[0] < vertex[1] < self.ybounds[1])
