# Usage:
 - Clone the repo and run run.bat with `cmd /k run.bat` or with `py frcwr.py` if you've already got pip up to date.
 - You can also run this program from the actions tab by triggering the `Run Script` action (you will need to fork the repo):

[![Run Script](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/actions/workflows/run.yml/badge.svg)](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/actions/workflows/run.yml)
![Screenshot 2024-04-24 194905](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/assets/117952984/a03c4cb1-d4f8-455d-9286-2cdc2c645e77)
the output is located in the `run-py` job in the `(4) Run Python` step.

# Requirements:
 - requires [python](https://www.python.org/downloads) (tested and verified for 3.12)
    - for most systems, the `run.bat`/`run.sh` script will automatically install pip with `python -m ensurepip` if not installed. However, WSL users will have to install pip externally
    - or just use the action

# Note:
 - The `run.bat`/`run.sh` file is made explicitly to update pip, and therefore will not be necessary for further runs of the program, use `python frcwr.py` instead.
