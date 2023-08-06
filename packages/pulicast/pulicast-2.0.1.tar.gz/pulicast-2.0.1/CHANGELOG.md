# Changelog

Until there is a dedicated guide how to use this log, please stick to this article:
https://keepachangelog.com/de/0.3.0/

Please pick from the following sections when categorizing your entry:
`Added`, `Changed`, `Removed`, `Fixed`

and put the following change severity in brackets (see the above link for details):
`Major`, `Minor`, `Patch`

## Unreleased

## [2.0.1] 2021-07-27

### Changed
- [Patch] Fix installation instructions, copyright headers, installation instructions and remove references to kiteswarms.com

## [2.0.0] 2021-07-23
## Changed
- [Major] Rename package to `pulicast`
- [Patch] Change registry path for ci jobs and remove slow tests tox job. 

## [1.6.0] 2021-07-22

### Added
- [Minor] Added reset first and unset first options to puliconf.
- [Patch] GPLv3 license.

### Removed
- [Patch] Removed dependencies to zcom and kiteswarms-ci.

## [1.5.1] 2021-06-29
- [Patch] Fix bug in puliscope launcher.

## [1.5.0] 2021-06-28

### Fixed
- [Patch] Fixed bug that caused SettingView to fail on int settings other than int64 ones.

### Added
- [Minor] Added puliconf command line tool.

### Changed
- [Patch] Introduced proper setuptools "extras" to only install the library, or the library with tools.

## [1.4.0] 2021-06-10
### Added
- [Minor] Added new validation function generators for puliconf settings
  
### Fixed
- [Patch] Switched from `warnings.warn` to `logging.warning` where it is more appropriate.

## [1.3.3] 2021-06-07

### Added
- [Minor] Added support for distributed settings with new roc_ack protocol including a new settings discovery system.
- [Minor] Added a settings view in puliscope.

### Fixed
- [Patch] Fix bug in ObservableDict.clear()
- [Patch] Fixed bug that caused primitive values not to be properly decoded by the universal decoder.

### Removed
- [Minor] Removed the properties view from puliscope.

## [1.3.2] 2021-06-07

### Added
- [Minor] Added a subscription handle to allow for unsubscribing from channels.
- [Minor] Added functions to asynchronously iterator over messages on a channel using trio.

### Fixed
- [Patch] Fixed bug in ordered subscription.

##Fixed
- [Patch] Fixed channel incompatibilities on Windows (which uses `\` as default).

## [1.3.1] 2021-04-12

### Fixed
- [Patch] Make the node iterable again

## [1.3.0] 2021-04-09

### Added
- [Minor] Not nodes, but channels operate in namespaces
- [Minor] Nodes operate in namespaces
- [Patch] Merge request template

## [1.2.1] 2021-03-08

### Changed
- [Minor] Unify the pulicast transport implementations

## [1.1.2] 2021-02-22

- [Patch] Fix a bug caused by trying to close a send_socket, that does not exist any more in the current implementation.

## [1.1.1] 2021-02-15

- [Patch] Fixed bug that caused us to bleed multicast messages even if ttl=0

## [1.1.0] 2021-01-11

### Added
- [Minor] Add function to pause and resume subscriptions to the ThreadedNode.

### Fixed
- [Patch] Fixed broken pulijit constructor call
- [Patch] Add workaround for https://bugs.python.org/issue29256

## [1.0.0] 2020-12-04
 
### Added
- [Minor] Added a widget in PuliScope to visualize message frequencies

### Changed
* [Major] Simplify the interface to the transport layer and thereby change the wire format. 
  CAN NOT COMMUNICATE WITH OLDER PULICAST VERSIONS! 

## [0.10.0] 2020-12-03

### Changed
* [Patch] Make ObservableSet inherit from the python buildin set.
* [Patch] Add notes to the documentation to warn that exceptions due to wrong network interfaces are only thrown when subscribing.
* [Major] Cleaned up the start/stop logic of nodes.

## [0.9.1] 2020-11-19

### Changed
* [Patch] Fix bug of the qt transport failing to bind to multicast adresses under windows.

## [0.9.0] 2020-11-17

### Changed
* [Patch] Fix bug in channel discoverer that prevented it from discovering unused channels.

### Added
* [Patch] Add --port command line argument to puliscope.

## [0.8.0] 2020-10-26

### Changed
 * [Patch] Minor fixes in the examples.
 * [Patch] Exiting puliscope with ctrl+c fixed.
 
### Added
 * [Patch] DEFAULT_PORT constant.


## [0.7.0] 2020-10-26

### Changed
 * [Minor] Subscribe without delay when using the Trio Backend.
 * [Patch] Fixed typos in documentation
 * [Minor] Reorganized and renamed some classes so that users don't have to access `pulicast.core`.
 * [Minor] Fixed bugs in imports within the discovery module and added regression tests.
 
### Added
 * [Minor] Add zcm to pulicast migration guide.

### Removed
* [Minor] Removed tests for Qt content since they fail in CI/CD.

### Fixed
* [Patch] Fixed installation docu

## [0.6.0] - 2020-09-29

### Changed
* [Patch] Fix broken install instructions for puliscope.
* [Minor] Improved warnings of the discovery module.
* [Patch] Remove pytypes requirement for python3.8 and leave it for py36 via conditionals.

## [0.5.0] - 2020-09-23

### Changed
* [Minor] Adapted the lead computation to make it easier to understand and use.
* [Minor] Rename SocketNode to ThreadedNode
* [Minor] Fixes to the concurrency article
* [Minor] Minor fixes in documentation and code style.

### Added
* [Minor] Added more documentation and improved it a bit in general.
* [Minor] Entrypoint for puliscope.
* [Minor] Added graphviz dependency.
* [Minor] Make puliscope an install option.
* [Minor] Add documentation for pulicast tools.

## [0.4.0] - 2020-07-16

### Changed
* [Patch] Fix some regression bugs.
* [Patch] Adapt the tox file for new CI scripts.
* [Patch] Use standard release CI jobs.
* [Patch] Minor fixes to setup.py to enable package creation via setup.py

### Added
* [Patch] Add documentation (including dummy pages to fill out later).
* [Patch] Add unit tests.
* [Minor] Source property in NodeView of the discovery api.


## [0.3.0] - 2020-07-03

### Changed
* [Patch] Change folder structure to conform to our internal standards including a `src/` folder
* [Patch] Remove clutter on stdout
* [Patch] Various little fixes that emerged from code review during API documentation.

### Added
* [Patch] Add a changelog
* [Patch] Setup an initial testing skeleton
* [Patch] Setup infrastructure to upload to pypi server
* [Patch] Add API documentation
