.. _units-coordinates-sunpy:

Units and Coordinates in SunPy
******************************

This section of the guide will talk about representing physical units and
physical coordinates in SunPy. SunPy makes use of :ref:`Astropy <astropy:astropy-coordinates>` for
both these tasks.


Units in SunPy
==============

All functions in SunPy that accept or return numbers associated with physcial
quantities accept and return `~astropy.units.Quantity` objects. These objects
represent a number (or an array of numbers) and a unit. This means SunPy is
always explicit about the units associated with a value. Quantities and units
are powerful tools for keeping track of variables with a physical meaning and
make it straightforward to convert the same physical quantity into different units.

In this section of the guide we will give a quick introduction to `astropy.units`
and then demostrate how to use units with SunPy.

To use units we must first import them from Astropy. To save on typing we usually
import units as ``u``::

   >>> import astropy.units as u

Once we have imported units we can create a quantity by multiplying a number by
a unit::

   >>> length = 10 * u.meter
   >>> length
   <Quantity 10. m>

A `~astropy.units.Quantity` has both a ``.unit`` and a ``.value`` attribute::

  >>> length.value
  10.0

  >>> length.unit
  Unit("m")

These `~astropy.units.Quantity` objects can also be converted to other units, or
unit systems::

  >>> length.to(u.km)
  <Quantity 0.01 km>

  >>> length.cgs
  <Quantity 1000. cm>

Probably most usefully, `~astropy.units.Quantity` objects will propogate units
through arithmetic operations when appropriate::

  >>> distance_start = 10 * u.mm
  >>> distance_end = 23 * u.km
  >>> length = distance_end - distance_start
  >>> length
  <Quantity 22.99999 km>

  >>> time = 15 * u.minute
  >>> speed = length / time
  >>> speed
  <Quantity 1.53333267 km / min>

However, operations which do not make physical sense for the units specified will cause an error::

  >>> length + time
  Traceback (most recent call last):
  ...
  astropy.units.core.UnitConversionError: Can only apply 'add' function to quantities with compatible dimensions


Quantities as function arguments
================================

An extremely useful addition to the base functionality of Quanitities is the ``@u.quantity_input`` decorator.
This allows you to specify required units for function arguments to ensure that the calculation within that
function always make physical sense. For instance, if we defined a function to calculate speed as above,
we might want the distance and time as inputs::

  >>> def speed(length, time):
  ...     return length / time

However, this requires that length and time both have the appropriate units. We therefore want to use
`~astropy.units.quantity_input` to enforce this, here we use
`function annotations <https://python-3-for-scientists.readthedocs.io/en/latest/python3_features.html#function-annotations>`__
to specify the units.

  >>> @u.quantity_input
  ... def speed(length: u.m, time: u.s):
  ...     return length / time

Now, when this function is called, if the units of length and time are not convertible to the units specified,
an error will be raised stating that the units are incorrect or missing::

  >>> speed(1*u.m, 10*u.m)
  Traceback (most recent call last):
  ...
  astropy.units.core.UnitsError: Argument 'time' to function 'speed' must be in units convertible to 's'.

  >>> speed(1*u.m, 10)
  Traceback (most recent call last):
  ...
  TypeError: Argument 'time' to function 'speed' has no 'unit' attribute. You may want to pass in an astropy Quantity instead.

Note that the units of the inputs do not have to be exactly the same as those in the function definition, as long
as they can be converted to those units. So for instance, passing in a time in minutes still works even though we
specified `time: u.s`::

  >>> speed(1*u.m, 1*u.minute)
  <Quantity 1. m / min>

This may still not be quite as we want it, since we wanted the input time in seconds but the output is in m/min.
We can correct this by defining the function with an additional annotation::

  >>> @u.quantity_input
  ... def speed(length: u.m, time: u.s) -> u.m/u.s:
  ...     return length / time

This will force the output of the function to be converted to m/s before returning, so that you will always
have the same units on the output from this function::

  >>> speed(1*u.m, 1*u.minute)
  <Quantity 0.01666667 m / s>

Physical Coordinates in SunPy
=============================

In much the same way as `~astropy.units` are used for representing physical
quantities, SunPy uses `astropy.coordinates` to represent points in physical
space. This applies to both points in 3D space and projected coordinates in
images.

The astropy coordinates module is primarily used through the
`~astropy.coordinates.SkyCoord` class::

  >>> from astropy.coordinates import SkyCoord

To enable the use of the solar physics specific frames defined in SunPy we also
need to import them::

  >>> from sunpy.coordinates import frames

