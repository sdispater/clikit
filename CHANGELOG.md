# Change Log

## [0.5.1] - 2020-03-27

### Fixed

- Improved the error message display for multiline messages ([#21](https://github.com/sdispater/clikit/pull/21)).


## [0.5.0] - 2020-03-26

### Added

- Errors are now rendered in a nicer way for Python 3.6+ ([#19](https://github.com/sdispater/clikit/pull/19)).


## [0.4.3] - 2020-03-20

### Fixed

- Fixed encoding errors in questions for Python 2.7.


## [0.4.2] - 2020-02-28

### Fixed

- Fixed the terminal width being set to 0 in some circumstances ([#15](https://github.com/sdispater/clikit/pull/15)).
- Fixed the comptibility with the latest version of [pastel](https://github.com/sdispater/pastel) ([#10](https://github.com/sdispater/clikit/pull/10)).


## [0.4.1] - 2019-12-06

### Fixed

- Fixed the rendering of exception traces on Python 2.7


## [0.4.0] - 2019-10-25

### Changed

- Changed the way event names are stored and exposed.


### Fixed

- Fixed parsing of options after a `--` token.


## [0.3.2] - 2019-09-20

### Fixed

- Fixed handling of `KeyboardInterrupt` exceptions.


## [0.3.1] - 2019-06-24

### Fixed

- Fixed hidden command being displayed.


## [0.3.0] - 2019-06-24

### Added

- Added support for displaying multiple, independent progress bars.

### Fixed

- Fixed similar command names suggestions.
- Fixed the `help` command not displaying the help text of commands.


## [0.2.4] - 2019-05-11

### Fixed

- Fixed `help` command not displaying help for sub commands.
- Fixed possible errors for raised exceptions with a non-int `code` attribute.


## [0.2.3] - 2018-12-10

### Fixed

- Fixed handling of ANSI support detection in output.


## [0.2.2] - 2018-12-08

### Changed

- Write line methods will now always write `\n` instead of `os.linesep`.


## [0.2.1] - 2018-12-07

### Changed

- The `help` command will now insert the script name and command name where needed.

### Fixed

- Fixed handling of paragraph in help.


## [0.2.0] - 2018-12-06

### Added

- Added a basic event system.
- Added a `NullIO` class for no-op IO operations.
- Added a progress bar component.
- Added a `hidden` property on command configurations.

### Fixed

- Fixed help display for multi valued options.
- Fixed the progress indicator component.


[Unreleased]: https://github.com/sdispater/tomlkit/compare/0.5.1...master
[0.5.1]: https://github.com/sdispater/tomlkit/releases/tag/0.5.1
[0.5.0]: https://github.com/sdispater/tomlkit/releases/tag/0.5.0
[0.4.3]: https://github.com/sdispater/tomlkit/releases/tag/0.4.3
[0.4.2]: https://github.com/sdispater/tomlkit/releases/tag/0.4.2
[0.4.1]: https://github.com/sdispater/tomlkit/releases/tag/0.4.1
[0.4.0]: https://github.com/sdispater/tomlkit/releases/tag/0.4.0
[0.3.2]: https://github.com/sdispater/tomlkit/releases/tag/0.3.2
[0.3.1]: https://github.com/sdispater/tomlkit/releases/tag/0.3.1
[0.3.0]: https://github.com/sdispater/tomlkit/releases/tag/0.3.0
[0.2.4]: https://github.com/sdispater/tomlkit/releases/tag/0.2.4
[0.2.3]: https://github.com/sdispater/tomlkit/releases/tag/0.2.3
[0.2.2]: https://github.com/sdispater/tomlkit/releases/tag/0.2.2
[0.2.1]: https://github.com/sdispater/tomlkit/releases/tag/0.2.1
[0.2.0]: https://github.com/sdispater/tomlkit/releases/tag/0.2.0
[0.1.0]: https://github.com/sdispater/tomlkit/releases/tag/0.1.0
