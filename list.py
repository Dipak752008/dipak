#list-one variable with multiple values
student = ["dipak","kartik","rahul"]
print(student)
print(student[0])
print(student[1])
print(student[2])
mark = [100,90,80]
#loop through the list
for i in range(len(mark)):
    if mark[i] > 90:
        print(f"mark is {student[i]} {mark[i]} and grade is A")
    elif mark[i] > 80:
        print(f"mark is {student[i]} {mark[i]} and grade is B")
    else:
        print(f"mark is {student[2]} {mark[i]} and grade is C")


#create virtual environment
#python -m venv myenv
#source myenv/bin/activate  # On Windows: \Scripts\activatemyenv
#pip install flask  