A SkyCoord object to represent a point on the Sun can then be created::

  >>> c = SkyCoord(70*u.deg, -30*u.deg, obstime="2017-08-01",
  ...              frame=frames.HeliographicStonyhurst)
  >>> c
  <SkyCoord (HeliographicStonyhurst: obstime=2017-08-01T00:00:00.000): (lon, lat, radius) in (deg, deg, km)
      (70., -30., 695508.)>

This `~astropy.coordinates.SkyCoord` object can then be transformed to any
other coordinate frame defined either in Astropy or SunPy, for example::

  >>> c.transform_to(frames.Helioprojective)
  <SkyCoord (Helioprojective: obstime=2017-08-01T00:00:00.000, rsun=695508.0 km, observer=<HeliographicStonyhurst Coordinate for 'earth'>): (Tx, Ty, distance) in (arcsec, arcsec, km)
      (769.74997696, -498.75932128, 1.51668819e+08)>


It is also possible to convert three dimensional positions to astrophysical
frames defined in Astropy, for example `~astropy.coordimates.ICRS`.

  >>> c.transform_to('icrs')
  <SkyCoord (ICRS): (ra, dec, distance) in (deg, deg, km)
    (49.85053118, 0.05723938, 1417577.0297545...)>



Observer Location
-----------------

Both `~sunpy.coordinates.frames.Helioprojective` and
`~sunpy.coordinates.frames.Heliocentric` frames are defined based on the
position of the observer. Therefore to transform either of these frames to a
different frame the location of the observer must be known. The default
observer is the Earth. A different observer can be specified for a coordinate
object using the ``observer`` argument to `~astropy.coordinates.SkyCoord`.
For SunPy to calculate the location of the Earth, it must know the time for
which the coordinate is valid; this is specified with the ``obstime`` argument.

Using the observer location it is possible to convert a coordinate as seen by
one observer to a coordinate seen by another::

  >>> hpc1 = SkyCoord(0*u.arcsec, 0*u.arcsec, observer="earth",
  ...                 obstime="2017-07-26",
  ...                 frame=frames.Helioprojective)

  >>> hpc1.transform_to(frames.Helioprojective(observer="venus",
  ...                                          obstime="2017-07-26"))
  <SkyCoord (Helioprojective: obstime=2017-07-26T00:00:00.000, rsun=695508.0 km, observer=<HeliographicStonyhurst Coordinate for 'venus'>): (Tx, Ty, distance) in (arcsec, arcsec, km)
    (-1285.11970265, 106.17983302, 1.08317783e+08)>


Using Coordinates with SunPy Map
--------------------------------

.. plot::
   :include-source:

   SunPy Map uses coordinates to specify locations on the image, and to plot
   overlays on plots of maps. When a Map is created, a coordinate frame is
   constructed from the header information. This can be accessed using
   ``.coordinate_frame``:

   >>> import sunpy.map
   >>> from sunpy.data.sample import AIA_171_IMAGE   # doctest: +REMOTE_DATA
   >>> m = sunpy.map.Map(AIA_171_IMAGE)  # doctest: +REMOTE_DATA
   >>> m.coordinate_frame  # doctest: +REMOTE_DATA
   <Helioprojective Frame (obstime=2011-06-07T06:33:02.770, rsun=696000000.0 m, observer=<HeliographicStonyhurst Coordinate (obstime=2011-06-07T06:33:02.770): (lon, lat, radius) in (deg, deg, m)
        (0., 0.048591, 1.51846026e+11)>)>

   This can be used when creating a `~astropy.coordinates.SkyCoord` object to set
   the coordinate system to that image:

   >>> from astropy.coordinates import SkyCoord
   >>> import astropy.units as u
   >>> c = SkyCoord(100 * u.arcsec, 10*u.arcsec, frame=m.coordinate_frame)  # doctest: +REMOTE_DATA
   >>> c  # doctest: +REMOTE_DATA
   <SkyCoord (Helioprojective: obstime=2011-06-07T06:33:02.770, rsun=696000000.0 m, observer=<HeliographicStonyhurst Coordinate (obstime=2011-06-07T06:33:02.770): (lon, lat, radius) in (deg, deg, m)
       (0., 0.048591, 1.51846026e+11)>): (Tx, Ty) in arcsec
       (100., 10.)>

   This `~astropy.coordinates.SkyCoord` object could then be used to plot a point
   on top of the map:

   >>> import matplotlib.pyplot as plt
   >>> ax = plt.subplot(projection=m)  # doctest: +REMOTE_DATA
   >>> m.plot()  # doctest: +REMOTE_DATA
   <matplotlib.image.AxesImage object at ...>
   >>> ax.plot_coord(c, 'o')  # doctest: +REMOTE_DATA

