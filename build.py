# coding=utf-8

import subprocess

_SAFETY = 'pipenv run safety check --bare'
_FLAKE8 = 'pipenv run flake8 --ignore=D203,E126 --max-line-length=120 --exclude .svn,CVS,.bzr,.hg,.git,__pycache__,' \
          '.tox,__init__.py,build,dist,output,.cache,.hypothesis,./test/*,./.eggs/*, --max-complexity=10'
_PYLINT = ''.join(
    [
        'pipenv run pylint ./elib_config --reports=n --ignore=CVS --max-line-length=120 -j 8 --persistent=y ',
        """--init-hook="import sys; sys.path.append('.venv')" """,
        '-d disable=logging-format-interpolation,fixme,backtick,long-suffix,raw-checker-failed,bad-inline-option,',
        'locally-disabled,locally-enabled,suppressed-message,coerce-method,delslice-method,getslice-method,',
        'setslice-method,next-method-called,too-many-arguments,too-few-public-methods,reload-builtin,oct-method,',
        'hex-method,nonzero-method,cmp-method,using-cmp-argument,eq-without-hash,exception-message-attribute,',
        'sys-max-int,bad-python3-import,logging-format-interpolation,wrong-import-order,logging-fstring-interpolation,',
        '--evaluation="10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)"',
        '--output-format=text --score=n'
    ]
)
_PYTEST = 'pipenv run python -m pytest test --cov=elib_config --cov-report xml --cov-report html --cov-branch ' \
          '--durations=20 --tb=short --cov-config .coveragerc'

if __name__ == '__main__':
    subprocess.call(_SAFETY, shell=True)
    subprocess.call(_FLAKE8, shell=True)
    subprocess.call(_PYTEST, shell=True)
    # for task in (
    #     _SAFETY,
    #     _FLAKE8,
    #     _PYLINT,
    # ):
    #     # subprocess.check_call(task, shell=True)
    #     subprocess.call(task, shell=True)
