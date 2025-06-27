PORT="$1"

kill -9 $(lsof -ti ":PORT") 2>/dev/nulkl
git pull
python3 -m venv .venv
pip install -r requierments.txt
gunicorn -b ":PORT" app:app