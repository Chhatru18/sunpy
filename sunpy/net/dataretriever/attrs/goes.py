"""
This module provides the SatelliteNumber Attr for the GOES client.
"""

from sunpy.net.attr import SimpleAttr

__all__ = ['SatelliteNumber']


class SatelliteNumber(SimpleAttr):
    """
    The GOES Satellite Number.
    """
