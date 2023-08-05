# Overview
This is a Pure Python PPS interface following RFC2783. A PPPPS interface,
if you would.

The has the unfortunate task of rolling-up some system and implementation
specific knowledge into the Python layers. I could have thrown in the towel and
added dependencies on `cython` and `timepps` interfaces on the system, but that
would have required external dependencies and added build complexity.

# Prerequisites
Python: 2.7+, 3.5+

OSs:
* Linux
* FreeBSD

Note that Linux support may vary depending on the platform, as the `ioctl`
request values vary ever so slightly (and annoyingly). This is setup to use
the asm-generic `ioctl` constants, which should work on ARM and x86\_64. Buyer
beware.

# Interface
This strives to implement a reasonable subset of RFC2783 with python
abstractions instead of nitty-gritty C structures. Under the hood, there _are_
nitty-gritty C structures (care of `ctypes`) to interface with the kernel.

More information can be found at https://datatracker.ietf.org/doc/html/rfc2783.

This library does NOT support optional behavior, such as:
* the `ntp_fp_t` timestamp format
* `kcbind`

# Installation
From pypi:
```
pip install pps-tools
```

From your local checkout:
```
pip install [--user] .
```

or

```
python setup.py install [--user]
```

# Usage

## Command-line
This installs a `pps-tools` command with the `fetch` and `params` subcommands.
Access to the PPS devices, especially setting parameters may require elevated
privileges.

The `fetch` command mirrors `time_pps_fetch()`, printing out the assert or
clear events for the PPS device, depending on its current mode. This includes
the event time and count. The event assert or clear will be printed depending
on the device's current mode.

```
$ pps-tools fetch /dev/pps0
assert 8078 @ 1627007608.079880476
assert 8079 @ 1627007609.093453169
...
```

The `params` command mirrors `time_pps_getparams()` and `time_pps_setparams()`.
After optionally setting parameters, the updated params are fetched and printed
to stdout. In addition, this prints out the capabilities (`time_pps_getcap()`)
in a verbose fashion.

```
$ pps-tools params /dev/pps0
API Version         : 1
Assert Offset       : 0.0
Clear Offset        : 0.0
Current Mode        : 0x1111 - PPS_CAPTUREASSERT, PPS_OFFSETASSERT, PPS_CANWAIT, PPS_TSFMT_TSPEC
Capabilities        : 0x4369
  PPS_CAPTUREASSERT : 1
  PPS_CAPTURECLEAR  : 0
  PPS_OFFSETASSERT  : 1
  PPS_OFFSETCLEAR   : 0
  PPS_ECHOASSERT    : 0
  PPS_ECHOCLEAR     : 0
  PPS_CANWAIT       : 1
  PPS_CANPOLL       : 0
  PPS_TSFMT_TSPEC   : 1
  PPS_TSFMT_NTPFP   : 0
```

## Python Library
The PPS interface can be used in Python through the `PpsFile` class. Example:
```
import pps_tools

with pps_tools.PpsFile("/dev/pps0") as ppsf:
    capabilities = ppsf.get_cap()
    print(pps_tools.data.cap_to_dict(capabilities))

    params = ppsf.get_params()
    params['mode'] = pps_tools.data.PPS_CAPTUREASSERT
    ppsf.set_params(**params)

    edge = ppsf.fetch(timeout=None)
    print(edge)
```

See the `PpsFile` method documentation for more information.

The library takes care of mapping Python objects to the underlying C structures
for the given platform. It also takes care of calling `CREATE` and `DESTROY`
`ioctls` for the given file, even though it doesn't usually do anything in the
kernel.

The `pps_tools.data` module contains the C structures and `ioctl` constants for
the given platform. These can be used if one wishes to interact with the PPS
device directly.
