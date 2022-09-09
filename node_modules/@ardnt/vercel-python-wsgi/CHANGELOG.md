# Changelog

## 1.1.0 - 2021-04-20 - Zeit Now is now called Vercel

### Added
- Supported runtime Python 3.8

### Changed
- Upgraded builder packages
- Upgraded handler packages
- Moved all `@now/` prefixed build utilities to `@vercel/` prefix
- Renamed package to `vercel-python-wsgi`

### Removed
- Runtime Python 2.7 (no longer supported by Vercel)


## [1.0.11] - 2019-11-03 - Upgrade eslint-utils & werkzeug

### Changed
- Upgraded packages


## [1.0.10] - 2019-08-08 - Python 3.6 fix

### Changed
- Updated runtime and binary checking for new Zeit container
- Upgraded dependencies


## [1.0.9] - 2019-04-26 - Python 2.7 support

### Added
- Added a runtime validation step to interrupt the build if the user has
   configured an unsupported runtime.
- Added a warning if the python version implied by `runtime` is not available in
   the build environment. Falls back to a system python.
- Tests for Python 2.7.
- Updated requirements discussion in `README.md` to be consistent with revised
   requirements handling.


## [1.0.8] - 2019-04-16 - Organization migration

### Changed
- Migrated NPM and GitHub repositories to updated organization
- Updated readme to match new repository


## [1.0.7] - 2019-03-14 - Fixes for multi-value headers

### Changed
- Fixed url unquoting of query strings in the handler
- Fixed base64 encoding of responses in the handler (now passing `encoding` in
   the return dictionary).
- Fixed multi-value cookie handling (now passing multi-value cookies as a list
   of values for each key).


## [1.0.6] - 2019-03-14 - Fixes for base64 encoded bodies

### Changed
- Fixed base64 handling in the handler. Request bodies were previously being
   passed on to the application without decoding, but with padding stripped
   (preventing decoding by the application).


## [1.0.5] - 2019-03-13 - Fixes for querystrings and empty response bodies

### Changed
- Handler is now installed as a python package instead of being copied into the
   project source.
- Querystring handling has been corrected.
- Empty return body handling has been patched to match Now's requirement of a
   `body` object on the response. An empty body is returned if no body is
   supplied by the application.


## [1.0.4] - 2019-03-13 - Ensure logging configuration

### Added
- Logging is now configured with `logging.basicConfig()` in `handler.py` to
   ensure logging is initialized at the module level.


## [1.0.3] - 2019-03-10

### Changed
- Fixed typo in `index.js` which was appearing in logs


## [1.0.2] - 2019-03-10 - Selectable runtime

### Added
- Configuration option `runtime` can now be used to set the lambda runtime,
   e.g., `python3.6`. *The build environment is not affected, beware of
   issues building in Python 3.5 and running and other versions.*

### Changed
- Improved builder log output (`log.js`)
- Consolidated pip activities to `pip.js`

### Removed
- No longer installs `Werkzeug` every time. Projects will need to include
   `Werkzeug` as a dependency in their project `requirements.txt`. If a
   `requirements.txt` file is not found, the builder will install `Werkzeug`
   assuming the project has no other dependencies.


## [1.0.1] - 2019-03-03 - Fix logging

### Added
- Stubbed testing with a single GET request test and test configuration

### Changed
- Removed `print` calls from `now_python_wsgi.handler.handler()` to prevent
   printing sensitive data to longs (e.g., passwords passed in the body of a
   request).


## 1.0.0 - 2019-03-02 - Getting started!
We're just getting started. This establishes a tidy repository ready for the
world.


[1.0.11]: https://github.com/ardnt/now-python-wsgi/compare/v1.0.10...v1.0.11
[1.0.10]: https://github.com/ardnt/now-python-wsgi/compare/v1.0.9...v1.0.10
[1.0.9]: https://github.com/ardnt/now-python-wsgi/compare/v1.0.8...v1.0.9
[1.0.8]: https://github.com/ardnt/now-python-wsgi/compare/v1.0.7...v1.0.8
[1.0.7]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.6...v1.0.7
[1.0.6]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/ardent-co/now-python-wsgi/compare/v1.0.0...v1.0.1