For more information on coordinates see :ref:`sunpy-coordinates` section of
the :ref:`reference`.

Getting Started
===============

The easiest interface to the coordinates module is through the `~astropy.coordinates.SkyCoord` class::

  >>> import astropy.units as u
  >>> from astropy.coordinates import SkyCoord
  >>> from sunpy.coordinates import frames

  >>> c = SkyCoord(-100*u.arcsec, 500*u.arcsec, frame=frames.Helioprojective)
  >>> c = SkyCoord(x=-72241.0*u.km, y=361206.1*u.km, z=589951.4*u.km, frame=frames.Heliocentric)
  >>> c = SkyCoord(70*u.deg, -30*u.deg, frame=frames.HeliographicStonyhurst)
  >>> c
  <SkyCoord (HeliographicStonyhurst: obstime=None): (lon, lat, radius) in (deg, deg, km)
      (70., -30., 695508.)>

It is also possible to use strings to define the frame but in that case make sure to explicitly import `sunpy.coordinates` as it registers solar coordinate frames with Astropy coordinates::

  >>> import astropy.units as u
  >>> from astropy.coordinates import SkyCoord

  >>> import sunpy.coordinates
  >>> c = SkyCoord(-100*u.arcsec, 500*u.arcsec, frame='helioprojective')
  >>> c
  <SkyCoord (Helioprojective: obstime=None, rsun=695508.0 km, observer=earth): (Tx, Ty) in arcsec
      (-100.,  500.)>

SunPy implements support for the following solar physics coordinate systems:

* Helioprojective (Cartesian) `~sunpy.coordinates.frames.Helioprojective`
* Heliocentric `~sunpy.coordinates.frames.Heliocentric`
* Heliographic Stonyhurst `~sunpy.coordinates.frames.HeliographicStonyhurst`
* Heliographic Carrington `~sunpy.coordinates.frames.HeliographicCarrington`

for a complete description of these frames see `sunpy.coordinates.frames` and for
a more detailed description of the frames see `Thompson (2006). <https://doi.org/10.1051/0004-6361:20054262>`_

`~astropy.coordinates.SkyCoord` and all other `~astropy.coordinates` objects also support array coordinates.
These work the same as single-value coordinates, but they store multiple coordinates in a single object.
When you're going to apply the same operation to many different coordinates, this is a better choice than a list of `~astropy.coordinates.SkyCoord` objects, because it will be
**much** faster than applying the operation to each `~astropy.coordinates.SkyCoord` in a **for** loop::

   >>> c = SkyCoord([-500, 400]*u.arcsec, [100, 200]*u.arcsec, frame=frames.Helioprojective)
   >>> c
   <SkyCoord (Helioprojective: obstime=None, rsun=695508.0 km, observer=earth): (Tx, Ty) in arcsec
       [(-500.,  100.), ( 400.,  200.)]>
   >>> c[0]
   <SkyCoord (Helioprojective: obstime=None, rsun=695508.0 km, observer=earth): (Tx, Ty) in arcsec
       (-500.,  100.)>

Accessing Coordinates
---------------------

Individual coordinates can be accessed via attributes on the `~astropy.coordinates.SkyCoord` object, but the names of the components of the coordinates for each frame differ.
For a full description of all the properties of the frames see `sunpy.coordinates.frames`.

`~sunpy.coordinates.Helioprojective`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the helioprojective frame the coordinates are accessed as ``Tx`` and ``Ty``
representing theta ``x`` and ``y``.
These are the same coordinates that are often referred to as ``solar-x`` and ``solar-y``::

  >>> c = SkyCoord(-500*u.arcsec, 100*u.arcsec, frame=frames.Helioprojective)
  >>> c.Tx
  <Longitude -500. arcsec>
  >>> c.Ty
  <Latitude 100. arcsec>

`~sunpy.coordinates.Heliocentric`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Heliocentric is normally a Cartesian frame so the coordinates are accessed as ``x, y, z``::

  >>> c = SkyCoord(-72241.0*u.km, 361206.1*u.km, 589951.4*u.km, frame=frames.Heliocentric)
  >>> c.x
  <Quantity -72241. km>
  >>> c.y
  <Quantity 361206.1 km>
  >>> c.z
  <Quantity 589951.4 km>

