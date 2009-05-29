Installation
============

Requirements
------------
 * Python XMP Toolkit
 * Python 2.5+
 * Exempi 2.1
 * Linux or OS X (see notes below for Windows)


Python AVM Library
----------------------
The short version of installation is::

  python setup.py install


Python XMP Toolkit
----------------------
The Python XMP Toolkit may be downloaded from
http://code.google.com/p/python-xmp-toolkit/.

The short version of installation is::

  python setup.py install

Note, in case you haven't installed Exempi you will get an :exc:`ExempiLoadError` exception once you try to load :mod:`libxmp`.

Exempi
------
Python XMP Toolkit requires Exempi 2.1 which can be downloaded from
http://libopenraw.freedesktop.org/wiki/Exempi. To install Exempi, unpack the
distribution and run::

  ./configure
  make
  sudo make install


Mac OS X 
--------
Note Exempi requires boost (http://www.boost.org/) to compile, so on OS X you probably need to run configure with one of the following options.::

  ./configure --with-darwinports
  ./configure --with-fink 

.. warning::
	Note, currently Exempi 2.1 does not compile on OS X, due to bugs 
	in a number of Makefiles. A patched version of Exempi 2.1 that compiles 
	under OS X can be download at 
	http://python-xmp-toolkit.googlecode.com/files/exempi-2.1.0-patched.tar.gz.

Windows 
-------
The library has not been tested on Windows, and nor has any serious effort been made to test it. Hence, developers wanting to use the library on Windows are encouraged to try it out and let us know if it works. 

The library ought to work on Windows, if Exempi can be compiled as a DLL using e.g. Cygwin.