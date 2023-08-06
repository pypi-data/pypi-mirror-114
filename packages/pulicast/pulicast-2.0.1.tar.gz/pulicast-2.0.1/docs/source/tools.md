# Tools

Pulicast comes with a number of tools to support you during development.
Some are written in C++ and come with the installation of the C++ pulicast package (`apt install kiteswarms-pulicast`), others
are written in Python. It is recommended to install them using [pipx](https://pipxproject.github.io/pipx/).

For detailed usage information, all tools have a `--help` flag.

## PuliPing (C++)

`puliping` is a tool for 1. sending ping probes, 2. echoing ping probes and 3. recording those echos.
By adding a unique ID to each ping, the recorded echos can be matched with the sent pings to compute
precise round-trip-times (rtt) and track message loss.
When running PuliPing you have to specify what probes to send and what probes to reflect back as an
echo.
This allows to model a large number traffic scenarios. Examples include:
 1. Measuring messages sent from a node to itself by telling PuliPing to probe and echo on the same
 probe.
 2. Measuring unidirectional traffic by starting two PuliPing instances where one instances just
 sends a probe and the other just reflect that probe.
 3. Measuring a star configuration where one PuliPing instance sends a probe and the others just
 reflect that probe
 4. Measuring bidirectional traffic flow with two PuliPing instances Alice and Bob.
 Alice sends probe "A" and Bob reflects probe "A". Bob sends probe "B" and Alice relfects probe "B".

## ZCMPing (C++)

`zcmping` is a tool just like PuliPing with the only change that it uses ZCM as a backend.
it was build to measure traffic going through a `puli_zcm_bridge`.

## Pulicast-ZCM Bridge (C++)

`puli_zcm_bridge` forwards messages between pulicast and [ZCM](https://github.com/ZeroCM/zcm).
It was designed to help transitioning from ZCM to pulicast.

## PuliLog (C++)

`pulilog` records pulicast messages and writes them to a log file in the ZCM log format just like the `zcm-logger` does
for ZCM.

## PuliScope (Python)

Installation:

```bash
pipx install kiteswarms-pulicast
```

PuliScope is a GUI tool for showing a graph of the currently running pulicast node and how they publish/subscribe to channels.

## PuliSniffer and PuliLogSniffer (Python)

Installation:

```bash
pipx install kiteswarms-puli-sniffer
```

`puli-sniffer` is a command line tool for displaying active pulicast channels and the messages arriving on those channels.
It serves approximately the same purpose as `zcm-spy-lite`.

`puli-log-sniffer` is a command line tool for displaying distributed log messages.
