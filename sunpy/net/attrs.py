"""
This module provides a cleaner import namespace for all attrs.
"""
from .dataretriever.attrs import goes
from .jsoc import attrs as jsoc
from .vso import attrs as vso
from .vso.attrs import Instrument, Level, Sample, Time, Wavelength

__all__ = ['Time', 'Instrument', 'Wavelength', 'Level', 'Sample', 'vso', 'jsoc', 'goes']
