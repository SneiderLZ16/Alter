"""
db_init.py
Initializes the SQLite database (school.db) and seeds sample data.
Run once before starting the app.
"""
from models import db, init_db, Student, Teacher, Course, Enrollment
from flask import Flask
import os, random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

FIRST_NAMES = ["Alex","Ben","Carla","Diana","Ethan","Fatima","Gabriel","Hannah","Iker","Julia","Kevin","Laura","Miguel","Nora","Omar","Paula","Quinn","Rosa","Samuel","Tania","Ulysses","Valeria","Walter","Ximena","Yahir","Zoe"]
LAST_NAMES = ["Garcia","Lopez","Martinez","Rodriguez","Gonzalez","Perez","Sanchez","Ramirez","Torres","Flores","Rivera","Diaz","Vega","Reyes","Castro"]

with app.app_context():
    if os.path.exists("school.db"):
        os.remove("school.db")
    init_db()
    # Teachers
    t1 = Teacher(first_name="Ana", last_name="Lopez", email="ana.lopez@example.com")
    t2 = Teacher(first_name="Miguel", last_name="Suarez", email="miguel.suarez@example.com")
    t3 = Teacher(first_name="Laura", last_name="Martinez", email="laura.martinez@example.com")
    db.session.add_all([t1,t2,t3])
    db.session.commit()
    # Courses
    c1 = Course(code="MAT101", name="Mathematics I", credits=3, teacher_id=t1.id)
    c2 = Course(code="FIS101", name="Physics I", credits=4, teacher_id=t2.id)
    c3 = Course(code="ENG101", name="English I", credits=2, teacher_id=t3.id)
    c4 = Course(code="HIS101", name="History I", credits=2, teacher_id=t3.id)
    db.session.add_all([c1,c2,c3,c4])
    db.session.commit()
    # Students - generate ~100 records
    students = []
    for i in range(1,101):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
        s = Student(first_name=fn, last_name=ln, email=email, date_of_birth="2006-01-01")
        students.append(s)
    db.session.add_all(students)
    db.session.commit()
    # Enroll some students into courses randomly
    enrollments = []
    import random
    student_ids = [s.id for s in Student.query.all()]
    course_ids = [c.id for c in Course.query.all()]
    for sid in random.sample(student_ids, 60):  # enroll 60 random students in random courses
        cid = random.choice(course_ids)
        e = Enrollment(student_id=sid, course_id=cid, grade=random.choice(["A","B","C","D","F",""]))
        enrollments.append(e)
    db.session.add_all(enrollments)
    db.session.commit()
    print("Initialized database with sample data: school.db")
