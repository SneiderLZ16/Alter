# ER Diagram (ASCII) and Normalization (3NF)

Entities:
- Student (id, first_name, last_name, email, date_of_birth, created_at)
- Teacher (id, first_name, last_name, email)
- Course (id, code, name, credits, teacher_id)
- Enrollment (id, student_id, course_id, grade, enrolled_at)

ASCII ER Diagram:
```
[Student] 1 ---< [Enrollment] >--- 1 [Course] --- N [Teacher]
 student.id (PK)     enrollment.id (PK)    course.id (PK)   teacher.id (PK)
 first_name                          code (UNIQUE)     first_name
 last_name                           name              last_name
 email (UNIQUE)                      credits           email (UNIQUE)
```

Normalization justification:
- 1NF: All attributes are atomic.
- 2NF: Non-key attributes fully depend on PK. Enrollment has uniqueness on (student_id, course_id).
- 3NF: No transitive dependencies. Teacher details are stored in Teacher table, not duplicated in Course rows.
