"""Obstacle map
"""
import cv2
import numpy as np
import matplotlib.path as mplPath

# placeholder
class Map:
    def __init__(self, xbounds=[0, 300], ybounds=[0, 200]):
        self.xbounds = xbounds
        self.ybounds = ybounds

    def isvalid(self, vertex):
        # return true if the given vertex is not an obstacle and is
        #  within the workspace bounds
        return ((self.xbounds[0] < vertex[0] < self.xbounds[1]) and (self.ybounds[0] < vertex[1] < self.ybounds[1]))

    # Drawing the obstacles and returning true if the vertex is not an obstacle
    def obstacles(x,y):

        BlankImage = 255 * np.ones(shape=[200, 300, 3], dtype=np.uint8)
        # Window name in which image is displayed
        map = 'Final Map'

        # Circular Obstacle
        CirCenter = (225, 50) # Center coordinates of the circular obstacle
        r = 25 # Radius of circular obstacle
        Color = (0, 0, 0) # black color for the obstacle outline
        # Draw a circular obstacle on the map
        cv2.circle(BlankImage, CirCenter, r, Color, -1)

        # Elliptical Obstacle
        ElCenter = (150, 100) # Center coordinates of the ellipse shaped obstacle
        ElMajor = 40 # Major axis length of the ellipse
        ElMinor = 20 # Minor axis length of the ellipse
        # Draw an ellipse shaped obstacle on the map
        cv2.ellipse(BlankImage, ElCenter, (ElMajor, ElMinor), 0, 0, 360, 0, -1)

        # Polygon Obstacle
        poly = np.array([[20, 80], [25, 15], [75, 15], [100, 50], [75,80], [50,50]], np.int32) # Vertices of the polygon
        # Draw the polygon, True indicates it is a closed line polygon
        cv2.polylines(BlankImage, [poly], True, Color)
        cv2.fillPoly(BlankImage, [poly], (0,0,0))

        # Diamond shaped obstacle
        Diamond = np.array([[225,190], [250,175], [225,160], [200,175]], np.int32) # Vertices of the diamond
        # Draw the diamond shaped obstacle
        cv2.polylines(BlankImage,[Diamond], True, Color)
        cv2.fillPoly(BlankImage,[Diamond], color=(0, 0, 0))

        # The rectangular obstacle
        for a in range(200):
            for b in range(300):
                j = a;
                i = 200 - b
                if i - (1.73) * j + 135 > 0 and i + (0.58) * j - 96.35 <= 0 and i - (1.73) * j - 15.54 <= 0 and i + (0.58) * j - 84.81 >= 0:
                    BlankImage[b, a] = (0, 0, 0)

        def PointInsidePolygon(x, y, poly):
            n = len(poly)
            inside = False
            p1x, p1y = poly[0]
            for i in range(n + 1):
                p2x, p2y = poly[i % n]
                if y > min(p1y, p2y):
                    if y <= max(p1y, p2y):
                        if x <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                                if p1x == p2x or x <= xinters:
                                    inside = not inside
                    p1x, p1y = p2x, p2y
            #print("Polygon",inside)
            # If inside == True, then the point is inside the polygon
            if inside == False:
                return False
            else:
                return True

        # Displaying the final map with obstacles
        # cv2.imshow(map, BlankImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # If the vertices are inside the polygon returns true
        InPolygon = PointInsidePolygon(x, y, poly)
        #print("InPolygon", InPolygon)
        InDiamond = PointInsidePolygon(x, y, Diamond)
        #print("InDiamond", InDiamond)

        # Equation of a circle is x**2 + y**2 = r**2, If we have x**2 + y**2 > r**2, vertex is not an obstacle
        # Equation of an ellipse is (x**2 / a**2) + (y**2 / b**2) = 1, If we have (x**2 / a**2) + (y**2 / b**2) > 1, vertex is not an obstacle

        if (((x** 2 + y** 2) > r ** 2) and (((x**2 / ElMajor**2) + (y**2 / ElMinor**2)) > 1) and (InPolygon == False) and (InDiamond == False)):
            #print(x,y)
            return True
        elif(y - (1.73) * x + 135 > 0 and y + (0.58) * x - 96.35 <= 0 and y - (1.73) * x - 15.54 <= 0 and y + (0.58) * x - 84.81 >= 0):
            return False
        #print(x,y)
        return False

    # Function call - (10,190) is not an obstacle and (10,10) is an obstacle
    # test = obstacles(10,190)
    # print(test)

