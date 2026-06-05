from flask import Flask, render_template, request

app = Flask(__name__)

# Student Database (Realistic Data)
students = [
    {
        "roll_no": "CS101",
        "name": "Dipak Madane",
        "course": "Computer Engineering",
        "attendance": 92,
        "marks": {
            "Python": 88,
            "DBMS": 85,
            "Java": 82,
            "Web Tech": 90
        }
    }
]

# Notices
notices = [
    "NBA Accreditation Visit on 15 September",
    "Internship Report Submission Last Date: 30 June",
    "Semester Exam Form Started"
]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    roll_no = request.form['roll_no']

    for student in students:
        if student["roll_no"] == roll_no:
            return render_template(
                'dashboard.html',
                student=student,
                notices=notices
            )

    return "Student Not Found"

if __name__ == '_main_':
    app.run(debug=True)
<!DOCTYPE html>
<html>
<head>
    <title>College Smart Portal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>

<div class="login-box">
    <h1>🎓 College Smart Portal</h1>

    <form action="/dashboard" method="POST">
        <input type="text" name="roll_no"
               placeholder="Enter Roll Number" required>

        <button type="submit">Login</button>
    </form>

    <p>Demo Roll No: CS101</p>
</div>

</body>
</html>