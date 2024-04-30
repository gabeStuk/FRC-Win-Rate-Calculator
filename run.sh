python -m ensurepip --upgrade
pip install requests
if ["$#" -gt 0]; then
  pythpn frcwr.py "$@"
else
  python frcwr.py
fi
