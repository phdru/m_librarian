Installation using pip
======================

System-wide
-----------

::

    sudo pip install m_librarian

User mode
---------

::

    pip install --user m_librarian

Virtual envs
------------

::

    pip install m_librarian

Progress bar
============

To allow ``ml-import.py`` to display progress bar the program requires
library ``m_lib``. You can install the library separately using, e.g.,
command ``pip install m_lib``. Or you can install the library with
``m_librarian``: ``pip install m_librarian[pbar]``.

Other extras
============

``pip install m_librarian[web]`` installs libraries needed for web-ui.

``pip install m_librarian[wx]`` installs a library needed for wx GUI
(``wxPython``). Should work for non-Linux platforms, but for Linux
``wxPython`` should be installed separately either using system package
manager, or from https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ ,
or using ``conda``::

    conda create -n wx27 python=2.7 wxpython
    conda activate wx27

Python 2.7 is used here just an example, the librarin works with any
Python version, 2.7 and 3.4+.

Installation from sources
=========================

To install the library from sources system-wide run run the following
command:

::

    sudo python setup.py install

If you don't want to install it system-wide you can install it in your
home directory; run run the following command:

::

    python setup.py install --user

Option '--user' installs m_librarian into
$HOME/.local/lib/python$MAJOR.$MINOR/site-packages/ where python finds it
automatically. It also installs m_librarian scripts into $HOME/.local/bin;
add the directory to your $PATH or move the scripts to a directory in your
$PATH.
