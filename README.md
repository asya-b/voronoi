# voronoi
Code to generate Voronoi nearest-neighbour density images like:

![](/home/asya/Documents/Research/mProject/Images/Fornax/voronoi/e-06/300neighbors.png)

## Required Modules and Libraries:

​	time, copy, sys, numpy, scipy, matplotlib

## Usage:

`python voronoi.py example_points.npy example_probabilities.npy`

Running the command as given will produce example_figure.png, however the .npy files may be replaced as follows:

  - example_points.npy:
        - *ndarray of floats, shape (npoints, 2)*
      - Coordinates of each particle point
  - example_probabilities.npy:
        - *ndarray of floats, shape (npoints,)*
      - Probabilities of each particle to represent a star. See https://github.com/rerrani/nbopy/blob/master/npaint.py for a routine to calculate these probabilities for an N-body halo.

Within voronoi.py, one may customise the following:

- number of nearest neighbours		*ln. 32*
- lower cutoff										 *ln. 34*
- colormap 											*ln. 106*
- figure size, limits, labels, etc. 		*ln. 113 - 128*