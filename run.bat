@echo off
set argc=0
for %%x in (%*) do Set /A argc+=1
python -m ensurepip --upgrade
pip install requests
if argc GTR 0 (python frcwr.py %*) ELSE (python frcwr.py)
