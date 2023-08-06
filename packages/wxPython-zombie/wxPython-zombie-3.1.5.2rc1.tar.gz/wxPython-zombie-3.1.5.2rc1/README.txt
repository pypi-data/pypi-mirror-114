**wxPython-zombie** eventually matured to version 3.1.5 of wxWidgets. No more
development, only bug fixes are done. **wxPython-zombie** will provide the 64-bit
binary extension package (build with Visual Studio 2019) for MS Windows 10/11 and
the source package to build for Linux. This is a pre-release for Python 3.10.

You must not install **wxPython** and **wxPython-zombie** in the same environment,
both packages use the package directory ``wx``.

The build and installation on Linux was tested on Arch Linux, with just the
minimal explicit installed packages or groups linux, base, base-devel, python,
python-pip, webkit2gtk, glu and sdl2. Use the verbose and user option in pip.

The demo package of **wxPython-zombie** is included in the distribution.


Installation on MS Windows 10/11
--------------------------------
Using pip::

    > pip install wxpython-zombie


Build and installation on Arch Linux
------------------------------------
Using pip::

    > pip install -v --user wxpython-zombie


Start the demo
--------------
From the console::

    > wxpython-demo

