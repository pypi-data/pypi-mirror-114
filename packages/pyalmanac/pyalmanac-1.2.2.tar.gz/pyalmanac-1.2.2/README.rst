=============================
Pyalmanac Project Description
=============================

This is the **PyPI edition** of `Pyalmanac-Py3 <https://github.com/aendie/Pyalmanac-Py3>`_. Version numbering starts from 1.0 as the previous well-tested Pyalmanac-Py3 versions that are on github were never published elsewhere. Version numbering follows the scheme *Major.Minor.Patch*, whereby the *Patch* number represents some kind of a small fix to the intended release, e.g. 1.2.1 removes an unnecessary file and the deprecated (but still functional) LaTeX command *\\clearscrheadfoot* is repalaced by *\\clearpairofpagestyles*.

Pyalmanac is a **Python 3** script that essentially creates the daily pages of the Nautical Almanac.
These are tables that are needed for celestial navigation with a sextant. Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

Pyalmanac was developed based on the original *Pyalmanac* by Enno Rodegerdts. Various improvements, enhancements and bugfixes have been included. Pyalmanac contains its own star database (similar to the database in ``Ephem`` 3.7.6 whose accuracy was sub-optimal).
It has been updated with data from the Hipparcos Star Catalogue and the GHA/Dec star data now matches a sample page from a Nautical Almanac typically to within 0°0.1'.

However Pyalmanac is nearing the end of its useful days. Almanacs generated after the next few years may be insufficient for navigational purposes.
**SFalmanac** (or **Skyalmanac** with some restrictions regarding the accuracy of sunset/twilight/sunrise and moonrise/moonset) are the new norm as these are based on the more accurate algorithms employed in the `NASA JPL HORIZONS System <https://ssd.jpl.nasa.gov/horizons.cgi>`_. The same algorithms are implemented in Skyfield.

Pyalmanac is implemented using Ephem (originally named PyEphem), which in turn uses XEphem that uses the VSOP87D algorithms for the planets. XEphem is also 'end of life' as no further updates are planned. 
The key discrepancies are related to the projected speed of Earth's rotation, or "siderial time".

Skyfield-based almanacs (SFalmanac and Skyalmanac), on the other hand, now use the International Earth Rotation and Reference 
Systems Service (IERS) Earth Orientation Parameters (EOP) data which are forecast for at least the coming 
12 months (and updated weekly). 
Accurate assessment of "sidereal time" will minimize GHA discrepancies in general. This applies to all celestial objects.


Software Requirements
=====================

.. |nbsp| unicode:: 0xA0 
   :trim:

| Most of the computation is done by the free Ephem library.
| Typesetting is done typically by MiKTeX or TeX Live.
| These need to be installed:

* Python v3.4 or higher (the latest version is recommended)
* Ephem >= 3.7.6
* MiKTeX |nbsp| |nbsp| or |nbsp| |nbsp| TeX Live

Installation
============

Install a TeX/LaTeX program on your operating system so that 'pdflatex' is available.

Ensure that the `pip Python installer tool <https://pip.pypa.io/en/latest/installing.html>`_ is installed.
Then ensure that old versions of PyEphem, Ephem and Pyalmanac are not installed before installing SkyAlmanac from PyPI::

  python -m pip uninstall pyephem ephem pyalmanac
  python -m pip install pyalmanac

Thereafter run it with::

  python -m pyalmanac

On a POSIX system (Linux or Mac OS), use ``python3`` instead of ``python`` above.

This PyPI edition also supports installing and running in a `venv <https://docs.python.org/3/library/venv.html>`_ virtual environment.
Finally check or change the settings in ``config.py``.
It's location is printed immediately whenever Pyalmanac runs.

Guidelines for Linux & Mac OS
-----------------------------

Quote from `Chris Johnson <https://stackoverflow.com/users/763269/chris-johnson>`_:

It's best to not use the system-provided Python directly. Leave that one alone since the OS can change it in undesired ways.

The best practice is to configure your own Python version(s) and manage them on a per-project basis using ``venv`` (for Python 3). This eliminates all dependency on the system-provided Python version, and also isolates each project from other projects on the machine.

Each project can have a different Python point version if needed, and gets its own site_packages directory so pip-installed libraries can also have different versions by project. This approach is a major problem-avoider.

Troubleshooting
---------------

If using MiKTeX 21 or higher, executing 'option 5' (Increments and Corrections) it will probably fail with::

    ! TeX capacity exceeded, sorry [main memory size=3000000].

To resolve this problem (assuming MiKTeX has been installed for all users),
open a Command Prompt as Administrator and enter: ::

    initexmf --admin --edit-config-file=pdflatex

This opens pdflatex.ini in Notepad. Add the following line: ::

    extra_mem_top = 1000000

and save the file. Problem solved. For more details look `here <https://tex.stackexchange.com/questions/438902/how-to-increase-memory-size-for-xelatex-in-miktex/438911#438911>`_.