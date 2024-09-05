python -m ensurepip --upgrade
pip install requests
if [ "$#" -gt 0 ]; then
  python frcwr.py "$@"
else
  python frcwr.py
fi
