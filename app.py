<<<<<<< HEAD
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

    conn = get_db()

    if search:
        students = conn.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + search + '%',)
        ).fetchall()
    else:
        students = conn.execute(
            "SELECT * FROM students"
        ).fetchall()

    conn.close()

    return render_template("record.html", students=students)
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
@app.route("/delete/<int:id>")
def delete_student(id): 
    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?", (id,)
    )


    conn.commit()
    conn.close()

    flash("Student Deleted Successfully!", "success")

    return redirect(url_for("records"))
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    init_db()
=======
from flask import Flask, render_template, request, redirect, url_for,redirect,flash

app = Flask(__name__)
app.secret_key = 'collegeportal'

students = [
    {
        "name": "Dipak Madane",
        "roll": 101,
        "attendance": "92%",
        "marks": 85
    },
    {
        "name": "Prisha Madane",
        "roll": 102,
        "attendance": "95%",
        "marks": 90
    },
    {
        "name": "Vedansh Madane",
        "roll": 103,
        "attendance": "88%",
        "marks": 78
    },
    {
        "name": "Devansh Madane",
        "roll": 104,
        "attendance": "97%",
        "marks": 94
    },
    {
        "name": "Aarav Madane",
        "roll": 105,
        "attendance": "90%",
        "marks": 82
    }
]
@app.route("/add", methods=["GET", "POST"])
def add_student():


    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        attendance = request.form["attendance"]
        marks = request.form["marks"]

        if not name or not roll or not attendance or not marks:
            flash("All fields are required!", "danger")
            return redirect(url_for("add_student"))

        students.append({
            "name": name,
            "roll": roll,
            "attendance": attendance,
            "marks": marks
        })

        flash("Student Added Successfully!", "success")

        return redirect(url_for("records"))

    return render_template("add_student.html")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("record.html", students=students)
@app.route("/about")
def about():    
    return render_template("about.html")

if __name__ == "__main__":
>>>>>>> 392ac851567b5a4f1fc1ec05baea01d7378eefd4
    app.run(debug=True)