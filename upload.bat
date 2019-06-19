@echo off
py setup.py sdist 2>nul >nul
twine upload dist/* --skip-existing