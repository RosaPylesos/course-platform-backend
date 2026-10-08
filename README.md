# music-shop-backend

This is Backend part for music shop coursework,
made by using Python, FastAPI, Uvicorn, SqlAlchemy
and Alembic (with many more dependencies of theirs).
The Backend runs on FastAPI with PostgreSQL RDBMS.

# HOW TO RUN

First off, you need to switch your python on
venv in this directory. You can make this by:
```bash
.venv\Scripts\Activate\ps1
```

To run this thing you'll need to install the
modules from **requirements.txt** via pip.
to do so just write in terminal
```bash
pip install -r requirements.txt
```

To run the "Swagger" docs, you'll need to
run the server via uvicorn module. Currently,
in our case we'll use this command:
```bash
uvicorn app.main:app --reload
```
It will open up **localhost:8000**, so with
"/docs" directory you can have access to FastAPI
documentation.

# Migration Stuff

For now, it's the only command to run for migrating
DB schema on terminal, by using Alembic:
```bash
alembic upgrade head
```
This command will automatically upgrade your DB
schema and add all of necessary tables to it for
proper work.