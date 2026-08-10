from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
import math
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
app.secret_key = "collegeportal"
client = Groq(
api_key=os.getenv("GROQ_API_KEY")
)
def ask_ai(doubt):

    prompt = f"""
You are an AI study assistant for a college student.

Student's Doubt:
{doubt}

Explain the answer in simple and easy language.
Give a clear explanation with examples if required.
Keep the answer educational and concise.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
# Database Connection
def get_db():
    conn = sqlite3.connect("myproject.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create Table 
def init_db():
    conn = get_db()

    # Students Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT UNIQUE NOT NULL,
            attendance INTEGER NOT NULL,
            marks INTEGER NOT NULL,
            branch TEXT NOT NULL,
            photo TEXT
            
        
        )
    """)

    # Users Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Home Page
@app.route("/")
def home():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    conn.close()

    return render_template( "home1.html", students=students, total=total)


# Records Page
@app.route("/record")
def records():

    search = request.args.get("search", "")
    attendance = request.args.get("attendance", "")

    # Current page
    page = request.args.get("page", 1, type=int)

    # Ek page par kitne students
    per_page = 5

    conn = get_db()

    # Attendance dropdown
    attendances = conn.execute("""
        SELECT DISTINCT attendance
        FROM students
        ORDER BY attendance
    """).fetchall()

    # Base query
    query = "SELECT * FROM students WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM students WHERE 1=1"

    params = []
    count_params = []

    # Search filter
    if search:
        query += " AND name LIKE ?"
        count_query += " AND name LIKE ?"

        params.append("%" + search + "%")
        count_params.append("%" + search + "%")

    # Attendance filter
    if attendance:
        query += " AND attendance = ?"
        count_query += " AND attendance = ?"

        params.append(attendance)
        count_params.append(attendance)

    # Total students
    total_students = conn.execute(
        count_query,
        count_params
    ).fetchone()[0]

    # Total pages
    total_pages = (total_students + per_page - 1) // per_page

    # Page ko valid rakho
    if page < 1:
        page = 1

    if total_pages > 0 and page > total_pages:
        page = total_pages

    # Pagination offset
    offset = (page - 1) * per_page

    # Students for current page
    query += " ORDER BY id DESC LIMIT ? OFFSET ?"

    params.extend([per_page, offset])

    students = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return render_template(
        "record1.html",
        students=students,
        attendances=attendances,
        selected_attendance=attendance,
        search=search,
        page=page,
        total_pages=total_pages,
        total_students=total_students
    )
# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        existing = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        if existing:
            flash("Username already exists!", "danger")
            conn.close()
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)

        # Agar users ka naam dipak hoga to wo admin rahega
       
        role = "admin" if username == "Dipak" else "student"

        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Notice page 
@app.route("/notice")
def notice():
    notices = [
        {
            "title": "Semester Exam",
            "date": "15 July 2026",
            "message": "Semester examination will start from 15 July."
        },
        {
            "title": "Holiday",
            "date": "20 July 2026",
            "message": "College will remain closed on Guru Purnima."
        },
        {
            "title": "Project Submission",
            "date": "25 July 2026",
            "message": "Submit your final project before 25 July."
        },
        {
            "title": "Sports Day",
            "date": "30 July 2026",
            "message": "Annual sports day will be held on 30 July."
        },
        {
            "title": "Traditional Day",
            "date": "5 August 2026",
            "message": "Annual traditional day will be celebrated on 5 August."
        }
    ]
    return render_template("notice.html", notices=notices)

