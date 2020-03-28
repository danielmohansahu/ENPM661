# convenience class for all parameters

class Options:
    # required arguments
    start               = None
    goal                = None
    rpm                 = None
    clearance           = None
    
    # fixed constants
    radius              = 0.354/2
    wheel_radius        = 0.076/2
    wheel_separation    = 0.3175 # estimate
    timestep            = 1/10
    # @TODO resolution should be a function of timestep / RPM
    resolution          = [0.05, 0.05, 15]

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
