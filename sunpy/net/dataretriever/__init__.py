"""
This module provides a framework for downloading data from "simple" web sources such as HTTP or FTP
servers.

Although it could be used for more complex services as well. Following the example of `sunpy.map`
and `sunpy.timeseries` this module provides a base class `~sunpy.net.dataretriever.GenericClient`
from which specific services can subclass. All these subclasses are then registered with the `Fido
<sunpy.net.fido_factory.UnifiedDownloaderFactory>` factory class, so do not need to be called
individually.
"""

from .client import GenericClient, QueryResponse, QueryResponseBlock
from .sources.eve import EVEClient
from .sources.goes import XRSClient
from .sources.lyra import LYRAClient
from .sources.noaa import NOAAIndicesClient, NOAAPredictClient, SRSClient
from .sources.norh import NoRHClient
from .sources.rhessi import RHESSIClient

__all__ = ['QueryResponseBlock', 'QueryResponse', 'GenericClient',
           'EVEClient', 'XRSClient', 'LYRAClient', 'NOAAIndicesClient',
           'NOAAPredictClient', 'NoRHClient', 'RHESSIClient', 'SRSClient']
