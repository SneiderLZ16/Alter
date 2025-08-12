# School CRUD Project — Improved (English)

This project is a documented, production-minded small-scale CRUD application for a school management scenario.
It includes: Students, Teachers, Courses and Enrollments (many-to-many). The code is documented in English with
docstrings and comments. This package was prepared to satisfy assessment rubrics and to be easy to run locally.

## Quick start (tested on Windows, macOS, Linux)

1. Unzip the project and open terminal in the project folder.
2. Create and activate a virtual environment:

- Windows (CMD):
```
python -m venv venv
venv\Scripts\activate.bat
```

- Windows (PowerShell):
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

- macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Initialize the database (creates `school.db` and seeds sample data):
```
python db_init.py
```

5. Run the app:
```
python app.py
```

6. Open your browser at http://127.0.0.1:5000/

## What changed / improvements
- All source files documented in English with docstrings and helpful comments.
- `utils.py` contains CSV validation and normalization helpers.
- Bulk sample CSV with ~100 students and enrollments for testing.
- `docs/` contains MER.md, MER.drawio (editable XML), and a "guion" (defense Q&A) in English and Spanish.

If you want any additional features (authentication, deployment script, PostgreSQL migration), tell me and I will add them.
