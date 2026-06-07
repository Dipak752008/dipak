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
    app.run(debug=True)