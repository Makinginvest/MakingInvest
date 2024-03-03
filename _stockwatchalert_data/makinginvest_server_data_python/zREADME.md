brew update

brew upgrade python3

copy verions Pipfile to requirement.txt

# streamlit run \_streamlit/app.py --server.runOnSave true

# create venv

```
python -m venv __venv

```

# deactivate venv

deactivate

### Freeze pip

pip freeze > requirements.txt

# install from requirement txt

pip install --upgrade pip

pip install -r requirements.txt

# active env

pipenv shell

pip install --upgrade pip

# run server

uvicorn main:app --reload

# run server with app

PRODUCTION=False uvicorn app.main:app --host=0.0.0.0 --port=8999 --workers=4
PRODUCTION=False uvicorn app.main:app --host=0.0.0.0 --port=8999 --workers=8 --reload
