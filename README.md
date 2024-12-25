# Usage
 - Clone the repository and run `run.bat`/`run.sh` with `cmd /k run.bat`/`bash run.sh`/`zsh run.sh` or with `python frcwr.py` if you've already got pip up to date

   Cmd:
   ```cmd
   git clone https://github.com/gabeStuk/FRC-Win-Rate-Calculator
   dir FRC-Win-Rate-Calculator
   cmd /K run.bat
   ```
   Bash:
   ```bash
   git clone https://github.com/gabeStuk/FRC-Win-Rate-Calculator
   cd FRC-Win-Rate-Calculator
   bash run.sh
   ```
   Zsh:
   ```zsh
   git clone https://github.com/gabeStuk/FRC-Win-Rate-Calculator
   cd FRC-Win-Rate-Calculator
   zsh run.sh
   ```
 - If you run the program after cloning the repository (without the action), you will need to supply an api key. Go [here](https://www.thebluealliance.com/account/login?next=http://www.thebluealliance.com/account) to make an account and then scroll down to the Read API Keys, add a new key, and copy the X-TBA-Auth-Key value into the program's prompt
 - You can also run this program from the actions tab by triggering the [![Run Script](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/actions/workflows/run.yml/badge.svg)](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/actions/workflows/run.yml) action (you will need to [fork](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/fork) the repository):


![Screenshot 2024-04-24 194905](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/assets/117952984/a03c4cb1-d4f8-455d-9286-2cdc2c645e77)
the output is located in the `run-py` job in the `(4) Run Python` step:
![Screenshot 2024-04-24 221159](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/assets/117952984/56e526e3-d744-447a-9660-8664e13f2ef2)
![Screenshot 2024-04-24 221219](https://github.com/gabeStuk/FRC-Win-Rate-Calculator/assets/117952984/6f9af872-c903-4675-b3a5-eea09ab7f1e1)



# Requirements
 - requires [python](https://www.python.org/downloads) (tested and verified for 3.12)
    - for most systems, the `run.bat`/`run.sh` script will automatically install pip with `python -m ensurepip` if not installed. However, WSL users will have to install pip seperately, which varies by distro, but [here](https://www.tecmint.com/install-pip-in-linux/) is a good article explaining the process for different package managers.
    - or just use the action

# Notes
 - The `run.bat`/`run.sh` file is made explicitly to update pip, and therefore will not be necessary for further runs of the program. Use `python frcwr.py` for future runs instead.
 - The start year and end year are optional parameters. The start year defaults to the later of the two teams' rookie years, and the end year defaults to the current season.
 - If you look at the action yml or python script, you will see that the script supports cli with mandatory inputs of `-team1` and `-team2` (self explanatory), the `-start` and `-end` years (optional), and an optional input for the api `-key` (overrides cached/inputted api key). Note this is only if you execute the python file directly as referenced in [Note 1](#notes).
