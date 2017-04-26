Installation using pip
======================

System-wide
-----------

::

    sudo pip install --trusted-host phdru.name --find-links=http://phdru.name/Software/Python/ --install-option='-O2' m_librarian

User mode
---------

::

    pip install --trusted-host phdru.name --find-links=http://phdru.name/Software/Python/ --install-option='-O2' --user m_librarian

Virtual envs
------------

::

    pip install --trusted-host phdru.name --find-links=http://phdru.name/Software/Python/ --install-option='-O2' m_librarian

For Python 2.6 the command is easy_install.

Installation from sources
=========================

To install the library from sources system-wide run run the following
command:

::

    sudo python setup.py install -O2

If you don't want to install it system-wide you can install it in your
home directory; run run the following command:

::

    python setup.py install -O2 --user

Option '--user' installs m_librarian into
$HOME/.local/lib/python$MAJOR.$MINOR/site-packages/ where python finds it
automatically. It also installs m_librarian scripts into $HOME/.local/bin;
add the directory to your $PATH or move the scripts to a directory in your
$PATH.
