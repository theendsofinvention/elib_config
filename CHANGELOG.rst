Changelog
=========
2018.10.24.1 (2018-10-24)
-------------------------
Changes
~~~~~~~
- Switch to tomlkit (#15) [etcher]
  * chg: dev: update reqs
  * chg: dev: create root logger object
  * chg: dev: create static Types translation
  * chg: dev: move validate in its own module
  * chg: switch over to using tomlkit instead of toml
  * fix: dev: linting
  * chg: dev: remove useless check
  * chg: dev: config_value_path __init__
  Remove __init__ parameters to pre-declare a path as file, dir, or
  must_exist.
  * chg: dev: add checks for must_be_file/dir
  * chg: dev: path: deterministic constraints
  * fix: fix default key in tables arrays
  * chg: dev: no cover (trivia)
  * chg: dev: fix/add tests
  * fix: dev: simplify code
  * fix: dev: simplify code
  * chg: dev: extract TOML logic in its own module
2018.10.15.1 (2018-10-15)
-------------------------
New
~~~
- Error info (#12) [etcher]
  * chg: add a tiny bit more info when parsing fails
  Working on #10
  * new: dev: test single quoted strings
  * chg: dev: update reqs
  * fix: boolean config values are lowercase
  This should be shown as such in the example config file
  * chg: dev: (trivia) linting
  * fix: dev: linting
  * chg: dev: update reqs
2018.09.16.1 (2018-09-16)
-------------------------
Fix
~~~
- Fix integer ret type (#9) [etcher]
  * update reqs
  * fix integer value return type
2018.09.02.1 (2018-09-02)
-------------------------
Fix
~~~
- Fix conftest.py (#8) [etcher]
  * fix: fix conftest.py
  * update reqs
  * chg: dev: remove assert
  * ignore graphs
  * update reqs
2018.08.27.4 (2018-08-27)
-------------------------
Fix
~~~
- Update header for example file to reflect TOML (#7) [etcher]
2018.08.27.3 (2018-08-27)
-------------------------
- Create LICENSE. [etcher]
2018.08.27.2 (2018-08-27)
-------------------------
- Update README.md. [etcher]
2018.08.27.1 (2018-08-27)
-------------------------
Changes
~~~~~~~
- Finishing up (#6) [etcher]
  * update reqs
  * switch to pyproject.toml
  * remove unused fixture
  * ignore .eggs
2018.08.25.1 (2018-08-25)
-------------------------
- Use epab (#5) [etcher]
  * clean up test_requirements in setup.py
  * update reqs
  * add epab to reqs
  * remove build files
  * add dummy epab.yml
- Linting. [etcher]
- Update imports in tests. [etcher]
- Add a check for missing and duplicate values. [etcher]
- Infer config value path at runtime. [etcher]
- Reset os.environ after every test. [etcher]
- Expose write_example_config_file. [etcher]
- Expose SENTINEL. [etcher]
- Export ConfigValueInteger. [etcher]
- Add integer config value (#4) [etcher]
- Expose config values. [etcher]
- Add optional path root for config values (#3) [etcher]
- Update setup.py & lint (#2) [etcher]
  * add dev reqs to setup.py
  * update trove classifiers
  * add config file for BetterCodeHub
  * tweaking BCH config
  * ignore config example header as well
  * ignore config example header as well
  * split codebase into sub-packages
  * tweaking BCH config
  * linting
  * some more linting
- Initial commit. [etcher]
  First version of the library
- Init commit. [132nd-etcher]