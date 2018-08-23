elib_config
===========

My own poor little attempt at a config lib.

I want configuration to live in a TOML file.

I also want config values set in the OS environment to take precedence.

I want config values should also exist in a hierarchic tree.

I want config values to be type-checked, and casted to the correct type at runtime. Obviously, those types must be 
checked.

I want config values with default values, and config values without. Those without should be considered "mandatory" 
config values.  

All of those checks must raise corresponding exceptions.

Finally, since configuration evolves with the package, it's hard to keep track of. Therefore, I want the config 
package to create an example config file based on the config values that have been declared, and nothing else.




[![<3 Open Source](https://badges.frapsoft.com/os/v3/open-source-200x33.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

[![Cheese shop](https://img.shields.io/pypi/status/epab.svg)](https://pypi.python.org/pypi/epab/)
[![License](https://img.shields.io/github/license/132nd-etcher/EPAB.svg)](https://github.com/132nd-etcher/epab/blob/master/LICENSE)
[![Appveyor build](https://img.shields.io/appveyor/ci/132nd-etcher/epab/master.svg?label=master)](https://ci.appveyor.com/project/132nd-etcher/epab)
[![Codacy grade](https://img.shields.io/codacy/grade/7413d0314ed44765a9dbde48b8c8277c.svg)](https://www.codacy.com/app/132nd-etcher/epab)
[![Codacy coverage](https://img.shields.io/codacy/coverage/7413d0314ed44765a9dbde48b8c8277c.svg)](https://www.codacy.com/app/132nd-etcher/epab)
[![Requires.io](https://requires.io/github/132nd-etcher/epab/requirements.svg?branch=master)](https://requires.io/github/132nd-etcher/epab/requirements/?branch=master)
[![CodeClimate maintainability](https://img.shields.io/codeclimate/maintainability/132nd-etcher/epab.svg)](https://codeclimate.com/github/132nd-etcher/epab)
[![BetterCodeHub](https://bettercodehub.com/edge/badge/132nd-etcher/epab?branch=master)](https://bettercodehub.com/results/132nd-etcher/epab)
[![OSI Best Practices](https://bestpractices.coreinfrastructure.org/projects/1548/badge)](https://bestpractices.coreinfrastructure.org/projects/1548)
[![CodeFactor](https://www.codefactor.io/repository/github/132nd-etcher/epab/badge)](https://www.codefactor.io/repository/github/132nd-etcher/epab)

[![Throughput Graph](https://graphs.waffle.io/132nd-etcher/epab/throughput.svg)](https://waffle.io/132nd-etcher/epab/metrics/throughput)
