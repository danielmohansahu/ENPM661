# ENPM661 Project #1

This repository contains a Python implementation of a Brute Force Search (BFS) to 
determine the optimal solution to the 8-Puzzle problem (a gentler version of the [15 Puzzle Problem](https://en.wikipedia.org/wiki/15_puzzle)).

Technically this code supports solving any sized puzzle of this class (e.g. 15, 24, 35, etc.). But due to the prohibitively high runtimes this has not been tested beyond the 8 puzzle problem.

## Usage

The simplest case is to run the solver against a randomly generated start node, as such:
```shell
./solve.py
```

Alternatively, one can supply an arbitrary starting node:
```shell
./solve.py -s 2 1 3 4 5 6 7 8 0
```

Both calls should result in similar output:
```shell
$ ./solve.py
Goal node: 1 4 7 2 5 8 3 6 0
Start node: 6 0 2 3 8 4 5 1 7
Success found!
Success found!
Tree traversed in 18.416 seconds
Optimal solution length: 24
```

The optimal path found is output to a local `nodePath.txt` file, along with more information about all the nodes traversed. Visualization of the optimal path can be accomplished via the following (assuming a `nodePath.txt` file is in the same folder as the script.)
```bash
python plot_path.py
```

## Dependencies

This project requires Python3 with the Numpy module. It has been tested on Ubuntu 16.04 in a virtual environment, but should be theoretically extensible to any system capable of running Python3.
