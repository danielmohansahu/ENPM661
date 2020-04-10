# A\* Search and Visualization

## Overview

This ROS package wraps a Python package that uses the A\* search algorithm to find an optimal path from a given start node to a given goal node. The resulting path navigation can be simulated in gazebo or simply output to a video.

## Building

This is a ROS package that has been tested against ROS Melodic on Ubuntu 18.04 and should be cross-compatible with ROS Kinetic. To build, run the following in the root of the workspace:

```
catkin_make
```

## Usage

The simplest usage is to run the core planning node without any visualization. This will take start / goal node values from the user and plan a path through the expected obstacle map.

```bash
# load ROS environment
source devel/setup.bash

# call and plan from the given start node [-4,-4,60] 
#   to [4,4] with a clearance of [0.1] and discrete RPM action set of [100,200]:
#   Video output can be enabled with the `-v` flag.
rosrun turtlebot_planner planner.py -s -4 -4 60 -g 4 4 -r 100 200 -c 0.1
```

The full list of potential arguments is:
```
rosrun turtlebot_planner planner.py -h
```

The planned path can be simulated via an example launch file. To simulate, run the following:

```bash
source devel/setup.bash
roslaunch turtlebot_planner plan.launch
```

Note that the same arguments are available here but are named differently for various reasons. To see them, call:

```bash
roslaunch turtlebot_planner plan.launch --ros-args
```

## Dependencies

This code a ROS installation (Kinetic, Melodic) and Gazebo. The only external ros package is the set of turtlebot gazebo packages. These can be installed vis:

```bash
sudo apt-get install ros-{ROSDISTRO}-turtlebot3
```

We also require the `ffmpeg` library to generate the output video. On Ubuntu this can be installed via:
```bash
sudo apt install ffmpeg
```
