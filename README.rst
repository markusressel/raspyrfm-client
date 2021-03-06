.. |pypi_version| image:: https://badge.fury.io/py/raspyrfm-client.svg
    :target: https://badge.fury.io/py/raspyrfm-client

raspyrfm-client |pypi_version|
==============================

A python 3.4+ library that allows the generation of network codes for the RaspyRFM rc module (and other gateways too!).

Build Status
============

.. |build_master| image:: https://travis-ci.org/markusressel/raspyrfm-client.svg?branch=master
    :target: https://travis-ci.org/markusressel/raspyrfm-client/branches

.. |build_beta| image:: https://travis-ci.org/markusressel/raspyrfm-client.svg?branch=beta
    :target: https://travis-ci.org/markusressel/raspyrfm-client/branches

.. |build_dev| image:: https://travis-ci.org/markusressel/raspyrfm-client.svg?branch=dev
    :target: https://travis-ci.org/markusressel/raspyrfm-client/branches


.. |codebeat_master| image:: https://codebeat.co/badges/fcac9cfe-b6a2-4c4a-938d-42214371dc3d
    :target: https://codebeat.co/projects/github-com-markusressel-raspyrfm-client-master

.. |codebeat_beta| image:: https://codebeat.co/badges/c6c09759-3f34-4a16-b17e-d7989b3f7fae
    :target: https://codebeat.co/projects/github-com-markusressel-xs1-api-client-beta

.. |codebeat_dev| image:: https://codebeat.co/badges/6ef4cbdd-a452-45b2-8ee8-f7a09e53689f
    :target: https://codebeat.co/projects/github-com-markusressel-raspyrfm-client-dev

+--------------------+------------------+-----------------+
| Master             | Beta             | Dev             |
+====================+==================+=================+
| |build_master|     | |build_beta|     | |build_dev|     |
+--------------------+------------------+-----------------+
| |codebeat_master|  | |codebeat_beta|  | |codebeat_dev|  |
+--------------------+------------------+-----------------+

Home Assistant
==============
The initial goal of this library was to be able to integrate the SimpleSolutions ConnAir gateway with `Home Assistant <https://www.home-assistant.io>`_. This gateway is sadly not sold anymore but there are other alternatives like the Intertechno Gateway or the `ConnAir Emulator script <https://github.com/Phunkafizer/RaspyRFM/blob/master/connair.py>`_ that can be used on a Raspberry Pi equipped with a 433MHz radio like the `RaspyRFM from Seegel Systeme <https://www.seegel-systeme.de/produkt/raspyrfm-ii/>`_.

You can find the related integration documentation here: 
`RaspyRFM Home Assistant component documentation <https://www.home-assistant.io/components/switch.raspyrfm/>`_

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
   from raspyrfm_client.device_implementations.controlunit.actions import Action
   from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
   from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
   from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer


Create the :code:`RaspyRFMClient` object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Get a client instance by calling:


.. code-block:: python

   rfm_client = RaspyRFMClient()

Create a :code:`Gateway` instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can let the library search automatically for gateways available in LAN using:

.. code-block:: python

   gateways = rfm_client.search()

This will return a list of Gateways that can later be used to send signals to.

To get a quick overview of what gateway **manufacturers** and **models** are supported call:

.. code-block:: python

   rfm_client.list_supported_gateways()

Create a gateway instance with the specified :code:`IP` and :code:`Port` of your Gateway by using:

.. code-block:: python

   gateway = rfm_client.get_gateway(Manufacturer.SEEGEL_SYSTEME, GatewayModel.RASPYRFM, "192.168.2.10", 9876)

or

.. code-block:: python

   gateway = rfm_client.get_gateway(Manufacturer.SEEGEL_SYSTEME, GatewayModel.RASPYRFM, "192.168.2.10") # defaults to 49880 or the gateway implementations default

Get a :code:`ControlUnit`
^^^^^^^^^^^^^^^^^^^^^^^^^
ControlUnits are the devices that receive the RC signals sent using the gateway, f.ex. a power outlet.

To get a quick overview of what ControlUnits **manufacturers** and **models** are supported call:

.. code-block:: python

   rfm_client.list_supported_controlunits()

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

To generate codes for a device **you first have to get an instance of its implementation** like this:

.. code-block:: python

   brennenstuhl_rcs1000 = rfm_client.get_controlunit(manufacturer_constants.BRENNENSTUHL,
                                             manufacturer_constants.RCS_1000_N_COMFORT)

