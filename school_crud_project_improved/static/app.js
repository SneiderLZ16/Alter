async function fetchJSON(url, opts){ const r = await fetch(url, opts); return r.json(); }

async function loadStudents(){
  const students = await fetchJSON("/api/students");
  const el = document.getElementById("studentsList");
  el.innerHTML = "<ul>" + students.slice(0,50).map(s=>`<li>${s.id} - ${s.first_name} ${s.last_name} (${s.email})</li>`).join("") + "</ul>";
}
async function loadCourses(){
  const courses = await fetchJSON("/api/courses");
  const el = document.getElementById("coursesList");
  el.innerHTML = "<ul>" + courses.map(c=>`<li>${c.id} - ${c.code}: ${c.name} (${c.credits} cr)</li>`).join("") + "</ul>";
}
async function loadEnrollments(){
  const e = await fetchJSON("/api/enrollments");
  const el = document.getElementById("enrollList");
  el.innerHTML = "<ul>" + e.map(x=>`<li>${x.id} - student ${x.student_id} in course ${x.course_id} (grade: ${x.grade || "-"})</li>`).join("") + "</ul>";
}

document.getElementById("studentForm").onsubmit = async (ev)=>{
  ev.preventDefault();
  const form = new FormData(ev.target);
  const body = Object.fromEntries(form.entries());
  await fetch("/api/students", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body)});
  ev.target.reset();
  loadStudents();
};

document.getElementById("courseForm").onsubmit = async (ev)=>{
  ev.preventDefault();
  const body = Object.fromEntries(new FormData(ev.target).entries());
  await fetch("/api/courses", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body)});
  ev.target.reset();
  loadCourses();
};

document.getElementById("enrollForm").onsubmit = async (ev)=>{
  ev.preventDefault();
  const body = Object.fromEntries(new FormData(ev.target).entries());
  const csv = "student_email,course_code\n" + body.student_email + "," + body.course_code + "\n";
  const blob = new Blob([csv], {type:"text/csv"});
  const fd = new FormData();
  fd.append("file", blob, "temp.csv");
  await fetch("/api/upload/enrollments", {method:"POST", body:fd});
  ev.target.reset();
  loadEnrollments();
};

// CSV upload handlers
document.getElementById("uploadStudentsBtn").onclick = ()=> document.getElementById("studentsCsv").click();
document.getElementById("studentsCsv").onchange = async (ev)=>{
  const f = ev.target.files[0];
  if(!f) return;
  const fd = new FormData(); fd.append("file", f);
  await fetch("/api/upload/students", {method:"POST", body:fd});
  loadStudents();
};

document.getElementById("uploadEnrollmentsBtn").onclick = ()=> document.getElementById("enrollmentsCsv").click();
document.getElementById("enrollmentsCsv").onchange = async (ev)=>{
  const f = ev.target.files[0];
  if(!f) return;
  const fd = new FormData(); fd.append("file", f);
  await fetch("/api/upload/enrollments", {method:"POST", body:fd});
  loadEnrollments();
};

loadStudents(); loadCourses(); loadEnrollments();
