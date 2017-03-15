raspyrfm-client
==============

A python library for accessing actuator and sensor data on the the EZcontrol® XS1 Gateway using their HTTP API.

How to use
==========

Installation
------------

:code:`pip install raspyrfm-client`

Usage
-----

For a basic example have a look at the `example.py <https://github.com/markusressel/raspyrfm-client/blob/master/example_simple.py>`_ file.

If you need more info have a look at the `documentation <http://raspyrfm-client.readthedocs.io/>`_ which should help.

Basic Example
-------------
Import required modules
^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   from raspyrfm_client import RaspyRFMClient
   from raspyrfm_client.device import actions
   from raspyrfm_client.device.manufacturer import manufacturer_constants


Create the :code:`RaspyRFMClient` object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you know the :code:`IP` and :code:`Port` of your :code:`RaspyRFM` you can pass them as arguments:

.. code-block:: python

   rfm_client = RaspyRFMClient("192.168.2.10", 9876)

or

.. code-block:: python

   rfm_client = RaspyRFMClient("192.168.2.10") # defaults to port 49880

Otherwise you can just create it without:

.. code-block:: python

   rfm_client = RaspyRFMClient()

and then let the client search for the :code:`RaspyRFM` automatically with:

.. code-block:: python

   ip = rfm_client.search()

This will return an :code:`IP Address` if a :code:`RaspyRFM` module was found.

**WARNING:** currently the search() method only works on linux systems :(

Get a Device
^^^^^^^^^^^^

To get a quick overview of what **manufacturers** and **models** are supported call:

.. code-block:: python

   rfm_client.list_supported_devices()

which will give you an indented list of supported manufacturers and their supported models similar to this:

.. code-block:: text

   Elro
     RC3500-A IP44 DE
     AB440S
     AB440D 200W
     AB440D 300W
     AB440ID
     AB440IS
     AB440L
     AB440SC
     AB440WD
   BAT
     RC AAA1000-A IP44 Outdoor
   Brennenstuhl
     RCS 1000 N Comfort
     RCS 1044 N Comfort
   Intertek
     Model 1919361
   [...]

**Use the names in this list (or better yet: :code:`manufacturer_constants.py` constants) to get a device in the next step.**

To generate codes for a device **you first have to get an instance of its implementation**. Use the following method to get just that:

.. code-block:: python

   brennenstuhl_rcs1000 = rfm_client.get_device(manufacturer_constants.BRENNENSTUHL,
                                             manufacturer_constants.RCS_1000_N_COMFORT)

It is always a good choice to **only use values present in :code:`manufacturer_constants`** but if needed this can also be a :code:`string`. These should always be the same values as the ones printed by the :code:`list_supported_devices()` method.

Generate action codes
^^^^^^^^^^^^^^^^^^^^^
Now that you have an implementation instance you can generate codes for supported actions by using an :code:`actions` constant that you imported previously.

To get a list of supported actions call:

.. code-block:: python

   brennenstuhl_rcs1000.get_supported_actions()

and generate a code with:

.. code-block:: python

   code = brennenstuhl_rcs1000.generate_code(actions.ON)

Send the code to the :code:`RaspyRFM` module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To send a code for your device of choice you can combine the two objects in this call:

.. code-block:: python

   rfm_client.send(brennenstuhl_rcs1000, actions.ON)

Custom implementations
======================



License
=======

::

    raspyrfm- by Markus Ressel
    Copyright (C) 2017  Markus Ressel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
