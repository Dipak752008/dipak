import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "collegeportal"


# Database Connection
def get_db():
    conn = sqlite3.connect("myproject.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create Table
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            attendance TEXT NOT NULL,
            marks INTEGER NOT NULL
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

    conn.close()

    return render_template("home.html", students=students)


# Records Page
@app.route("/records")
def records():
    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template("records.html", students=students)


# About Page
@app.route("/about")
def about():
    return render_template("about.html")


# Add Student
@app.route("/add", methods=["GET", "POST"])
def add_student():

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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)