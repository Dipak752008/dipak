def marks_report():
    marks = [80, 75, 70, 85, 90]

    total = 0
    for mark in marks:
        total += mark

    percentage = total / len(marks)

    print("\nMarks:", marks)
    print("Total:", total)
    print("Percentage:", percentage)

    if percentage >= 75:
        print("Result: Distinction")
    elif percentage >= 60:
        print("Result: First Class")
    elif percentage >= 45:
        print("Result: Pass")
    else:
        print("Result: Fail")


def attendance_report():
    attendance = ["Present", "Present", "Absent", "Present", "Present"]

    present = 0
    for status in attendance:
        if status == "Present":
            present += 1

    print("\nPresent Days:", present)


def show_notices():
    notices = ["Exam on Monday", "Holiday on Friday"]

    print("\n--- NOTICE BOARD ---")
    for notice in notices:
        print("-", notice)


print("===== COLLEGE SMART PORTAL =====")

name = input("Enter Student Name: ")

print("\nWelcome", name)

marks_report()
attendance_report()
show_notices()

print("\nThank You")