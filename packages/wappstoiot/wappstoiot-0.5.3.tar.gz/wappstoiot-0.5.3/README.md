Wappsto IoT
===============================================================================

[![Build Status](https://travis-ci.com/Wappsto/python-wappsto-iot.svg?branch=master)](https://travis-ci.com/Wappsto/python-wappsto-iot)
[![Coverage Status](https://coveralls.io/repos/github/Wappsto/python-wappsto-iot/badge.svg?branch=master)](https://coveralls.io/github/Wappsto/python-wappsto-iot?branch=master)

The wappstoiot module provide a simple python interface to [wappsto.com](https://wappsto.com/) for easy prototyping.


## Prerequisites

A [wappsto.com](https://wappsto.com/) Account, that the unit can connect to.

The wappsto module requires a set of certificates for authentication. The certificates can be downloaded from [wappsto.com](https://wappsto.com/), or with the build-in CLI tool: `python3 -m wappstoiot`.
The certificates provides the unit with the secure connection to wappsto.com.

To read more about how the Wappsto IoT work behind the screen go [here](https://documentation.wappsto.com).

## The Basics

To understand how to use Wappsto IoT, there is some terms that need to be known.
* Control
    - Change request value.
* Report
    - The current value.
* Refresh
    - Value Update request.
* Delete
    - inform that a delete have happened.
* network -> device -> value
    - ...

## Getting Started

Working examples of usage can be found in the [example folder](./example).

### Echo example

The following explains the example code found in [info.py](./example/echo.py).

```python
network = wappstoiot.Network(
    name="echo",
    configFolder="echo"
)
```

```python
device = network.createDevice(
    name="EchoDevice"
)
```

```python
value = device.createValue(
    name="Moeller",
    value_type=wappstoiot.ValueType.STRING
)
```

```python
value.onControl(
    callback=lambda obj, new_value: obj.report(new_value)
)
```

```python
value.onRefresh(
    callback=lambda obj: obj.report(f"{obj.data} Refreshed!")
)
```

```python
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    network.close()
```


## Installation using pip

The wappsto module can be installed using PIP (Python Package Index) as follows:

```bash
$ pip install -U wappstoiot
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details.

