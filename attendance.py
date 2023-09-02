from tkinter import*
from tkinter import ttk
#from tkcalendar import Calendar
import PIL.Image,PIL.ImageTk #Pillow Library
from tkinter import messagebox
from compProject_MySQL import *
import cv2
import os
import csv
from tkinter import filedialog

mydata=[] #list for csv files
class Attendance:
        def __init__(self,root):
                self.root=root #initialising root
                self.root.geometry("1530x790+0+0")
                self.root.title("Face Recognition")

                #Image 1
                img=PIL.Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/university.jpg")
                img=img.resize((800,200),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg=PIL.ImageTk.PhotoImage(img) #variable goes inside parameter

                f_lb1=Label(self.root,image=self.photoimg)
                f_lb1.place(x=0,y=0,width=800,height=200) #place requires axes

                #Image 2
                img1=PIL.Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/face.jpg")
                img1=img1.resize((800,200),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg1=PIL.ImageTk.PhotoImage(img1) #variable goes inside parameter

                f_lb1=Label(self.root,image=self.photoimg1)
                f_lb1.place(x=800,y=0,width=800,height=200) #place requires axes
#PUT BACKGROUND IMAGE LATER
                #background image
                img3=PIL.Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/pink.jpg")
                img3=img3.resize((1530,710),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg3=PIL.ImageTk.PhotoImage(img3) #variable goes inside parameter

                bg_img=Label(self.root,image=self.photoimg3)
                bg_img.place(x=0,y=130,width=1530,height=710) #place requires axes
                title_lbl=Label(bg_img,text="Attendance Management System",font=("Helvetica",25,"bold"),bg="white",fg="black") #bg is background, fg is foreground
                title_lbl.place(x=0,y=0,width=1530,height=45)

                main_frame=Frame(bg_img,bg="white",bd=2) #bd = border, bg_img is put in as frame is over it
                main_frame.place(x=0,y=50,width=1525,height=600)

                #Left Label Frame
                Left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Attendance Details",bg="white",font=("Helvetica",12,"bold")) #relief is border style   
                Left_frame.place(x=10,y=10,width=730,height=580)

                img_left=PIL.Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/princeton.jpg")
                img_left=img_left.resize((720,130),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg_left=PIL.ImageTk.PhotoImage(img_left) #variable goes inside parameter

                f_lb1=Label(Left_frame,image=self.photoimg_left)
                f_lb1.place(x=5,y=0,width=720,height=130) #place requires axes

                left_inside_frame=Frame(Left_frame,relief=RIDGE,bg="white",bd=2) 
                left_inside_frame.place(x=1,y=180,width=720,height=370)

                #LabelsEntry
                
                #StudentId
                StudentId_label=Label(left_inside_frame,text="StudentId:",font=("times new roman",13,"bold"),bg="white")
                StudentId_label.grid(row=0,column=0,padx=10,pady=10,sticky=W)

                self.atten_studentid=ttk.Entry(left_inside_frame,width=22) #,font=("times new roman",13,"bold")) #entry box for typing
                self.atten_studentid.grid(row=0,column=1,padx=10,pady=5,sticky=W)

                #Roll
                rollLabel=Label(left_inside_frame,text="Roll No:",font=("times new roman",13,"bold"),bg="white")
                rollLabel.grid(row=0,column=2,padx=4,pady=8,sticky=W)

                self.atten_roll=ttk.Entry(left_inside_frame,width=22, state = DISABLED)
                self.atten_roll.grid(row=0,column=3,pady=8)


                #Name
                nameLabel=Label(left_inside_frame,text="Name:",font=("times new roman",13,"bold"),bg="white")
                nameLabel.grid(row=1,column=0)

                self.atten_name=ttk.Entry(left_inside_frame,width=22)
                self.atten_name.grid(row=1,column=1,pady=8)

                #Department
                depLabel=Label(left_inside_frame,text="Department:",font=("times new roman",13,"bold"),bg="white")
                depLabel.grid(row=1,column=2)

                self.atten_dep=ttk.Entry(left_inside_frame,width=22, state = DISABLED)
                self.atten_dep.grid(row=1,column=3,pady=8)

                #Time
                timeLabel=Label(left_inside_frame,text="Time:",font=("times new roman",13,"bold"),bg="white")
                timeLabel.grid(row=2,column=0)

                self.atten_time=ttk.Entry(left_inside_frame,width=22)
                self.atten_time.grid(row=2,column=1,pady=8)

                #Date
                dateLabel=Label(left_inside_frame,text="Date:",font=("times new roman",13,"bold"),bg="white")
                dateLabel.grid(row=2,column=2)

                self.atten_date=ttk.Entry(left_inside_frame,width=22)
                self.atten_date.grid(row=2,column=3,pady=8)

                #Attendance
                attendanceLabel=Label(left_inside_frame,text="Attendance Status:",font=("times new roman",13,"bold"),bg="white")
                attendanceLabel.grid(row=3,column=0)

                self.atten_status=ttk.Combobox(left_inside_frame,width=20,state="readonly")
                self.atten_status["values"]=("Present","Absent")
                self.atten_status.grid(row=3,column=1,pady=8)
                self.atten_status.current(0)

                
                #Button frame
                btn_frame=Frame(left_inside_frame,bd=2,relief=RIDGE,bg="white")
                btn_frame.place(x=0,y=300,width=705, height=30)

                #Import button
                ''''
                save_btn=Button(btn_frame,text="Import csv",width=24,bg="blue", cursor="hand2") #,fg="white",)
                save_btn.grid(row=0,column=0)
                '''
                '''
                #Save
                update_btn=Button(btn_frame,text="Save",width=24,bg="blue", cursor="hand2") #,fg="white",)
                update_btn.grid(row=0,column=0)
                '''
                #Update
                update_btn=Button(btn_frame,text="Update",width=24,bg="blue", cursor="hand2", command = self.update) #,fg="white",)
                update_btn.grid(row=0,column=1, padx = 90)
                #update_btn.pack(side = LEFT, fill = BOTH, expand = True)

                #Reset
                reset_btn=Button(btn_frame,text="Reset",width=24,bg="blue", cursor="hand2", command = self.reset) #,fg="white",)
                reset_btn.grid(row=0,column=2)
                #reset_btn.pack(side = LEFT, fill = BOTH, expand = True)



                #Right Label Frame
                Right_frame=LabelFrame(main_frame,bg="white",bd=2,relief=RIDGE,text="Attendance Details",font=("Helvetica",12,"bold")) #relief is border style   
                Right_frame.place(x=780,y=10,width=735,height=580) 

                table_frame=Frame(Right_frame,bd=2,relief=RIDGE,bg="white")
                table_frame.place(x=5,y=5,width=720, height=455)

                #SCROLL BAR TABLE

                scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
                scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

                self.AttendanceReportTable=ttk.Treeview(table_frame,column=("id","roll","name","department","date","time","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

                scroll_x.pack(side=BOTTOM,fill=X)
                scroll_y.pack(side=RIGHT,fill=Y)

                scroll_x.config(command=self.AttendanceReportTable.xview)
                scroll_y.config(command=self.AttendanceReportTable.yview)
                #config to config the scroll to the table

                self.AttendanceReportTable.heading("id",text="Student Id")
                self.AttendanceReportTable.heading("roll",text="Roll No")
                self.AttendanceReportTable.heading("name",text="Name")
                self.AttendanceReportTable.heading("department",text="Department")
                self.AttendanceReportTable.heading("date",text="Date")
                self.AttendanceReportTable.heading("time",text="Time")
                #self.AttendanceReportTable.heading("attendance",text="Attendance Id")

                self.AttendanceReportTable["show"]="headings"

                self.AttendanceReportTable.column("id",width=100)
                self.AttendanceReportTable.column("roll",width=100)
                self.AttendanceReportTable.column("name",width=100)
                self.AttendanceReportTable.column("department",width=100)
                self.AttendanceReportTable.column("date",width=100)
                self.AttendanceReportTable.column("time",width=100)
                self.AttendanceReportTable.column("attendance",width=100)

                self.fetch_info()

                self.AttendanceReportTable.pack(fill=BOTH,expand=1) #fill on both axes and expand

                self.AttendanceReportTable.bind("<Double-1>", self.fill_entries)


        #=================================fetching the data============================================






        def fetch_info(self):
                info = []
                try:
                        with open(os.path.dirname(os.path.realpath(__file__))+"/Attendance_register_25_7_21.csv", "r", newline = "") as file:
                                reader_object = csv.reader(file)
                                if reader_object == []:
                                        messagebox.showerror("Error", "No attendance records found.")
                                else:
                                        next(reader_object)
                                        for i in reader_object:
                                                info.append(i)
                        
                        for i in info:
                                data = []
                                if i != ["\n"]:
                                        try:
                                                stream_rollno = completing_data(self, int(i[0]))
                                                #print(stream_rollno)
                                                data.append(i[0])
                                                data.append(stream_rollno[0][1])
                                                data.append(i[1])
                                                data.append(stream_rollno[0][0])
                                                data.append(i[2])
                                                data.append(i[3])
                                                data.append(i[4])
                                        except ValueError:
                                                messagebox.showerror("Error", "Student ID not found.")
                                else:
                                        data.append("")
                                self.AttendanceReportTable.insert("", "end", values = data)
                except FileNotFoundError:
                        messagebox.showerror("Error", "Attendance records not available.")

        def fill_entries(self, event):
                #print("!")
                self.atten_dep.config(state = NORMAL)
                self.atten_roll.config(state = NORMAL)
                self.atten_studentid.config(state = NORMAL)
                self.atten_name.config(state = NORMAL)

                self.atten_studentid.delete(0, 'end')
                self.atten_roll.delete(0, 'end')
                self.atten_name.delete(0, 'end')
                self.atten_dep.delete(0, 'end')
                self.atten_time.delete(0, 'end')
                self.atten_date.delete(0, 'end')
                self.atten_status.current(0)
                
                selected_data = self.AttendanceReportTable.focus()
                data = self.AttendanceReportTable.item(selected_data, 'values')
                if data != ("",):
                        self.atten_studentid.insert(0, data[0])
                        self.atten_roll.insert(0, data[1])
                        self.atten_name.insert(0, data[2])
                        self.atten_dep.insert(0, data[3])
                        self.atten_time.insert(0, data[5])
                        self.atten_date.insert(0, data[4])
                        if data[6] == "Present":
                                self.atten_status.current(0)
                        else:
                                self.atten_status.current(1)

                self.atten_dep.config(state = DISABLED)
                self.atten_roll.config(state = DISABLED)
                self.atten_studentid.config(state = DISABLED)
                self.atten_name.config(state = DISABLED)


        def reset(self):
                self.atten_dep.config(state = NORMAL)
                self.atten_roll.config(state = NORMAL)
                self.atten_studentid.config(state = NORMAL)
                self.atten_name.config(state = NORMAL)

                self.atten_studentid.delete(0, 'end')
                self.atten_roll.delete(0, 'end')
                self.atten_name.delete(0, 'end')
                self.atten_dep.delete(0, 'end')
                self.atten_time.delete(0, 'end')
                self.atten_date.delete(0, 'end')
                self.atten_status.current(0)

                self.atten_dep.config(state = DISABLED)
                self.atten_roll.config(state = DISABLED)
                self.atten_studentid.config(state = DISABLED)
                self.atten_name.config(state = DISABLED)


        def update(self):
                selected_data = self.AttendanceReportTable.focus()
                data = self.AttendanceReportTable.item(selected_data, 'values')
                updated_data = [["Student ID", "Name", "Date", "Time", "Present/Absent"]]
                with open(os.path.dirname(os.path.realpath(__file__))+"/Attendance_register_25_7_21.csv", "r", newline = "") as file:
                        reader_object = csv.reader(file)
                        for i in reader_object:
                                if i[0] == data[0] and i[1] == data[2] and i[2] == data[4] and i[3] == data[5] and i[4] == data[6]:
                                        if self.atten_status.get() == "Absent":
                                                updated_data.append([self.atten_studentid.get(), self.atten_name.get(), "", "", self.atten_status.get()])
                                        else:      
                                                updated_data.append([self.atten_studentid.get(), self.atten_name.get(), self.atten_date.get(), self.atten_time.get(), self.atten_status.get()])
                                elif i != ["Student ID", "Name", "Date", "Time", "Present/Absent"]:
                                        updated_data.append(i)
                
                with open(os.path.dirname(os.path.realpath(__file__))+"/Attendance_register_25_7_21.csv", "w", newline = "") as file:
                        writer_object = csv.writer(file)
                        writer_object.writerows(updated_data)
                
                self.atten_dep.config(state = NORMAL)
                self.atten_roll.config(state = NORMAL)
                self.atten_studentid.config(state = NORMAL)
                self.atten_name.config(state = NORMAL)

                self.atten_studentid.delete(0, 'end')
                self.atten_roll.delete(0, 'end')
                self.atten_name.delete(0, 'end')
                self.atten_dep.delete(0, 'end')
                self.atten_time.delete(0, 'end')
                self.atten_date.delete(0, 'end')
                self.atten_status.current(0)
                
                self.atten_dep.config(state = DISABLED)
                self.atten_roll.config(state = DISABLED)
                self.atten_studentid.config(state = DISABLED)
                self.atten_name.config(state = DISABLED)


if __name__== "__main__":
        root=Tk()
        obj=Attendance(root)
        root.mainloop()
