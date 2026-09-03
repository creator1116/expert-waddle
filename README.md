# Wiki Organization - Expert Waddle

This is a small Flask app added to the repository to provide a lightweight "wiki organization" feature (collections/books of links).

Quick start (local):

1. Create and activate a Python virtualenv (Python 3.8+ recommended).

2. Install dependencies:

   pip install -r requirements.txt

3. Initialize the database:

   python init_db.py

4. Run the app:

   flask run

The admin interface is protected by a simple password stored in the environment variable ADMIN_PASSWORD. If not set, admin actions are still allowed locally.

Files added:
- app.py (Flask application)
- models.py (SQLAlchemy models)
- init_db.py (create the SQLite database)
- requirements.txt
- README.md
- .gitignore
- templates/* (Jinja2 templates for UI)
- static/main.css, static/main.js

If you want me to open a pull request or create a branch/PR instead, tell me which branch name to use.