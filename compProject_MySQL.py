from tkinter import messagebox
import mysql.connector
import os
from tkinter import *


def taking_password():
	global pword
	global entry
	global PasswordWindow
	try:
		with open(os.path.dirname(os.path.realpath(__file__))+"/MySQL_password.txt", "r") as file:
			pword = file.read()
	except FileNotFoundError:
		PasswordWindow = Tk()
		PasswordWindow.geometry("200x150")
		PasswordWindow.title("MySQL Password")
		label = Label(PasswordWindow, text="Enter MySQL password:", font=("times new roman",13,"bold"))
		label.pack()
		entry = Entry(PasswordWindow, width=20, font=("times new roman",13,"bold"))
		entry.pack()
		button = Button(PasswordWindow, text="Enter", width=10, bg="blue", cursor="hand2", command=entering_password)
		button.pack()
		#PasswordWindow.quit
		PasswordWindow.mainloop()

	return pword

def entering_password():
	with open(os.path.dirname(os.path.realpath(__file__))+"/MySQL_password.txt", "w") as file:
		file.write(entry.get())
		file.flush()
		#PasswordWindow.quit()
		taking_password()

def inserting_data(self):
	pword = taking_password()
	while True:
		try:
			print("32", pword)
			mydb = mysql.connector.connect(host = "localhost", username = "root", password = pword)	#we'll have to adjust this according to the MySQL password for the system.
			break
		except:
			messagebox.showerror("Incorrect Password", "Incorrect MySQL password. Try again.")
			os.remove(os.path.dirname(os.path.realpath(__file__))+"/MySQL_password.txt")
			taking_password()
	my_cursor = mydb.cursor()
	#creating the database if it doesn't already exist:
	my_cursor.execute("create database if not exists Attendance_System")
	mydb.commit()
	#creating the table then inserting values:
	my_cursor.execute("use Attendance_System")
	my_cursor.execute("""create table if not exists student_info(Stream char(15),
												Grade int,
												Section char(1),
												Year char(15),
												Student_id int unique,
												Name char(15),
												Roll_No int,
												Gender char(10),
												Email char(50),
												Phone char(15),
												DOB char(15),
												Photo_Sample char(3))""")
	mydb.commit()

	my_cursor.execute("insert into student_info values ('{}', {}, '{}', '{}', {}, '{}', {}, '{}', '{}', '{}', '{}')".format(
																self.dep_combo.get(),
																int(self.grade_combo.get()),
																self.sec_combo.get(),
																self.year_combo.get(),
																#self.d, self.g, self.s, self.y,
																int(self.studentId_entry.get()),
																self.studentName_entry.get(),
																int(self.roll_no_entry.get()),
																self.gender_entry.get(),
																self.email_entry.get(),
																#self.phone_entry.get(),
																self.date_entry.get(),
																self.photo_sample.get()	#if a photo sample was given.
																))
	mydb.commit()

	my_cursor.close()
	mydb.close()
	
def fetching_data(self): 	#i've put the data in the list, "info" but it still has to go into the table using tkinter.
	pword = taking_password()
	mydb = mysql.connector.connect(host = "localhost", username = "root", password = pword, database = "Attendance_System")
	my_cursor = mydb.cursor()
	my_cursor.execute("select * from student_info")
	info = my_cursor.fetchall()
	my_cursor.close()
	mydb.close()

	return info

def deleting_data(self):
	pword = taking_password()
	mydb = mysql.connector.connect(host = "localhost", username = "root", password = pword, database = "Attendance_System")
	my_cursor = mydb.cursor()
	my_cursor.execute("delete from student_info where Student_id = {}".format(self.var_roll.get(),))
	my_cursor.commit()
	my_cursor.close()
	mydb.close()

def searching_data(self, search_field, search_val):
	pword = taking_password()
	mydb = mysql.connector.connect(host = "localhost", username = "root", password = pword, database = "Attendance_System")
	my_cursor = mydb.cursor()
	if search_field == "Name":
		my_cursor.execute("select * from student_info where Name like '%{}%'".format(search_val))
	elif search_field == "Roll No":
		my_cursor.execute("select * from student_info where Roll_No like {}".format(search_val))
	info = my_cursor.fetchall()
	my_cursor.close()
	mydb.close()

	return info

def completing_data(self, search_val):
	pword = taking_password()
	mydb = mysql.connector.connect(host = "localhost", username = "root", password = pword, database = "Attendance_System")
	my_cursor = mydb.cursor()
	my_cursor.execute("select Stream, Roll_No from student_info where Student_id = {}".format(search_val))
	info = my_cursor.fetchall()
	my_cursor.close()
	mydb.close()

	return info