`~sunpy.coordinates.HeliographicStonyhurst` and `~sunpy.coordinates.HeliographicCarrington`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both the heliographic frames use latitude, longitude and radius which are accessed as follows::

   >>> c = SkyCoord(70*u.deg, -30*u.deg, frame=frames.HeliographicStonyhurst)
   >>> c.lat
   <Latitude -30. deg>
   >>> c.lon
   <Longitude 70. deg>
   >>> c.radius
   <Distance 695508. km>

Transforming Between Coordinate Frames
======================================

Both `~astropy.coordinates.SkyCoord` and `~astropy.coordinates.BaseCoordinateFrame` instances have a
`~astropy.coordinates.SkyCoord.transform_to` method.
This can be used to transform the frame to any other frame, either implemented in SunPy or in `Astropy <http://docs.astropy.org/en/stable/coordinates/transforming.html>`_.
An example of transforming the center of the solar disk to Carrington coordinates is::

   >>> c = SkyCoord(0*u.arcsec, 0*u.arcsec, frame=frames.Helioprojective, obstime="2017-07-26")
   >>> c
   <SkyCoord (Helioprojective: obstime=2017-07-26T00:00:00.000, rsun=695508.0 km, observer=<HeliographicStonyhurst Coordinate for 'earth'>): (Tx, Ty) in arcsec
       (0., 0.)>
   >>> c.transform_to(frames.HeliographicCarrington)
   <SkyCoord (HeliographicCarrington: obstime=2017-07-26T00:00:00.000): (lon, lat, radius) in (deg, deg, km)
      (283.99298362, 5.31701821, 695508.00000058)>

It is also possible to transform to any coordinate system implemented in Astropy.
This can be used to find the position of the solar limb in AltAz equatorial coordinates::

    >>> from astropy.coordinates import EarthLocation, AltAz
    >>> time = '2017-07-11 15:00'
    >>> greenbelt = EarthLocation(lat=39.0044*u.deg, lon=-76.8758*u.deg)
    >>> greenbelt_frame = AltAz(obstime=time, location=greenbelt)
    >>> west_limb = SkyCoord(900*u.arcsec, 0*u.arcsec, frame=frames.Helioprojective, obstime=time)
    >>> west_limb.transform_to(greenbelt_frame)  # doctest: +SKIP
    <SkyCoord (AltAz: obstime=2017-07-11 15:00:00.000, location=(1126916.53031967, -4833386.58391627, 3992696.622115747) m, pressure=0.0 hPa, temperature=0.0 deg_C, relative_humidity=0, obswl=1.0 micron): (az, alt, distance) in (deg, deg, m)
        (111.40839101, 57.16645715, 1.51860261e+11)>

Observer Location Information
=============================

