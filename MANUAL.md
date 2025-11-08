# RaspyRFM Client Manual

This manual walks you through everything you need to work with the
`raspyrfm-client` repository: checking out the project, preparing a
Python environment, running tests, generating documentation, using the
library in your own scripts, and extending it with support for new
hardware.

---

## 1. Repository Overview

The repository is structured around a Python package that provides
high-level helpers for driving 433/868 MHz radio gateways (for example
the Seegel Systeme RaspyRFM II) and for generating the corresponding RC
codes for receivers such as smart plugs.

```
.
├── custom_components/              # Home Assistant integration (optional)
├── docs/                           # Sphinx documentation project
├── example.py                      # Interactive end-to-end demonstration
├── example_search.py               # Discovers gateways on the LAN
├── example_simple.py               # Minimal gateway/device usage sample
├── raspyrfm_client/                # Main Python package
│   ├── client.py                   # High level RaspyRFMClient façade
│   └── device_implementations/     # Gateway and control-unit specifics
├── tests/                          # pytest-based automated test-suite
├── MANUAL.md                       # This manual
└── README.rst                      # Project summary for PyPI/GitHub
```

> **Tip:** The `custom_components` directory only matters if you install
the bundled Home Assistant integration. You can use the library on its
own without Home Assistant.

---

## 2. Prerequisites

1. **Python** – Version 3.8 or newer is recommended. The package
   supports Python 3.4+, but modern tooling is easier with newer
   interpreters.
2. **Git** – Required for cloning the repository and managing changes.
3. **Virtual environment tooling** – Use `venv`, `virtualenv`, `poetry`,
   or your preferred tool to keep dependencies isolated.
4. **Hardware (optional)** – For live testing you need a compatible
   gateway (RaspyRFM, ConnAir, Intertechno, …) on the same network and at
   least one supported receiver (control unit).

---

## 3. Cloning the Repository

```bash
# Clone your fork or the upstream repository
$ git clone https://github.com/<your-account>/raspyrfm-client.git
$ cd raspyrfm-client

# Optionally point a remote at the upstream repository for easy syncing
$ git remote add upstream https://github.com/markusressel/raspyrfm-client.git
```

Synchronise with upstream when needed:

```bash
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

---

## 4. Creating and Activating a Virtual Environment

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

Deactivate at any time with `deactivate`.

---

## 5. Installing Dependencies

Install runtime dependencies from `requirements.txt` and optional test
requirements from `test_requirements.txt`.

```bash
# Core dependencies used by the library itself
(.venv) $ pip install --upgrade pip
(.venv) $ pip install -r requirements.txt

# Install extra tooling needed by the test-suite
(.venv) $ pip install -r test_requirements.txt
```

When packaging or installing from PyPI you can simply run:

```bash
(.venv) $ pip install .
```

---

## 6. Running the Test Suite

Automated tests are built with `pytest`.

```bash
(.venv) $ pytest
```

`pytest -k <pattern>` lets you run a subset of tests. Add `-vv` for more
verbose output.

---

## 7. Building the Documentation

The `docs/` directory contains a Sphinx project. Generate HTML docs with:

```bash
(.venv) $ cd docs
(.venv) $ make html  # On Windows use: .\make.bat html
```

Open `_build/html/index.html` in a browser to view the generated manual.
Use `make clean` to remove previous builds if you need a fresh build.

---

## 8. Exploring the Examples

Three convenience scripts in the project root illustrate typical
workflows. Run them with your virtual environment activated.

1. **`example_simple.py`** – Minimal end-to-end usage: discover a
   gateway, configure a device, and send a single command.

   ```bash
   (.venv) $ python example_simple.py
   ```

2. **`example.py`** – Extended example that interactively asks for
gateway and device information, prints supported actions, and sends a
command.

   ```bash
   (.venv) $ python example.py
   ```

3. **`example_search.py`** – Demonstrates gateway discovery and prints
all gateways found on the local network.

   ```bash
   (.venv) $ python example_search.py
   ```

Each script uses the public API exposed by `RaspyRFMClient`, so they are
good templates for your own applications.

---

## 9. Using `RaspyRFMClient` in Your Own Scripts

Follow these steps to generate and send codes to your devices.

1. **Import the library and enumerations**

   ```python
   from raspyrfm_client import RaspyRFMClient
   from raspyrfm_client.device_implementations.controlunit.actions import Action
   from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
   from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
   from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
   ```

2. **Create a client instance**

   ```python
   client = RaspyRFMClient()
   ```

   Instantiation dynamically loads every gateway and control-unit
   implementation shipped with the library so you have instant access to
   the latest protocol definitions.

3. **Discover gateways (optional)**

   ```python
   gateways = client.search()
   for gateway in gateways:
       print(gateway)
   ```

   The library broadcasts `SEARCH HCGW` on UDP port 49880 and filters
   replies using the regex supplied by each gateway implementation. Each
   result contains the host/port information required to send commands.

4. **Inspect supported hardware**

   ```python
   client.list_supported_gateways()
   client.list_supported_controlunits()
   ```

   These helper methods print manufacturer/model combinations bundled
   with the library.

5. **Create gateway and control-unit objects**

   ```python
   gateway = client.get_gateway(
       Manufacturer.SEEGEL_SYSTEME,
       GatewayModel.RASPYRFM,
       host="192.168.0.23",  # replace with your gateway
       port=49880             # optional: falls back to the implementation default
   )

   device = client.get_controlunit(
       Manufacturer.BRENNENSTUHL,
       ControlUnitModel.RCS_1000_N_COMFORT
   )
   ```

6. **Configure the receiver channel**

   Most control units require a channel configuration (for example, a
   DIP-switch ID and channel). Consult the documentation for each device
   to determine valid keys and ranges, then pass them via
   `set_channel_config()`.

   ```python
   device.set_channel_config(id="A", channel=1)
   ```

7. **Send an action**

   ```python
   client.send(gateway, device, Action.ON)
   ```

   Actions are enumerated in `controlunit.actions.Action`. Toggle a
   switch off with `Action.OFF`. Some devices provide extra actions—check
   `get_supported_actions()` on the control-unit instance.

---

## 10. Advanced Usage

### 10.1 Handling Multiple Devices

Create one device instance per physical receiver. Store them in a
collection alongside the channel configuration so you can address each
receiver explicitly.

```python
devices = {
    "living_room_lamp": client.get_controlunit(Manufacturer.INTERTECHNO, ControlUnitModel.IT_1500),
    "garden_lights": client.get_controlunit(Manufacturer.ELRO, ControlUnitModel.AB440S),
}

