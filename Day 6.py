from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)   
students = [
            {"roll_no": "102", "name": "Vedansh", "course": "Computer Engineering", "attendance": 88, "marks": {"Python": 78, "DBMS": 80, "Java": 75, "Web Tech": 85}},
            {"roll_no": "103", "name": "Prisha", "course": "   Computer Engineering", "attendance": 95, "marks": {"Python": 92, "DBMS": 90, "Java": 88, "Web Tech": 94}},
            {"roll_no": "104", "name": "Suzzane", "course": "Computer Engineering", "attendance": 85, "marks": {"Python": 80, "DBMS": 78, "Java": 70, "Web Tech": 82}},
]
@app.route("/")
def home():    return render_template("home.html")
                           
@app.route("/records")
def records(): 
    return render_template("record.html", students=students)

@app.route("/about")
def about():
    return render_template("about.html")
if __name__ == "__main__":
    app.run(debug=True)