Both `~sunpy.coordinates.frames.Helioprojective` and `~sunpy.coordinates.frames.Heliocentric` frames are defined by the location of the observer.
For example in `~sunpy.coordinates.frames.Helioprojective` the observer is at the origin of the coordinate system.
This information is encoded in the `~sunpy.coordinates.frames.Helioprojective` and `~sunpy.coordinates.frames.Heliocentric` frames as the ``observer`` attribute, which is itself an instance of the `~sunpy.coordinates.frames.HeliographicStonyhurst` frame.
The default observer location is set to the position of the Earth (using  ~sunpy.coordinates.ephemeris.get_body_heliographic_stonyhurst`) as long as the ``obstime`` attribute is specified.
If the ``obstime`` attribute is not set then you will be unable to transform the frame unless an explicit ``observer`` is specified, as the time is required to calculate the location of the Earth.
The location of the observer is automatically populated from metadata when coordinate frames are created using `~sunpy.map.Map`.

It is possible to convert from a `~sunpy.coordinates.frames.Helioprojective` frame with one observer location to another `~sunpy.coordinates.frames.Helioprojective` frame with a different observer location.
You nedd to convert through `~sunpy.coordinates.frames.Heliographic` but this does involve making an assumption of the radius of the Sun to calculate the position on the solar sphere.
The conversion can be performed as follows::

  >>> import sunpy.coordinates

  >>> hpc1 = SkyCoord(0*u.arcsec, 0*u.arcsec, observer="earth", obstime="2017-07-26", frame=frames.Helioprojective)
  # Define a new Helioprojective frame with a different observer.
  >>> hpc_out = sunpy.coordinates.Helioprojective(observer="venus", obstime="2017-07-26")
  # Perform the transformation from one to the other.
  >>> hpc2 = hpc1.transform_to(hpc_out)

An example with two maps, named ``aia`` and ``stereo``::

  >>> hpc1 = SkyCoord(0*u.arcsec, 0*u.arcsec, frame=aia.coordinate_frame)  # doctest: +SKIP
  >>> hpc2 = hpc1.transform_to(stereo.coordinate_frame)  # doctest: +SKIP

Design of the Coordinates Module
================================

This module works by defining a collection of ``Frames`` (`sunpy.coordinates.frames`), which exists on a transformation graph, where the transformations between the coordinate frames are then defined and registered with the transformation graph (`sunpy.coordinates.transformations`).
It is also possible to transform SunPy frames to Astropy frames.

Positions within these ``Frames`` are stored as a ``Representation`` of a coordinate, a representation being a description of a point in a Cartesian, spherical or cylindrical system.
A frame that contains a representation of one or many points is said to have been 'realized'.

For a more in depth look at the design and concepts of the Astropy coordinates system see, :ref:`astropy-coordinates-overview`.

Frames and SkyCoord
-------------------

The `~astropy.coordinates.SkyCoord` class is a high level wrapper around the `astropy.coordinates` package.
It provides an easier way to create and transform coordinates, by using string representations for frames rather than the classes themselves and some other usability improvements.
For more information see the `~astropy.coordinates.SkyCoord` documentation.

The main advantage provided by `~astropy.coordinates.SkyCoord` is the support it provides for caching Frame attributes.
Frame attributes are extra data specified with a frame, some examples in `sunpy.coordinates` are ``obstime`` or ``observer`` for observer location.
Only the frames where this data is meaningful have these attributes, i.e. only the Helioprojective frames have ``observer``.
However, when you transform into another frame and then back to a projective frame using `~astropy.coordinates.SkyCoord` it will remember the attributes previously provided, and repopulate the final frame with them.
If you were to do transformations using the Frames alone this would not happen.

The most important implication for this in `sunpy.coordinates` is the ``rsun`` parameter in the projective frames.
If you create a projective frame with a ``rsun`` attribute, if you convert back to a projective frame it will be set correctly.
It should also be noted that, if you create a Heliographic frame and then transform to a projective frame with an ``rsun`` attribute, it will not match the ``radius`` coordinate in the Heliographic frame.
This is because you may mean to be describing a point above the defined 'surface' of the Sun.

Coordinates and WCS
===================

The `sunpy.coordinates` package provides a mapping between ``FITS-WCS CTYPE`` convention and the coordinate frames as defined in `sunpy.coordinates`.
This is used via the `astropy.wcs.utils.wcs_to_celestial_frame` function, which the SunPy frames are registered upon when they are imported.
This list is used to convert from `~astropy.wcs.WCS` objects to coordinate frames.

The `~sunpy.map.GenericMap` class creates `~astropy.wcs.WCS` objects as ``amap.wcs``, however, it adds some extra attributes to the `~astropy.wcs.WCS` object to be able to fully specify the coordinate frame.
It adds ``heliographic_observer`` and ``rsun``.

If you want to obtain a un-realized coordinate frame corresponding to a `~sunpy.map.GenericMap` object you can do the following::

  >>> import sunpy.map
  >>> from sunpy.data.sample import AIA_171_IMAGE  # doctest: +REMOTE_DATA
  >>> amap = sunpy.map.Map(AIA_171_IMAGE)  # doctest: +REMOTE_DATA
  >>> amap.observer_coordinate  # doctest: +REMOTE_DATA
    <SkyCoord (HeliographicStonyhurst: obstime=2011-06-07T06:33:02.770): (lon, lat, radius) in (deg, deg, m)
        (0., 0.048591, 1.51846026e+11)>

which is equivalent to::

  >>> from astropy.wcs.utils import wcs_to_celestial_frame # doctest: +REMOTE_DATA
  >>> wcs_to_celestial_frame(amap.wcs)  # doctest: +REMOTE_DATA
    <Helioprojective Frame (obstime=2011-06-07T06:33:02.770, rsun=696000000.0 m, observer=<HeliographicStonyhurst Coordinate (obstime=2011-06-07T06:33:02.770): (lon, lat, radius) in (deg, deg, m)
        (0., 0.048591, 1.51846026e+11)>)>

Attribution
===========

Some of this documentation was adapted from Astropy under the terms of the `BSD License <https://raw.githubusercontent.com/astropy/astropy/master/LICENSE.rst>`_.

This package was initially developed by Stuart Mumford and Pritish Chakraborty as part of GSoC 2014.
