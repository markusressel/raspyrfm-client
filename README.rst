raspyrfm-client
===============

A python library that allows the generation of network codes for the RaspyRFM rc module.

Build Status
============
[![Build Status](https://travis-ci.org/markusressel/raspyrfm-client.svg?branch=master)](https://travis-ci.org/markusressel/raspyrfm-client)

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

**Use the names in this list (or better yet** :code:`manufacturer_constants.py`
**constants) to get a device in the next step.**

To generate codes for a device **you first have to get an instance of its implementation** like this:

.. code-block:: python

   brennenstuhl_rcs1000 = rfm_client.get_device(manufacturer_constants.BRENNENSTUHL,
                                             manufacturer_constants.RCS_1000_N_COMFORT)

It is always a good idea to **only use values present in** :code:`manufacturer_constants` but if needed you can also pass in a :code:`string`. These however need to always be the same values as the ones printed by the :code:`list_supported_devices()` method.

Channel configuration
^^^^^^^^^^^^^^^^^^^^^
Before you can generate codes with your shiny new device implementation you have to specify a channel configuration. These **configurations can be very different for every device**. The best way to know the correct way of specifying the channel configuration for a specific device is to look at the source code (yes I know...) or by trial and error (even worse). A good device implementation should tell you how the device configuration should look like when specifying it wrong.

However all configurations are a **keyed dictionary**.
So in general there are two ways of passing the channel configuration argument.
One (inline):

.. code-block:: python

    device.set_channel_config(value1=1, value2=2)

Two (as a dictionary):

.. code-block:: python

    device.set_channel_config(**{
        'value1': 1,
        'value2': 2
    })

**Note** that the **keys always need to be a** :code:`string`.

For our brennenstuhl device it would look like this:

.. code-block:: python

    brennenstuhl_rcs1000.set_channel_config(**{
        '1': True,
        '2': True,
        '3': True,
        '4': True,
        '5': True,
        'A': True,
        'B': False,
        'C': False,
        'D': False,
        'E': False
    })

Generate action codes
^^^^^^^^^^^^^^^^^^^^^
Now that you have an implementation instance you can generate codes for supported actions by using an :code:`actions` constant that you imported previously.

To get a list of supported actions for a device call:

.. code-block:: python

   brennenstuhl_rcs1000.get_supported_actions()

and generate a code for one of them with:

.. code-block:: python

   code = brennenstuhl_rcs1000.generate_code(actions.ON)

Send the code to the :code:`RaspyRFM` module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To send a code for your device of choice you can combine the two objects in this call:

.. code-block:: python

   rfm_client.send(brennenstuhl_rcs1000, actions.ON)

Note that this will only work if you specified an :code:`IP` manually or the :code:`search()` method has found your :code:`RaspyRFM` module.

Custom implementations
======================

The :code:`raspyrfm-client` library is designed so you can implement custom devices in a (hopefully) very easy way.

File Structure
--------------
All device implementations are located in the :code:`/device/manufacturers/` module and implement the base class :code:`Device` that can be found in :code:`/device/base.py`.

Create a new Device
-------------------
To create a new device implementation for a new manufacturer and model create a new subdirectory for your manufacturer and a python file for your model:

.. code-block::

    ───raspyrfm_client
    │   │   client.py
    │   │
    │   └───device
    │       │   actions.py
    │       │   base.py
    │       │
    │       └───manufacturer
    │           │   manufacturer_constants.py
    │           │
    │           ├───intertek
    │           │       Model1919361.py
    │           │
    │           ├───rev
    │           │       Ritter.py
    │           │       Telecontrol.py
    │           │
    │           ├───universal
    │           │       HX2262Compatible.py
    │           │
    │           └───yourmanufacturer
    │                   yourmodel.py
    ──────────────────────────────────────────

Implement a Device
------------------

Now the basic implementation of your device looks like this:

.. code-block:: python

    from raspyrfm_client.device import actions
    from raspyrfm_client.device.base import Device


    class YourModel(Device):

        def __init__(self):
            from raspyrfm_client.device.manufacturer import manufacturer_constants
            super(YourModel, self).__init__(manufacturer_constants.YOUR_MANUFACTURER, manufacturer_constants.YOUR_MODEL)


        def set_channel_config(self, **channel_arguments) -> None:
            pass

        def get_supported_actions(self) -> [str]:
            return [actions.ON]

        def generate_code(self, action: str) -> str:
            pass

Most importantly you have to call the :code:`super().__init__` method like shown. This will ensure that your implementation is found by the :code:`RaspyRFMClient` and you can get an instance of your device using :code:`rfm_client.get_device()` as shown before.

If your manufacturer does not exist yet **create a new constant** in the :code:`manufacturer_constants.py` file and use its value in your :code:`__init__`.
**Do the same thing for your model name.**

You also have to implement all abstract methods from the :code:`Device` class. Have a look at its documentation to get a sense of what those methods are all about.

After you have implemented all methods you are good to go!
Just call :code:`rfm_client.reload_device_implementations()` and :code:`rfm_client.list_supported_devices()` to check if your implementation is listed.
If everything looks good you can use your implementation like any other one.


License
=======

::

    raspyrfm-client by Markus Ressel
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
