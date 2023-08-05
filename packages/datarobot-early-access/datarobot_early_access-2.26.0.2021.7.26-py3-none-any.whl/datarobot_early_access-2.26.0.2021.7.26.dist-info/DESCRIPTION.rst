About datarobot_early_access
===============================
.. image:: https://img.shields.io/pypi/v/datarobot.svg
   :target: https://pypi.python.org/pypi/datarobot/
.. image:: https://img.shields.io/pypi/pyversions/datarobot.svg
.. image:: https://img.shields.io/pypi/status/datarobot.svg

DataRobot is a client library for working with the `DataRobot`_ platform API. This package is the
"early access" version of the client. For the most stable version, see the quarterly release on PyPI
at https://pypi.org/project/datarobot/.

Installation
=========================
Python 2.7 and >= 3.4 are supported.
You must have a datarobot account.

::

   $ pip install datarobot_early_access

Usage
=========================
The library will look for a config file `~/.config/datarobot/drconfig.yaml` by default.
This is an example of what that config file should look like.

::

   token: your_token
   endpoint: https://app.datarobot.com/api/v2

Alternatively a global client can be set in the code.

::

   import datarobot as dr
   dr.Client(token='your_token', endpoint='https://app.datarobot.com/api/v2')

Alternatively environment variables can be used.

::

   export DATAROBOT_API_TOKEN='your_token'
   export DATAROBOT_ENDPOINT='https://app.datarobot.com/api/v2'

See `documentation`_ for example usage after configuring.

Tests
=========================
::

   $ py.test

.. _datarobot: http://datarobot.com
.. _documentation: https://datarobot-public-api-client.readthedocs-hosted.com


