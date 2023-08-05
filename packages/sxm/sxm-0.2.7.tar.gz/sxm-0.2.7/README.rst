sxm-client
==========

.. image:: https://readthedocs.org/projects/sxm-client/badge/?version=latest
    :target: https://sxm-client.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/AngellusMortis/sxm-client/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/AngellusMortis/sxm-client/actions/workflows/ci.yml
    :alt: CI Status

.. image:: https://api.codeclimate.com/v1/badges/ea06824c1732b39d7d0b/maintainability
    :target: https://codeclimate.com/github/AngellusMortis/sxm-client/maintainability
    :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/ea06824c1732b39d7d0b/test_coverage
    :target: https://codeclimate.com/github/AngellusMortis/sxm-client/test_coverage
    :alt: Test Coverage

.. image:: https://pypip.in/v/sxm/badge.png
    :target: https://pypi.org/project/sxm/
    :alt: Latest PyPI version


.. warning:: Designed for PERSONAL USE ONLY

    ``sxm`` is a 100% unofficial project and you use it at your own risk.
    It is designed to be used for personal use with a small number of users
    listening to it at once. Similar to playing music over a speak from the
    radio directly. Using ``sxm-player`` in any corporate setting, to
    attempt to pirate music, or to try to make a profit off your subscription
    may result in you getting in legal trouble.

``sxm-client`` is a Python library designed to help write applications for the
popular XM Radio service.

* Free software: MIT license
* Documentation: http://sxm-client.readthedocs.io/.

Features
--------

* A simple HTTP Proxy server that can serve HLS streams for sxm-client channels
* Python sxm Client
* Python classes for interface with sxm channel data

For details on usage and installation, see the `documentation`_.

``sxm-client`` is designed to be a bare bones library to setup an anonymous HLS
stream. For a more in-depth applications, check out
`sxm-player`_.

.. _documentation: http://sxm-client.readthedocs.io/
.. _sxm-player: https://github.com/AngellusMortis/sxm-player


Credits
-------

Huge props to andrew0 <andrew0@github.com> for for reverse engineering the
original SXM APIs used

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
