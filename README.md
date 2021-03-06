elib_config
===========

[![<3 Open Source](https://badges.frapsoft.com/os/v3/open-source-200x33.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

[![Cheese shop](https://img.shields.io/pypi/status/elib_config.svg)](https://pypi.python.org/pypi/elib_config/)
[![License](https://img.shields.io/github/license/etcher-be/elib_config.svg)](https://github.com/etcher-be/elib_config/blob/master/LICENSE)
[![Appveyor build](https://img.shields.io/appveyor/ci/132nd-etcher/elib-config/master.svg?label=master)](https://ci.appveyor.com/project/132nd-etcher/elib-config)
[![Codacy grade](https://img.shields.io/codacy/grade/58cb5d65f3644ac790d8463749a350b6.svg)](https://www.codacy.com/app/etcher-be/elib_config)
[![Codacy coverage](https://img.shields.io/codacy/coverage/58cb5d65f3644ac790d8463749a350b6.svg)](https://www.codacy.com/app/etcher-be/elib_config)
[![Requires.io](https://requires.io/github/etcher-be/elib_config/requirements.svg?branch=master)](https://requires.io/github/etcher-be/elib_config/requirements/?branch=master)
[![CodeClimate maintainability](https://img.shields.io/codeclimate/maintainability/etcher-be/elib_config.svg)](https://codeclimate.com/github/etcher-be/elib_config)
[![BetterCodeHub](https://bettercodehub.com/edge/badge/etcher-be/elib_config?branch=master)](https://bettercodehub.com/results/etcher-be/elib_config)
[![OSI Best Practices](https://bestpractices.coreinfrastructure.org/projects/2145/badge)](https://bestpractices.coreinfrastructure.org/projects/2145)
[![CodeFactor](https://www.codefactor.io/repository/github/etcher-be/elib_config/badge)](https://www.codefactor.io/repository/github/etcher-be/elib_config)

[![Throughput Graph](https://graphs.waffle.io/etcher-be/elib_config/throughput.svg)](https://waffle.io/etcher-be/elib_config/metrics/throughput)

My own poor little attempt at a config lib.

I want configuration to live in a TOML file (maybe PEP518 will take off, and I'd like to give TOML a try anyway).

I also want config values set in the OS environment to take precedence.

I want config values to exist in a hierarchic tree.

I want config values to be type-checked, and casted to the correct type at runtime. Obviously, those types must be 
checked.

I want config values with default values, and config values without. Those without should be considered "mandatory" 
config values.  

All of those checks must raise corresponding exceptions.

Finally, since configuration evolves with the package, it's hard to keep track of. Therefore, I want the config 
package to create an example config file based on the config values that have been declared, and nothing else.

This package does about all that, hopefully in a consistent way.
