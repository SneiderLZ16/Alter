"""
app.py
Flask application exposing REST endpoints for Students, Teachers, Courses and Enrollments.
Includes CSV bulk upload endpoints with validation helpers.
"""
from flask import Flask, request, jsonify, send_from_directory, abort
from models import db, Student, Teacher, Course, Enrollment, init_db
from utils import read_csv_stream, validate_columns
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Ensure DB exists on startup
with app.app_context():
    init_db()

def validate_email(e):
    """Basic email validator (very small)."""
    return isinstance(e, str) and "@" in e and "." in e

# -------------------- Students CRUD --------------------
@app.route("/api/students", methods=["GET", "POST"])
def students():
    """
    GET: return list of students.
    POST: create a new student.
    """
    if request.method == "GET":
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students])
    data = request.get_json() or {}
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    dob = data.get("date_of_birth")
    if not (first_name and last_name and email and validate_email(email)):
        return jsonify({"error":"first_name, last_name and valid email required"}), 400
    student = Student(first_name=first_name.strip(), last_name=last_name.strip(), email=email.strip(), date_of_birth=dob)
    db.session.add(student)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"email already exists"}), 400
    return jsonify(student.to_dict()), 201

@app.route("/api/students/<int:sid>", methods=["GET","PUT","DELETE"])
def student_detail(sid):
    """Get, update or delete a student by id."""
    student = Student.query.get_or_404(sid)
    if request.method == "GET":
        return jsonify(student.to_dict())
    if request.method == "DELETE":
        db.session.delete(student)
        db.session.commit()
        return jsonify({"deleted": True})
    # PUT update
    data = request.get_json() or {}
    student.first_name = data.get("first_name", student.first_name)
    student.last_name = data.get("last_name", student.last_name)
    email = data.get("email", student.email)
    if not validate_email(email):
        return jsonify({"error":"invalid email"}), 400
    student.email = email
    student.date_of_birth = data.get("date_of_birth", student.date_of_birth)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"email already exists"}), 400
    return jsonify(student.to_dict())

# -------------------- Courses CRUD --------------------
@app.route("/api/courses", methods=["GET","POST"])
def courses():
    """List or create courses."""
    if request.method == "GET":
        return jsonify([c.to_dict() for c in Course.query.all()])
    data = request.get_json() or {}
    code = data.get("code")
    name = data.get("name")
    credits = int(data.get("credits") or 0)
    teacher_id = data.get("teacher_id")
    if not (code and name):
        return jsonify({"error":"code and name required"}), 400
    course = Course(code=code.strip(), name=name.strip(), credits=credits, teacher_id=teacher_id)
    db.session.add(course)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"course code must be unique"}), 400
    return jsonify(course.to_dict()), 201

@app.route("/api/courses/<int:cid>", methods=["GET","PUT","DELETE"])
def course_detail(cid):
    """Get, update or delete a course by id."""
    course = Course.query.get_or_404(cid)
    if request.method == "GET":
        return jsonify(course.to_dict())
    if request.method == "DELETE":
        db.session.delete(course)
        db.session.commit()
        return jsonify({"deleted": True})
    data = request.get_json() or {}
    course.code = data.get("code", course.code)
    course.name = data.get("name", course.name)
    course.credits = int(data.get("credits", course.credits))
    course.teacher_id = data.get("teacher_id", course.teacher_id)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"course code conflict"}), 400
    return jsonify(course.to_dict())

# -------------------- Teachers CRUD --------------------
@app.route("/api/teachers", methods=["GET","POST"])
def teachers():
    """List or create teachers."""
    if request.method == "GET":
        return jsonify([t.to_dict() for t in Teacher.query.all()])
    data = request.get_json() or {}
    fn = data.get("first_name"); ln = data.get("last_name"); email = data.get("email")
    if not (fn and ln and email):
        return jsonify({"error":"first_name, last_name, email required"}), 400
    teacher = Teacher(first_name=fn.strip(), last_name=ln.strip(), email=email.strip())
    db.session.add(teacher)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"teacher email must be unique"}), 400
    return jsonify(teacher.to_dict()), 201

@app.route("/api/teachers/<int:tid>", methods=["GET","PUT","DELETE"])
def teacher_detail(tid):
    """Get, update or delete a teacher by id."""
    teacher = Teacher.query.get_or_404(tid)
    if request.method == "GET":
        return jsonify(teacher.to_dict())
    if request.method == "DELETE":
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({"deleted": True})
    data = request.get_json() or {}
    teacher.first_name = data.get("first_name", teacher.first_name)
    teacher.last_name = data.get("last_name", teacher.last_name)
    teacher.email = data.get("email", teacher.email)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"teacher email conflict"}), 400
    return jsonify(teacher.to_dict())

