# Dijkstra Search

## Usage:

The code to solve for a Point Robot can be run via:

```bash
./dijkstra_point.py
```

The corresponding code for a rigid robot can be run via:

```bash
./dijkstra_rigid.py
```

Both scripts will attempt to solve the same path problem of determining 
an optimal path through the given FinalMap. They will then visualize the 
search process (which can be quite slow).

## Dependencies:

This code is written in Python3 and uses `matplotlib` and `numpy` as external dependencies. These can be installed via:

```bash
pip install numpy matplotlib
```

## Benchmarking:

On a Lenovo IdeaPad running Ubuntu 18.04 with AMD A9-9425 processor this code took about 30 seconds to solve. The visualization took much longer.


