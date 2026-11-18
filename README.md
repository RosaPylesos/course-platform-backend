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
also, for more information, this repo was made 
by using:
- **`Python 3.13.1`**
- **`pip 26.2.2`**
- **`PostgreSQL 18.6-4`**
so be sure that everything above this list is either 
the same version with your or above.

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
proper work. If you need to check your migration
status, try using "current" command:
```bash
alembic current
```
It will show whether your migration is on head or
not.

If you need to check SQLAlchemy relationships, 
you should probably use this command:
```bash
python -c "from sqlalchemy.orm import configure_mappers; from app.models import *; configure_mappers(); print('All model relationships configured successfully')"
```

One more horrendously large command to check 
DB dependency proper work is:
```bash
python -c "from app.database.connection import engine, SessionLocal; from app.api.dependencies import get_db; print('DB dependency imports successfully')"
```

# Misc
## Slugify strings
There've been used a **slugify** Python library,
if you want to test it's work, use this command:
```bash
python -c "from app.utils.slug import generate_slug; print(generate_slug('YOUR-STRING-TO-SLUG-HERE'))"
```
## JWT Token generation
Additionally, if you want to add/change JWT secret
token to .env, you can use this command:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Paste it to .env as __JWT_SECRET_KEY="your key here"__

## Seeding data via script.py
If you have some data that fits with validation,
(it needs to be in `.json` file format), you can
you **seed script** in the `scripts` folder.
for references - use `reference_data.json`, it 
can come in handy in cases when your data is about 
to be generated via LLM or AI Agents. That will help 
them to choose only preferable **`authors`, `topics`,**
**and `tags`**. Additionaly, there's an .md instruction for 
proper generation of those - it contains rules and constraints 
for required data to be generated.
when you data will be ready - rename the file to `courses_data.json` 
and use the terminal command down below:
```bash
python -m scripts.seed_courses
```
It will start to read data from your file and validate it 
with designed schemas for this operation. If there'll some 
mistake in validation, or the data you provided will be empty 
the script will notify you about this in your console window.