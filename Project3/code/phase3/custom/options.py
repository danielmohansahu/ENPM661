# convenience class for all parameters

class Options:
    # required arguments
    start               = None      # [meters, meters, degrees]
    goal                = None      # [meters, meters]
    rpm                 = None      # [rot/min, rot/min]
    clearance           = None      # meters
    
    # fixed constants
    radius              = 0.354/2   # meters
    wheel_radius        = 0.076/2   # meters
    wheel_separation    = 0.3175    # meters (estimate)
    timestep            = 1/15      # minutes

    def __init__(self, start, goal, rpm, clearance):
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
