"""Visualization Tools
"""

from .node import Node
from matplotlib import pyplot as plt

def plot_path(path):
    """Visualize the given path.

    Args:
        path: A list of Node objects.
    """
    # convert node to X,Y list
    X = [n.vertices[0] for n in path]
    Y = [n.vertices[1] for n in path]

    plt.plot(X,Y)
    plt.show()



def plot_workspace(workspace):
    """@TODO
    """
    ...



