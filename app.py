from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os
from groq import Groq
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "collegeportal"
client = Groq(
api_key=os.getenv("GROQ_API_KEY")
)


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
            marks INTEGER NOT NULL
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

    return render_template(
        "home.html",
        students=students,
        total=total
    )


# Records Page
@app.route("/record")
def records():

    search = request.args.get("search", "")
    attendance = request.args.get("attendance", "")

    conn = get_db()

    # Attendance dropdown ke liye unique values
    attendances = conn.execute("""
        SELECT DISTINCT attendance
        FROM students
        ORDER BY attendance
    """).fetchall()

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    # Search
    if search:
        query += " AND name LIKE ?"
        params.append("%" + search + "%")

    # Attendance Filter
    if attendance:
        query += " AND attendance = ?"
        params.append(attendance)

    students = conn.execute(query, params).fetchall()

    conn.close()

    return render_template(
        "record.html",
        students=students,
        attendances=attendances,
        selected_attendance=attendance
    )
# About Page
@app.route("/about")
def about():
    return render_template("about.html")

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

        # Agar users table khali hai to first user admin banega
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

        role = "admin" if total_users == 0 else "student"

        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

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

            flash("Login Successful!", "success")

            return redirect(url_for("home"))

        flash("Invalid Username or Password", "danger")

    return render_template("login.html")


# Add Student
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

        # Validation
        if not name or not roll or not attendance or not marks:
            flash("All fields are required!", "danger")
            return redirect(url_for("add_student"))

        conn = get_db()

        conn.execute(
            """
            INSERT INTO students
            (name, roll, attendance, marks)
            VALUES (?, ?, ?, ?)
            """,
            (name, roll, attendance, marks)
        )

        conn.commit()
        conn.close()

        flash("Student Added Successfully!", "success")

        return redirect(url_for("records"))

    return render_template("add_student.html")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if session.get("role")!="admin":
        flash("Access Denied!","danger")
        return redirect(url_for("home"))

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        attendance = request.form["attendance"]
        marks = request.form["marks"]

        conn.execute("""
            UPDATE students
            SET name=?, roll=?, attendance=?, marks=?
            WHERE id=?
        """, (name, roll, attendance, marks, id))

        conn.commit()
        conn.close()

        flash("Student Updated Successfully!", "success")
        return redirect(url_for("records"))

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)
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

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged Out Successfully!", "success")
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

init_db()
if __name__ == "__main__":
    
    app.run(debug=True)