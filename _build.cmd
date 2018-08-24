FOR %%x IN (_safety.cmd,_flake8.cmd,_pylint.cmd,_mypy.cmd,_pytest.cmd) DO call %%x || exit /B 1
