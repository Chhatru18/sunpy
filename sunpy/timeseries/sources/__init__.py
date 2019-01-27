"""
This module provies a collection of Datasource-specific classes.

This is where datasource specific logic is implemented. Each mission should have its own file with
one or more classes defined. Typically, these classes will be subclasses of the `sunpy.TimeSeries`
class.
"""
from sunpy.timeseries.sources.eve import EVESpWxTimeSeries
from sunpy.timeseries.sources.fermi_gbm import GBMSummaryTimeSeries
from sunpy.timeseries.sources.goes import XRSTimeSeries
from sunpy.timeseries.sources.lyra import LYRATimeSeries
from sunpy.timeseries.sources.noaa import NOAAIndicesTimeSeries, NOAAPredictIndicesTimeSeries
from sunpy.timeseries.sources.norh import NoRHTimeSeries
from sunpy.timeseries.sources.rhessi import RHESSISummaryTimeSeries

__all__ = ['EVESpWxTimeSeries', 'XRSTimeSeries', 'NOAAIndicesTimeSeries',
           'NOAAPredictIndicesTimeSeries', 'LYRATimeSeries', 'NoRHTimeSeries',
           'RHESSISummaryTimeSeries', 'GBMSummaryTimeSeries']