#Ai study tips page
@app.route("/ai_tips", methods=["GET", "POST"])
def ai_tips():

    if request.method == "POST":

        name = request.form["name"]
        marks = request.form["marks"]
        subject = request.form["subject"]

        prompt = f"""
Student Name: {name}
Subject: {subject}
Marks: {marks}/100

Give exactly 5 practical study tips in numbered points.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        tip = response.choices[0].message.content

        return render_template(
            "ai_result.html",
            name=name,
            subject=subject,
            marks=marks,
            tip=tip
        )

    return render_template("ai_tips.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["username"] = user["username"]
            session["role"]=user["role"]

            flash("Login Successful!🎉", "success")

            return redirect(url_for("home"))

        flash("Invalid Username or Password", "danger")

    return render_template("login.html")


# Add Student page
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if session.get("role") !="admin":
        flash("!Access Denied!","Danger")
        return redirect(url_for("home"))

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        attendance = request.form["attendance"]
        marks = request.form["marks"]
        photo = request.files["photo"]
        branch = request.form["branch"]
        filename =""
        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # Validation
        if not name or not roll or not attendance or not marks:
            flash("All fields are required!", "danger")
            return redirect(url_for("add_student"))

        conn = get_db()

        conn.execute(
            """
            INSERT INTO students
            (name, roll, attendance, marks,branch,photo)
            VALUES (?, ?, ?,?,?, ?)
            """,
            (name, roll, attendance, marks, branch, filename)
        )

        conn.commit()
        conn.close()

        flash("Student Added Successfully!", "success")

        return redirect(url_for("records"))

    return render_template("add_student.html")

#Edit student page
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if session.get("role") != "admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("home"))

    conn = get_db()

    # Pehle student fetch karo
    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        attendance = request.form["attendance"]
        marks = request.form["marks"]
        branch = request.form["branch"]

        photo = request.files["photo"]

        filename = student["photo"]

        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn.execute("""
            UPDATE students
            SET name=?, roll=?, attendance=?, marks=?, branch=?, photo=?
            WHERE id=?
        """, (name, roll, attendance, marks, branch, filename, id))

        conn.commit()
        conn.close()

        flash("Student Updated Successfully!", "success")
        return redirect(url_for("records"))

    conn.close()

    return render_template("edit_student.html", student=student)

# Delete student record page
@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id): 
    if session.get("role")!="admin":
        flash("Access Denied!","danger")
        return redirect(url_for("home"))

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?", (id,)
    )


    conn.commit()
    conn.close()

    flash("Student Deleted Successfully!", "success")

    return redirect(url_for("records"))

# View student recoeds page
@app.route("/student/<int:id>")
def student_detail(id):

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        flash("Student Not Found!", "danger")
        return redirect(url_for("records"))

    return render_template("student_detail.html", student=student)

# Branches page
@app.route("/branches")
def branches():

    conn = get_db()

    computer = conn.execute(
        "SELECT COUNT(*) FROM students WHERE branch='Computer Engineering'"
    ).fetchone()[0]

    mechanical = conn.execute(
        "SELECT COUNT(*) FROM students WHERE branch='Mechanical Engineering'"
    ).fetchone()[0]

    civil = conn.execute(
        "SELECT COUNT(*) FROM students WHERE branch='Civil Engineering'"
    ).fetchone()[0]

    electrical = conn.execute(
        "SELECT COUNT(*) FROM students WHERE branch='Electrical Engineering'"
    ).fetchone()[0]

    entc = conn.execute(
        "SELECT COUNT(*) FROM students WHERE branch='Electronics & Telecommunication'"
    ).fetchone()[0]

    ai = conn.execute(
        "SELECT COUNT(*) FROM students WHERE branch='Artificial Intelligence & Data Science'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "branches.html",
        computer=computer,
        mechanical=mechanical,
        civil=civil,
        electrical=electrical,
        entc=entc,
        ai=ai
    )
@app.route("/ai_doubt", methods=["GET", "POST"])
def ai_doubt():

    answer = None

    if request.method == "POST":

        doubt = request.form.get("doubt")

        if doubt:
            answer = ask_ai(doubt)

    return render_template(
        "ai_doubt.html",
        answer=answer
    )

# Log out page
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged Out Successfully!", "success")
    return redirect(url_for("home"))

# Error handeled page
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

init_db()
if __name__ == "__main__":
    
    app.run(debug=True)