The parameters of the :code:`get_controlunit()` method always need to be an enum value of the specified type.
You can get an enum constant by its name though using:

.. code-block:: python

   manufacturer = Manufacturer("Intertechno")
   model = ControlUnitModel("IT-1500")

:code:`ControlUnit` channel configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Before you can generate codes with your shiny new gateway and :code:`ControlUnit` implementations you have to specify a channel configuration for your :code:`ControlUnit`. These **configurations can be very different for every device**. The best way to know the correct way of specifying the channel configuration for a specific device is to look at the source code (yes I know...) or by trial and error (even worse). A good :code:`ControlUnit` implementation should tell you how the configuration should look like when specifying it in a wrong way.

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
The second one is the recommended one as it will often result in a much more readable source code.

For our Brennenstuhl device it would look like this:

.. code-block:: python

    brennenstuhl_rcs1000.set_channel_config(**{
        '1': True,
        '2': True,
        '3': True,
        '4': True,
        '5': True,
        'CH': 'A'
    })

Generate action codes
^^^^^^^^^^^^^^^^^^^^^
Now that you have a properly set up :code:`ControlUnit` you can generate codes for it's supported actions by using an :code:`Action` enum constant that you imported previously.

To get a list of supported actions for a :code:`ControlUnit` call:

.. code-block:: python

   brennenstuhl_rcs1000.get_supported_actions()

and generate a code for one of them using your :code:`Gateway` instance:

.. code-block:: python

   code = gateway.generate_code(brennenstuhl_rcs1000, Action.ON)

Send the code to the :code:`RaspyRFM` module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To send a code for your device of choice you can combine the objects in this call:

.. code-block:: python

   rfm_client.send(gateway, brennenstuhl_rcs1000, Action.ON)

This will generate a code specific to the passed in gateway implementation and send it to it's host address immediately after.

Custom implementations
======================

The :code:`raspyrfm-client` library is designed so you can implement custom devices in a (hopefully) very easy way.

File Structure
--------------
All :code:`ControlUnit` implementations are located in the :code:`/device_implementations/controlunit/manufacturer/` module and implement the base class :code:`Device` that can be found in :code:`/device_implementations/controlunit/base.py`.

Create a new :code:`ControlUnit`
--------------------------------
To create a new :code:`ControlUnit` implementation for a new manufacturer and model create a new subdirectory for your manufacturer and a python file for your model:

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

Implement a :code:`ControlUnit`
-------------------------------

Now the basic implementation of your :code:`ControlUnit` should looks like this:

.. code-block:: python

    from raspyrfm_client.device_implementations.controlunit.actions import Action
    from raspyrfm_client.device_implementations.controlunit.base import ControlUnit


    class YourModel(ControlUnit):
        def __init__(self):
            from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
            from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
            super().__init__(Manufacturer.YourManufacturer, ControlUnitModel.YourModel)

        def get_channel_config_args(self):
            return {}

        def get_pulse_data(self, action: Action):
            return [[0, 0], [0, 0]], 0, 0

        def get_supported_actions(self) -> [str]:
            return [Action.ON]


Most importantly you have to call the :code:`super().__init__` method like shown. This will ensure that your implementation is found by the :code:`RaspyRFMClient` and you can get an instance of your device using :code:`rfm_client.get_controlunit()` as shown before.

If your manufacturer does not exist yet **create a new enum constant** in the :code:`manufacturer_constants.py` file and use its value in your :code:`__init__`.
**Do the same thing for your model name** in the :code:`controlunit_constants.py` file.

You also have to implement all abstract methods from the :code:`Device` class. Have a look at it's documentation to get a sense of what those methods are all about.

After you have implemented all methods you are good to go!
Just call :code:`rfm_client.reload_implementation_classes()` and :code:`rfm_client.list_supported_controlunits()` to check if your implementation is listed.
If everything looks good you can use your implementation like any other one.



Exclude a WIP implementation
----------------------------
To prevent the RaspyRFM client from importing your half baked or base class implementation just include a class field like this:

.. code-block:: python

   class YourModel(ControlUnit):
      DISABLED = True

      [...]

Contributing
============

GitHub is for social coding: if you want to write code, I encourage contributions through pull requests from forks
of this repository. Create GitHub tickets for bugs and new features and comment on the ones that you are interested in.

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
