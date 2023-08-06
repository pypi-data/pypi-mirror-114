========
pop-loop
========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/


`pop-loop` Contains plugins that allow alternate io loops to be used to run asynchronous code in pop projects.

About
=====

Pop used the asyncio loop by default in a built-in mod at 'hub.pop.loop'.
It became necessary to split the mod into it's own project for more loop capabilities.
For testing, loop management was difficult, but paired with pytest-pop, pop-loop makes async testing easy.


What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.6+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``pop-loop``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

    If package is available via PyPI, include the directions.

    .. code-block:: bash

        pip install pop-loop


Install Extras
++++++++++++++

    ``pop-loop`` can be installed with extras to enable the different loop plugins in this project.

    trio:
    .. code-block:: bash

        pip install pop-loop\[trio\]


    uvloop:
    .. code-block:: bash

        pip install pop-loop\[uvloop\]

    qt:
    .. code-block:: bash

        pip install pop-loop\[qt\]


Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@gitlab.com/saltstack/pop/pop-loop.git
   cd pop-loop

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
=====

Describe some basic example use case for this plugin.

Examples
--------

uvloop example:
.. code-block:: python

    import asyncio
    import pop.hub

    hub = pop.hub.Hub()

    hub.pop.loop.create(loop_plugin="uv")
    task = hub.pop.Loop.create(asyncio.sleep(0))
    hub.pop.Loop.run_until_complete(task)


trio example:
.. code-block:: python

    import asyncio
    import pop.hub

    hub = pop.hub.Hub()

    hub.pop.loop.create(loop_plugin="trio")
    task = hub.pop.Loop.create(asyncio.sleep(0))
    hub.pop.Loop.run_until_complete(task)


QT example:
.. code-block:: python

    import asyncio
    import pop.hub
    import PyQt5.QtWidgets as pyqt5


    hub = pop.hub.Hub()
    hub.loop.qt.APP = pyqt5.QApplication([])
    hub.pop.loop.create(loop_plugin="qt")

    task = hub.pop.Loop.create(asyncio.sleep(0))
    hub.pop.Loop.run_until_complete(task)


Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
