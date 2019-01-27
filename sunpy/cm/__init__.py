"""
The following colormaps are provided by this module:
"""
from sunpy.cm.cm import *

for cmname in cmlist.keys():
    __doc__ += "\n* '`~sunpy.cm.cm.{}`'\n".format(cmname)
