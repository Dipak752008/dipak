#flask simple app
from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    print("College smart portal")
    return "<h1>College Smart Portal</h1><p>A simple portal for managing student records, marks and attendance.</p>" \
    "<p><a href='/records'>View Student Records</a></p><p><a href='/about'>About Project</a></p>" \
    "<p><a href='/contact'>Contact Us</a></p>" \
    "<p><a href='/services'>Our Services</a></p>" \
    "<p><a href='/team'>Our Team</a></p>"   
@app.route("/records")
def records():  
    students = [
        {"id": 101, "name": "Dipak", "course": "Computer Engineering", "percentage": 80},
        {"id": 102, "name": "vedansh", "course": "Computer Engineering", "percentage": 68},
        {"id": 103, "name": "prisha", "course": "Computer Engineering", "percentage": 88},
        {"id": 104, "name": "suzzane", "course": "Computer Engineering", "percentage": 58},
        {"id": 105, "name": "kushal", "course": "Computer Engineering", "percentage": 92}
    ]
    output = "<h1>Student Records</h1>"
    for student in students:
        output += f"<p>ID: {student['id']}<br>Name: {student['name']}<br>Course: {student['course']}<br>Percentage: {student['percentage']}%</p><hr>"
    return output
class team:
    def __init__(self, name, role):
        self.name = name
        self.role = role
@app.route("/about")
def about():
    Project = "College Smart Portal is developed using Python Flask."
    return f"<h1>About Project</h1><p>{Project}</p>" 
print("college smart portal is ")  
class Contact:
    def __init__(self, email, phone):
        self.email = email
        self.phone = phone
@app.route("/contact")
def contact():
    contact_info = Contact("dipakmadane@2008gmail.com", "123-456-7890")
    return f"<h1>Contact Us</h1><p>Email: {contact_info.email}</p><p>Phone: {contact_info.phone}</p>"

if __name__ == "__main__":
    app.run(debug=True)