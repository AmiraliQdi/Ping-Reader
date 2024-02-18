# ping-python

<a href="https://bluerobotics.com">
<img src="https://avatars2.githubusercontent.com/u/7120633?v=3&s=200" align="left" hspace="10" vspace="6">
</a>

[![Travis Build Status](https://travis-ci.org/bluerobotics/ping-python.svg?branch=master)](https://travis-ci.org/bluerobotics/ping-python)
[![Gitter](https://img.shields.io/badge/gitter-online-green.svg)](https://gitter.im/bluerobotics/discussion/)
[![PyPI version](https://badge.fury.io/py/bluerobotics-ping.svg)](https://badge.fury.io/py/bluerobotics-ping)

Python library for the Ping sonar. Ping is the simple, affordable, and compact ultrasonic altimeter for any aquatic
project.

This library exposes all functionality of the device, such as getting profiles, controlling parameters, switching modes,
or just simply reading in the distance measurement.

[Available here](https://www.bluerobotics.com/store/sensors-sonars-cameras/sonar/ping-sonar-r2-rp/)

<br/>
<br/>

## Resources

* [API Reference](https://docs.bluerobotics.com/ping-python/)
* [Device Specifications](https://www.bluerobotics.com/store/sensors-sonars-cameras/sonar/ping-sonar-r2-rp/#tab-technical-details)

## Installing

### pip

```sh
$ pip install bluerobotics-ping --upgrade
```

 ---

## Scripts

### Ping360.py

Basic ping360 example to perform full scan (use correct args to run script).

### PingImageMaker

PingImageMaker.py file can be used to make image representing an output for sonar scan using ping api.

### PingScript

PingScript.py file save a csv file containing response from ping360 device.

### PingViewerReader

ping360 API files forked from [main](https://github.com/bluerobotics/ping-python) BlueRobotics git repo.

---

#### The library is ready to use: `import brping`. If you would like to use the command line [examples](/examples) or [tools](/tools) provided by this package, follow the notes in python's [installing to user site](https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site) directions (eg `export PATH=$PATH:~/.local/bin`).

---

## Quick Start

The `bluerobotics-ping` package installs a `simplePingExample.py` script to get started. Place your device's file
descriptor (eg. `/dev/ttyUSB0`, `COM1`) after the --device option.

`$ simplePingExample.py --device <your-device>`

It's also possible to connect via UDP server using the `--udp` option with IP:PORT as input (e.g `192.168.2.2:9090`).
