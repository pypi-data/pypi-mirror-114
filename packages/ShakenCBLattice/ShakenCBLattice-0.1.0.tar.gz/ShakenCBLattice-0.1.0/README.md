# ShakenCBLattice

This repo contains codes for looking at band structures of Shaken Checkerboard Optical lattices.

## Installation
`pip install ShakenCBLattice`

## Usage

Currently there are two classes that can be instantiated, `CheckerboardLattice` and `ExtendedBasisLattice`.  The latter inherits from the former, so here I will go over some basics of the ExtendedBasisLattice class.

The general usage is:

```python
from ShakenCBLattice.ExtendedBasisLattice import ExtendedBasisLattice
eb = ExtendedBasisLattice(Vtotal, Ratio, n_lattice, Frequency, K0, nFloquetBasis, Ellipse_factor)
```
Where
  * Vtotal : Total lattice depth
  * Ratio : Ratio of in plane lattice depth to out of plane lattice depth
  * n_lattice : Number of fourier plane waves to truncate.  Since this is a 2D Matrix, the number of basis states will be (2 n_lattice+1 x 2 n_lattice+1)
  * Frequency : Frequency of the periodic driving
  * K0 : Dimensionless driving strength.
  * nFloquetBasis : Number of floquet blocks to include in the calculation.  Matrix will be block diagonal with (2 nFloquetBasis + 1 x 2 nFloquetBasis + 1) shape
  * Ellipse_Factor : Ratio of x motion to y motion.  A factor of 1 indicates a circle while 0 will be a 1D drive.
