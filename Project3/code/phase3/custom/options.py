# convenience class for all parameters

class Options:
    start               = [-4,-4,60]
    goal                = [4,4]
    rpm                 = [100, 100]
    clearance           = 0.1
    radius              = 0.1
    wheel_radius        = 0.076/2
    wheel_separation    = 0.354
    timestep            = 0.1
    resolution          = [0.1,0.1,30]
    def __init__(self, start, goal, rpm, clearance):
        if not len(start) == 3:
            raise RuntimeError("Invalid start node: {}".format(start))
        if not len(goal) == 2:
            raise RuntimeError("Invalid start node: {}".format(start))
        if not len(rpm) == 2:
            raise RuntimeError("Invalid start node: {}".format(start))
        self.start = start
        self.goal = goal
        self.clearance = clearance