# -------------------- Enrollments CRUD --------------------
@app.route("/api/enrollments", methods=["GET","POST"])
def enrollments():
    """List or create enrollments."""
    if request.method == "GET":
        return jsonify([e.to_dict() for e in Enrollment.query.all()])
    data = request.get_json() or {}
    student_id = data.get("student_id"); course_id = data.get("course_id"); grade = data.get("grade")
    if not (student_id and course_id):
        return jsonify({"error":"student_id and course_id required"}), 400
    # basic existence check
    if not Student.query.get(student_id) or not Course.query.get(course_id):
        return jsonify({"error":"student or course not found"}), 404
    enrollment = Enrollment(student_id=student_id, course_id=course_id, grade=grade)
    db.session.add(enrollment)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"student already enrolled in this course"}), 400
    return jsonify(enrollment.to_dict()), 201

@app.route("/api/enrollments/<int:eid>", methods=["GET","PUT","DELETE"])
def enrollment_detail(eid):
    """Get, update or delete an enrollment by id."""
    e = Enrollment.query.get_or_404(eid)
    if request.method == "GET":
        return jsonify(e.to_dict())
    if request.method == "DELETE":
        db.session.delete(e)
        db.session.commit()
        return jsonify({"deleted": True})
    data = request.get_json() or {}
    e.grade = data.get("grade", e.grade)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error":"update error"}), 400
    return jsonify(e.to_dict())

# -------------------- CSV Bulk Upload --------------------
@app.route("/api/upload/students", methods=["POST"])
def upload_students():
    """
    Upload students via CSV. Expected columns: first_name,last_name,email,date_of_birth
    Uses utils.validate_columns to ensure proper format.
    Returns inserted count and list of row errors.
    """
    if "file" not in request.files:
        return jsonify({"error":"file is required"}), 400
    f = request.files["file"]
    rows = read_csv_stream(f)
    required = ["first_name","last_name","email","date_of_birth"]
    ok, missing = validate_columns(required, rows[0].keys() if rows else [])
    if not ok:
        return jsonify({"error":"missing columns", "missing": missing}), 400
    inserted = 0; errors = []
    for i, row in enumerate(rows, start=1):
        try:
            fn = row.get("first_name"); ln = row.get("last_name"); email = row.get("email"); dob = row.get("date_of_birth")
            if not (fn and ln and email):
                errors.append({"row":i, "error":"missing required field"}); continue
            s = Student(first_name=fn.strip(), last_name=ln.strip(), email=email.strip(), date_of_birth=dob)
            db.session.add(s)
            db.session.flush()
            inserted += 1
        except Exception as ex:
            db.session.rollback()
            errors.append({"row":i, "error":str(ex)})
    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return jsonify({"inserted": inserted, "errors": errors, "commit_error": str(ex)}), 500
    return jsonify({"inserted": inserted, "errors": errors})

@app.route("/api/upload/enrollments", methods=["POST"])
def upload_enrollments():
    """
    Upload enrollments via CSV. Expected columns: student_email,course_code
    It resolves student_email -> student.id and course_code -> course.id.
    """
    if "file" not in request.files:
        return jsonify({"error":"file is required"}), 400
    f = request.files["file"]
    rows = read_csv_stream(f)
    required = ["student_email","course_code"]
    ok, missing = validate_columns(required, rows[0].keys() if rows else [])
    if not ok:
        return jsonify({"error":"missing columns", "missing": missing}), 400
    inserted = 0; errors = []
    for i, row in enumerate(rows, start=1):
        try:
            student_email = row.get("student_email"); course_code = row.get("course_code")
            if not (student_email and course_code):
                errors.append({"row":i, "error":"missing required field"}); continue
            student = Student.query.filter_by(email=student_email.strip()).first()
            course = Course.query.filter_by(code=course_code.strip()).first()
            if not student or not course:
                errors.append({"row":i, "error":"student or course not found"}); continue
            e = Enrollment(student_id=student.id, course_id=course.id)
            db.session.add(e)
            db.session.flush()
            inserted += 1
        except IntegrityError as ex:
            db.session.rollback()
            errors.append({"row":i, "error":"duplicate or constraint"})
        except Exception as ex:
            db.session.rollback()
            errors.append({"row":i, "error":str(ex)})
    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return jsonify({"inserted": inserted, "errors": errors, "commit_error": str(ex)}), 500
    return jsonify({"inserted": inserted, "errors": errors})

# -------------------- Serve UI --------------------
@app.route("/", methods=["GET"])
def index():
    """Serve the static HTML UI for manual testing."""
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    # turn on debug for local use
    app.run(debug=True)
