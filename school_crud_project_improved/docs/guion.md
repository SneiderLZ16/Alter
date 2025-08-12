# Guion de sustentación / Defense Script (EN & ES)

## English (key questions and concise answers)
Q: What entities exist and why?
A: Students, Teachers, Courses and Enrollments. Enrollments is an associative table to model the many-to-many relation between Students and Courses.

Q: What normalization level?
A: Up to 3NF. Fields are atomic, no partial dependencies and no transitive dependencies (teacher info is separated).

Q: How do CSV uploads work?
A: The system validates column names, types and referential integrity before inserting. Invalid rows are reported and skipped; transactions avoid partial commits on errors.

## Español (preguntas y respuestas clave)
P: ¿Qué entidades tiene y por qué?
R: Students, Teachers, Courses y Enrollments; la tabla Enrollments modela la relación N:M.

P: ¿Qué nivel de normalización aplicó?
R: Hasta 3FN; no hay dependencias transitivas y cada tabla tiene su propia responsabilidad.
