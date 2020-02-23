#!/usr/bin/env python3

from random import sample, randrange
from collections import defaultdict
import numpy as np
from dijkstra.dijkstra import Dijkstra

if __name__ == "__main__":
    # dummy graph (for testing)
    g = {
        (1,2): {
            (2,3): {(3,4)},
            (5,4): {(3,5)}
        }
    }
    d = Dijkstra()

    import code
    code.interact(local=locals())
