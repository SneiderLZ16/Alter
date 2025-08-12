"""
models.py
SQLAlchemy models for the School CRUD project.
Each model includes a `to_dict` convenience method for JSON serialization.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """
    Initialize the database (create tables).
    This function must be called within an application context.
    """
    db.create_all()

class Student(db.Model):
    """Student model: stores basic student information."""
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    date_of_birth = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        """Return a JSON-serializable representation of the student."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "created_at": str(self.created_at)
        }

class Teacher(db.Model):
    """Teacher model: information about teachers."""
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)

    def to_dict(self):
        """Return teacher dict for serialization."""
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "email": self.email}

class Course(db.Model):
    """Course model: each course has an optional teacher (FK)."""
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    credits = db.Column(db.Integer, default=0)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    teacher = db.relationship("Teacher", backref=db.backref("courses", lazy=True))

    def to_dict(self):
        """Return course information including linked teacher id."""
        return {"id": self.id, "code": self.code, "name": self.name, "credits": self.credits, "teacher_id": self.teacher_id}

class Enrollment(db.Model):
    """Enrollment model: associative table between Student and Course."""
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    grade = db.Column(db.String(10))
    enrolled_at = db.Column(db.DateTime, server_default=db.func.now())

    student = db.relationship("Student", backref=db.backref("enrollments", lazy=True))
    course = db.relationship("Course", backref=db.backref("enrollments", lazy=True))

    __table_args__ = (db.UniqueConstraint("student_id", "course_id", name="_student_course_uc"),)

    def to_dict(self):
        """Return json-serializable enrollment info."""
        return {"id": self.id, "student_id": self.student_id, "course_id": self.course_id, "grade": self.grade, "enrolled_at": str(self.enrolled_at)}
