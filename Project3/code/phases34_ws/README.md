# A\* Search

## Overview

This codebase uses the A\* search algorithm to find an optimal path from a start node to a goal node. The resulting path (and search space) are then visualized.

## Usage

In order to run the search with default options, simply call:

```bash
./astar_rigid.py
```

A number of user configurable options are available. For example, the following searches the same graph with a robot radius of 2 for a goal node of `[100 100 60]`:

```bash
./astar_rigid.py -r 2 -g 100 100 60
```

The full list of potential arguments is:
```
$ /astar_rigid.py --help
usage: astar_rigid.py [-h] [-s START [START ...]] [-g GOAL [GOAL ...]]
                [-c CLEARANCE] [-r RADIUS] [-S STEP_SIZE] [-t THETA_RES]
                [-x X_RES] [-y Y_RES]

Solve for an optimal path via A*.

optional arguments:
  -h, --help            show this help message and exit
  -s START [START ...], --start START [START ...]
                        Starting node indices.
  -g GOAL [GOAL ...], --goal GOAL [GOAL ...]
                        Goal node indices.
  -c CLEARANCE, --clearance CLEARANCE
                        Obstacle avoidance clearance.
  -r RADIUS, --radius RADIUS
                        Robot radius.
  -S STEP_SIZE, --step-size STEP_SIZE
                        Movement step size.
  -t THETA_RES, --theta-res THETA_RES
                        Theta movement resolution.
  -x X_RES, --x-res X_RES
                        X movement resolution.
  -y Y_RES, --y-res Y_RES
                        Y movemement resolution.
```

## Dependencies

This code uses Python3 with the following external modules:

 - matplotlib
 - numpy

These can be installed via:
```bash
pip install matplotlib numpy
```

We also require the `ffmpeg` library to generate the output video. On Ubuntu this can be installed via:
```bash
sudo apt install ffmpeg
```
