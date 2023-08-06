# Calibration transfer for chemometrics and spectral data applications

This package contains methods to perform calibration transfer based on bilinear models, mainly Partial Least Squares Regression.
Numpy and Sci-Kit Learn are mandatory dependencies

The methods included are:

(Piecewise) Direct Standardization (PDS, DS) (Wang 1991, Bouveresse1996)

Orthogonal projection (EPO transfer) (Zeaiter 2006, Roger 2003)

Domain invariant PLS (Nikzad-Langerodi 2018)

Joint Y PLS (Folch-Fortuny 2017, Garcia Munoz 2005)

To start using this package and get the documentation of the methods, do:

```python
import pycaltransfer.caltransfer as caltransfer
help(caltransfer.ds_pc_transfer_fit)
help(caltransfer.pds_pls_transfer_fit)
help(caltransfer.epo_fit)
help(caltransfer.jointypls_regression)
help(caltransfer.slope_bias_correction)
help(caltransfer.nipals_dipls)
```
