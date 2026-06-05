from flask import Flask, render_template

app = Flask(__name__)

students = [
    {"name": "Dipak", "course": "Computer Engineering", "percentage": 80},
    {"name": "Rahul", "course": "Computer Engineering", "percentage": 68},
    {"name": "Sneha", "course": "Computer Engineering", "percentage": 88},
    {"name": "Priya", "course": "Computer Engineering", "percentage": 58},
    {"name": "Amit", "course": "Computer Engineering", "percentage": 92}
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("records.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)