devices["living_room_lamp"].set_channel_config(id="B", channel=3)
```

### 10.2 Retrying or Sequencing Commands

UDP datagrams are fire-and-forget. If you want reliability, repeat
`client.send()` calls with small delays, or implement acknowledgement
logic within your own application.

```python
import time

for _ in range(3):
    client.send(gateway, devices["garden_lights"], Action.ON)
    time.sleep(0.3)
```

### 10.3 Capturing and Replaying Codes

The library focuses on code generation, but you can use the RaspyRFM
gateway to capture raw signals, then feed their parameters into custom
control-unit implementations. Use the learning features provided by the
Home Assistant integration in `custom_components/raspyrfm` if you need a
UI-driven workflow.

---

## 11. Extending the Library

You can add support for new gateways or receivers without touching the
core `RaspyRFMClient` implementation.

### 11.1 Adding a Control Unit

1. **Create a module** under
   `raspyrfm_client/device_implementations/controlunit/manufacturer/`.
2. **Subclass `ControlUnit`** and define the manufacturer/model
   constants you need.
3. **Implement required methods**:
   - `get_supported_actions()` should return a list of `Action` enum
     values.
   - `get_channel_config_args()` must describe the accepted
     configuration keys and validation regexes.
   - `get_pulse_data()` must return the pulse pairs, repetitions, and
     timebase required to build the RF payload.
4. **Register manufacturer constants** in
   `controlunit/controlunit_constants.py` if your device uses new enum
   entries.
5. **Write tests** that validate your new implementation’s behaviour.
   Use the existing tests under `tests/` as templates.

Because the client dynamically imports subclasses, no additional wiring
is necessary—your device will be available after the next
`RaspyRFMClient()` instantiation.

### 11.2 Adding a Gateway

1. **Create a subclass of `Gateway`** under
   `raspyrfm_client/device_implementations/gateway/manufacturer/`.
2. **Implement required methods**, notably:
   - `get_manufacturer()` and `get_model()` returning enum values.
   - `get_search_response_regex_literal()` describing how discovery
     responses look.
   - `create_from_broadcast()` to instantiate a configured gateway from
     discovery data.
   - `generate_code()` to transform a device/action pair into the text
     payload understood by the gateway hardware.
3. **Update enums** in
   `gateway/manufacturer/gateway_constants.py` if you introduce new
   models.
4. **Add tests** that cover payload generation and parsing logic.

---

## 12. Packaging and Publishing

1. Update the version number at the top of `setup.py` if you are making a
   release.
2. Ensure `README.rst` renders correctly (this is published to PyPI).
3. Build distributions:

   ```bash
   (.venv) $ python -m build
   ```

4. Upload to PyPI with `twine`:

   ```bash
   (.venv) $ twine upload dist/*
   ```

Refer to the official PyPI packaging guides if you need more detail.

---

## 13. Installing the Home Assistant Integration (Optional)

The `custom_components/raspyrfm` integration lets Home Assistant users
manage RaspyRFM gateways, learn RF codes, and expose control units as
entities.

1. Copy `custom_components/raspyrfm/` into your Home Assistant `config`
   directory under `custom_components/`.
2. Restart Home Assistant so it discovers the integration.
3. Configure the integration via Home Assistant’s UI:
   - Add the integration from **Settings → Devices & Services**.
   - Provide gateway host/port information.
   - Use the provided panel to capture codes and map them to entities.

The integration communicates with the same Python package shipped in
this repository, so any additional gateways or control units you add are
available inside Home Assistant as well.

---

## 14. Troubleshooting

| Symptom | Fix |
| --- | --- |
| `socket.timeout` during discovery | Ensure the gateway is powered, on the same subnet, and that UDP broadcast traffic is not blocked by your router or firewall. |
| `ValueError` when calling `set_channel_config()` | Check the required keys and regex constraints returned by `get_channel_config_args()` for your control unit. |
| Commands do nothing | Verify the gateway host/port, confirm the receiver is paired with the expected channel, and send the command multiple times to account for packet loss. |
| Import errors after adding new implementations | Run `client.reload_implementation_classes()` or restart your Python process so new subclasses are loaded. |

---

## 15. Getting Help

- Browse the auto-generated module reference inside `docs/_build/html`
  after running `make html`.
- Search the `tests/` directory for concrete examples of how payloads and
  channels are configured.
- File an issue on GitHub if you encounter bugs or want to propose
  enhancements.

Happy hacking!
