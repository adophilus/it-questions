from ...controllers.account import Account
from ...controllers.classroom import Classroom

def deleteClassrooms ():
	classrooms = Classroom.getAll()
	for classroom in classrooms:
		print(classroom.delete())

def addStudent (student_id, classroom_id):
	student = Account(id = student_id)

	classroom = Classroom(classroom_id = classroom_id)

	if (classroom and student):
		print(f"[+] Adding student to {classroom}")
		classroom.addMember(student)
	else:
		print("[-] Invalid student or classroom")