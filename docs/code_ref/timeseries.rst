.. _sunpy-timeseries:

****************
SunPy timeseries
****************

This package provides a datatype for 1D time series data, replacing the SunPy LightCurve module.

Currently the objects can be instansiated from files (such as CSV and FITS) and urls to these files.
However, they do not include data downloaders for their specific instruments as this will become part of the universal downloader.

.. automodapi:: sunpy.timeseries
   :no-inheritance-diagram:

.. automodapi:: sunpy.timeseries.metadata
   :no-inheritance-diagram:

.. automodapi:: sunpy.timeseries.timeseries_factory
   :no-inheritance-diagram:

.. automodapi:: sunpy.timeseries.sources
   :no-inheritance-diagram:
