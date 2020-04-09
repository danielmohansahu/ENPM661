# convenience class for all parameters

class Options:
    # required arguments
    start               = None      # [meters, meters, degrees]
    goal                = None      # [meters, meters]
    rpm                 = None      # [rot/min, rot/min]
    clearance           = None      # meters
    visualize           = None      # bool
    
    # fixed constants (taken from turtlebot3 URDF)
    radius              = 0.354/2   # meters
    wheel_radius        = 0.033     # meters
    wheel_separation    = 0.16      # meters (estimate)
    timestep            = 1.0/120   # minutes

    def __init__(self, start, goal, rpm, clearance, visualize):
        if not len(start) == 3:
            raise RuntimeError("Invalid start node: {}".format(start))
        if not len(goal) == 2:
            raise RuntimeError("Invalid start node: {}".format(start))
        if not len(rpm) == 2:
            raise RuntimeError("Invalid start node: {}".format(start))
        self.start = start
        self.goal = goal
        self.rpm = rpm
        self.clearance = clearance
        self.visualize = visualize
