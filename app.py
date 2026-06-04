from appmy import Flask

app = Flask(__name__)

# List of Dictionaries (Student Records)
students = [
    {"id": 101, "name": "Dipak", "course": "Computer Engineering", "percentage": 80},
    {"id": 102, "name": "vedansh", "course": "Computer Engineering", "percentage": 68},
    {"id": 103, "name": "prisha", "course": "Computer Engineering", "percentage": 88},
    {"id": 104, "name": "suzzane", "course": "Computer Engineering", "percentage": 58},
    {"id": 105, "name": "kushal", "course": "Computer Engineering", "percentage": 92}
]

# Route 1 - Homepage
@app.route("/")
def home():
    return """
    <h1>College Smart Portal</h1>
    <p>A simple portal for managing student records, marks and attendance.</p>
    """

# Route 2 - Records Page
@app.route("/records")
def records():
    output = "<h1>Student Records</h1>"
    for student in students:
        output += f"""
        <p>
        ID: {student['id']}<br>
        Name: {student['name']}<br>
        Course: {student['course']}<br>
        Percentage: {student['percentage']}%
        </p>
        <hr>
        """
    return output

# Route 3 - Extra Route
@app.route("/about")
def about():
    return """
    <h1>About Project</h1>
    <p>College Smart Portal is developed using Python Flask.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)