"""
This module provides errors/exceptions and warnings of general use for SunPy.

Exceptions that are specific to a given subpackage should *not* be here, but rather in the
particular subpackage.
"""

__all__ = ["SunpyWarning", "SunpyUserWarning", "SunpyDeprecationWarning"]


class SunpyWarning(Warning):
    """
    The base warning class from which all Sunpy warnings should inherit.
    """


class SunpyUserWarning(UserWarning, SunpyWarning):
    """
    The primary warning class for Sunpy.

    Use this if you do not need a specific sub-class.
    """


class SunpyDeprecationWarning(SunpyWarning):
    """
    A warning class to indicate a deprecated feature.
    """
