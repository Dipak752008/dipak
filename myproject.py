# ==========================
# COLLEGE SMART PORTAL
# ==========================
# 1. Main  Dictionary

portal_info = {
    "portal_name": "College Smart Portal",
    "college_name": "GOVERMENT POLYTECHNIC HINGOLI ",
    "department": "Computer Engineering",
    "admin": "Dipak",
    "version": "1.0",
    "total_students": 5
}


# ==========================
# 2. List of Dictionaries
# ==========================

students = [
    {"id": 101, "name": "Dipak", "year": "SY", "attendance": 92},
    {"id": 102, "name": "Mahesh", "year": "SY", "attendance": 85},
    {"id": 103, "name": "Prisha", "year": "SY", "attendance": 78},
    {"id": 104, "name": "Vedansh", "year": "SY", "attendance": 65},
    {"id": 105, "name": "Ritesh", "year": "SY", "attendance": 88}
]


courses = {
    "C101": "Python Programming",
    "C102": "Database Management",
    "C103": "Web Development",
    "C104": "Computer Networks"
}

# 4. get_status() Function


def get_status(attendance):
    if attendance >= 75:
        return "Eligible"
    else:
        return "Short Attendance"

# 5. search_records() Function

def search_records(name):
    for student in students:
        if student["name"].lower() == name.lower():
            print("\nStudent Found")
            print(student)
            return

    print("\nStudent Not Found")


# 6. Print Portal Details


print("===== PORTAL INFORMATION =====")

for key, value in portal_info.items():
    print(key, ":", value)


# 7. Print Student Records


print("\n===== STUDENT RECORDS =====")

for student in students:
    print(
        "ID:", student["id"],
        "| Name:", student["name"],
        "| Year:", student["year"],
        "| Attendance:", student["attendance"],
        "| Status:", get_status(student["attendance"])
    )


# 8. Print Courses

print("\n===== COURSES =====")

for code, course in courses.items():
    print(code, "-", course)


# 9. Search Student

student_name = input("\nEnter Student Name: ")
search_records(student_name)

print("\nThank You for using the College Smart Portal")
