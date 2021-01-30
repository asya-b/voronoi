# voronoi
Code to generate Voronoi nearest-neighbour density images like:

![example figure](https://github.com/asya-b/voronoi/blob/main/images/300neighbors.png?raw=true)

## Required Modules and Libraries:

  time, copy, sys, numpy, scipy, matplotlib

## Usage:

`python voronoi.py example_points.npy example_probabilities.npy`

Running the command as given will produce images/2neighbours.png (identical to images/example_figure.png), however the .npy files may be replaced as follows:

  - example_points.npy:
      - *ndarray of floats, shape (npoints, 2)*
      - Coordinates of each particle point
  - example_probabilities.npy:
      - *ndarray of floats, shape (npoints,)*
      - Probabilities of each particle to represent a star. See https://github.com/rerrani/nbopy/blob/master/npaint.py for a routine to calculate these probabilities for an N-body halo.

Within voronoi.py, one may customise the following:

- *ln. 32* -------------- number of nearest neighbours
- *ln. 34* -------------- lower cutoff
- *ln. 106* ------------ colormap
- *ln. 113 - 128* ----- figure size, limits, labels, etc.
