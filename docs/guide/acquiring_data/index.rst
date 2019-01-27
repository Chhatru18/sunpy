.. _acquiring_data:

*************************
Acquiring Data with SunPy
*************************

In this section of the guide we will introduce the ways you can obtain different
kind of solar data from different places.

This submodule contains many layers. Most
users should use `Fido <sunpy.net.fido_factory.UnifiedDownloaderFactory>`, which
is an interface to multiple sources including all the sources implemented in
`~sunpy.net.dataretriever` as well as `~sunpy.net.vso` and `~sunpy.net.jsoc`.
Fido ~`sunpy.net.fido_factory.UnifiedDownloaderFactory` can be used like so::

    >>> from sunpy.net import Fido, attrs as a
    >>> results = Fido.search(a.Time("2012/1/1", "2012/1/2"), a.Instrument('lyra'))  # doctest: +REMOTE_DATA
    >>> files = Fido.fetch(results)  # doctest: +SKIP


.. toctree::
    :maxdepth: 2

    sample-data
    fido
    jsoc
    hek
    helioviewer
    database
