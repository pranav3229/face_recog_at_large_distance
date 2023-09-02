from tkinter import*
from tkinter import ttk
from tkinter import messagebox
#from tkcalendar import Calendar
#from PIL import Image,PIL.ImageTk #Pillow Library
import PIL.Image, PIL.ImageTk
from compProject_FaceRecognition_06012022 import *
from compProject_MySQL import *
from faces import *
import sys


class Student:

        def __init__(self,root):
                
                self.root=root #initialising root
                self.root.geometry("1530x790+0+0")
                self.root.title("Face Recognition")
                #self.var = 1
                #Image 1
                img=PIL.Image.open(r"/Users/Glovantech/Documents/Python_DeepanR/img/university.jpg")
                img=img.resize((500,130),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg=PIL.ImageTk.PhotoImage(img) #variable goes inside parameter
                ''
                f_lb1=Label(self.root,image=self.photoimg)
                f_lb1.place(x=0,y=0,width=500,height=130) #place requires axes

                #Image 2
                img1=PIL.Image.open(r"/Users/Glovantech/Documents/Python_DeepanR/img/face.jpg")
                img1=img1.resize((500,130),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg1=PIL.ImageTk.PhotoImage(img1) #variable goes inside parameter

                f_lb1=Label(self.root,image=self.photoimg1)
                f_lb1.place(x=500,y=0,width=550,height=130) #place requires axes

                #Image 3
                img2=PIL.Image.open(r"/Users/Glovantech/Documents/Python_DeepanR/img/princeton.jpg")
                img2=img2.resize((500,130),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg2=PIL.ImageTk.PhotoImage(img2) #variable goes inside parameter

                f_lb1=Label(self.root,image=self.photoimg2)
                f_lb1.place(x=1000,y=0,width=550,height=130) #place requires axes

                #background image
                img3=PIL.Image.open(r"/Users/Glovantech/Documents/Python_DeepanR/img/pink.jpg")
                img3=img3.resize((1530,710),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg3=PIL.ImageTk.PhotoImage(img3) #variable goes inside parameter

                bg_img=Label(self.root,image=self.photoimg3)
                bg_img.place(x=0,y=130,width=1530,height=710) #place requires axes
                
                #title_lbl=Label(bg_img,text="Student Management System",font=("Helvetica",25,"bold"),bg="white",fg="black") #bg is background, fg is foreground
                title_lbl=Label(text="Student Management System",font=("Helvetica",25,"bold"),bg="white",fg="black") #bg is background, fg is foreground
                title_lbl.place(x=0,y=0,width=1530,height=45)
                
                main_frame=Frame(bg_img,bd=2) #bd = border, bg_img is put in as frame is over it
                main_frame.place(x=20,y=50,width=1480,height=600)

                #Left Label Frame
                Left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Details",font=("Helvetica",12,"bold")) #relief is border style   
                Left_frame.place(x=10,y=10,width=730,height=580)
                
                img_left=PIL.Image.open(r"/Users/Glovantech/Documents/Python_DeepanR/img/princeton.jpg")
                img_left=img_left.resize((720,130),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg_left=PIL.ImageTk.PhotoImage(img_left) #variable goes inside parameter'''
                               
                f_lb1=Label(Left_frame,image=self.photoimg2)
                f_lb1.place(x=5,y=0,width=720,height=130) #place requires axes'''

                #Current Course Information
                current_course_frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Current Course Information",font=("times new roman",12,"bold")) #relief is border style
                current_course_frame.place(x=5,y=135,width=720,height=120)

                #Stream/Department
                dep_label=Label(current_course_frame,text="Stream",font=("times new roman",12,"bold"),bg="white") #department label is dep
                dep_label.grid(row=0,column=0,padx=10) #row and column start from 0
                self.dep_combo=ttk.Combobox(current_course_frame,font=("times new roman",12,"bold"),state="read only") #fancy combo box from ttk, requires frame inside parameter; state read only makes it read only
                self.dep_combo.config(state="readonly") #allows it to be read only
                self.dep_combo['values']=("Select Stream","Science","Commerce","Arts/Humanities")
                self.dep_combo.current(0) #gives current position of first value in the above tuple, iterates through
                self.dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

                #Grade
                grade_label=Label(current_course_frame,text="Grade",font=("times new roman",13,"bold"),bg="white")
                grade_label.grid(row=0,column=2,padx=10)
                self.grade_combo=ttk.Combobox(current_course_frame,font=("times new roman",12,"bold"))
                self.grade_combo.config(state="readonly")
                self.grade_combo['values']=("Select Grade","11","12")
                self.grade_combo.current(0)
                self.grade_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)

                #Section
                sec_label=Label(current_course_frame,text="Section",font=("times new roman",13,"bold"),bg="white")
                sec_label.grid(row=1,column=2,padx=10)
                self.sec_combo=ttk.Combobox(current_course_frame,font=("times new roman",12,"bold"),state="read only")
                self.sec_combo.config(state="readonly")
                self.sec_combo['values']=("Select Section","A","B","C","D")
                self.sec_combo.current(0)
                self.sec_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)

                #Year
                year_label=Label(current_course_frame,text="Year",font=("times new roman",13,"bold"),bg="white")
                year_label.grid(row=1,column=0,padx=10)
                self.year_combo=ttk.Combobox(current_course_frame,font=("times new roman",12,"bold"),state="read only")
                self.year_combo.config(state="readonly")
                self.year_combo['values']=("Select Year","2019-2020","2020-2021","2021-2022","2022-2023")
                self.year_combo.current(0)
                self.year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)


                

                #Class Student Information
                class_Student_frame=LabelFrame(Left_frame,bd=2,bg="white",relief=RIDGE,text="Class Student Information",font=("times new roman",12,"bold")) #relief is border style   
                class_Student_frame.place(x=5,y=260,width=720,height=295)

                #StudentId
                studentId_label=Label(class_Student_frame,text="StudentId",font=("times new roman",13,"bold"),bg="white")
                studentId_label.grid(row=0,column=0,padx=10,pady=10,sticky=W)
                studentId_var = IntVar()
                self.studentId_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",13,"bold")) #entry box for typing
                self.studentId_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)

                #Student Name
                studentName_label=Label(class_Student_frame,text="Student Name",font=("times new roman",13,"bold"),bg="white")
                studentName_label.grid(row=0,column=2,padx=10,pady=10,sticky=W)
                studentName_var = StringVar()
                self.studentName_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",13,"bold")) #entry box for typing
                self.studentName_entry.grid(row=0,column=3,pady=5,sticky=W)

                #Roll No
                roll_no_label=Label(class_Student_frame,text="Roll No.",font=("times new roman",13,"bold"),bg="white")
                roll_no_label.grid(row=1,column=2,padx=10,pady=20,sticky=W)
                roll_no_var = IntVar()
                self.roll_no_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",13,"bold")) #entry box for typing
                self.roll_no_entry.grid(row=1,column=3,sticky=W)

                #Gender
                gender_label=Label(class_Student_frame,text="Gender",font=("times new roman",13,"bold"),bg="white")
                gender_label.grid(row=1,column=0,padx=10,pady=5,sticky=W)
                gender_entry_var = StringVar()
                self.gender_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",13,"bold")) #entry box for typing
                self.gender_entry.grid(row=1,column=1,padx=10,sticky=W)

                #Email
                email_label=Label(class_Student_frame,text="Email",font=("times new roman",13,"bold"),bg="white")
                email_label.grid(row=3,column=0,padx=10,pady=10,sticky=W)
                email_entry_var = StringVar()
                self.email_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",13,"bold")) #entry box for typing
                self.email_entry.grid(row=3,column=1,padx=10,sticky=W)

                #phone 
                phone_label=Label(class_Student_frame,text="Phone No.",font=("times new roman",13,"bold"),bg="white")
                phone_label.grid(row=3,column=2,padx=10,pady=10,sticky=W)
                phone_entry_var = IntVar()
                self.phone_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",13,"bold")) #entry box for typing
                self.phone_entry.grid(row=3,column=3,sticky=W)

                #DOB
                
                '''
                cal=Calendar(root,selectmode='day',day=1,year=2021,month=1,)
                cal.pack(pady=20)
                
                def grad_date():
                        date.config(text="Date:"+cal.get_date())
                Button(root,text="Get date",command=grad_date).pack(pady=20)
                date=Label(date_label)
                date.pack(pady=20)
                '''
                date_label=Label(class_Student_frame,text="Date Of Birth",font=("times new roman",13,"bold"),bg="white")
                date_label.grid(row=3,column=2,padx=10,pady=10,sticky=W)
                date_entry_var = StringVar()
                self.date_entry=ttk.Entry(class_Student_frame,width=20,font=("times new roman",13,"bold")) #entry box for typing
                self.date_entry.grid(row=3,column=3,sticky=W)

                #Radio Buttons
                self.photo_sample = StringVar()
                radiobtn1=ttk.Radiobutton(class_Student_frame,text="Take Photo Sample",value="Yes", variable = self.photo_sample)
                radiobtn1.grid(row=4,column=0,padx=10)

                radiobtn2=ttk.Radiobutton(class_Student_frame,text="No Photo Sample",value="No", variable = self.photo_sample)
                radiobtn2.grid(row=4,column=1,padx=10)

                #Radio button frame
                btn_frame=Frame(class_Student_frame,bd=2,relief=RIDGE,bg="white")
                btn_frame.place(x=5.5,y=195,width=705, height=30)

                #Save button
                save_btn=Button(btn_frame,text="Save",width=24,bg="blue",cursor="hand2", command = self.save_fn)
                save_btn.grid(row=0,column=0)
                '''
                #Update
                update_btn=Button(btn_frame,text="Update",width=24,bg="blue",cursor="hand2")
                update_btn.grid(row=0,column=1)
                
                #Delete
                delete_btn=Button(btn_frame,text="Delete",width=24,bg="blue",cursor="hand2")
                delete_btn.grid(row=0,column=2)
                '''
                #Reset
                reset_btn=Button(btn_frame,text="Reset",width=24,bg="blue",cursor="hand2", command = self.reset)
                reset_btn.grid(row=0,column=2)

                #Second frame to hold take photo sample and update photo sample buttons
                btn_frame1=Frame(class_Student_frame,bd=2,relief=RIDGE,bg="white")
                btn_frame1.place(x=5.5,y=223,width=705, height=30)

                #Take photo sample
                take_photo_btn=Button(btn_frame1,text="Take Photo Sample",width=49,bg="blue",cursor="hand2", command = self.take_photo_samples_fn)#collect_samples(studentName_entry.get()))
                take_photo_btn.grid(row=1,column=0)
                '''
                #Update photo sample
                update_photo_btn=Button(btn_frame1,text="Update Photo ",width=49,bg="blue",cursor="hand2", command = take_photo_samples_fn)
                update_photo_btn.grid(row=1,column=1)
                '''
                #Right Label Frame
                Right_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Details",font=("Helvetica",12,"bold")) #relief is border style   
                Right_frame.place(x=780,y=10,width=660,height=580)
                
                img_right=PIL.Image.open(r"/Users/Glovantech/Documents/Python_DeepanR/img/princeton.jpg")
                img_right=img_right.resize((720,130),PIL.Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg_right=PIL.ImageTk.PhotoImage(img_right) #variable goes inside parameter
                
                f_lb1=Label(Right_frame,image=self.photoimg2)
                f_lb1.place(x=5,y=0,width=720,height=130) #place requires axes


                #Search System
                Search_frame=LabelFrame(Right_frame,bd=2,relief=RIDGE,text="Search System",font=("times new roman",12,"bold")) #relief is border style   
                Search_frame.place(x=5,y=135,width=640,height=80)

                search_label=Label(Search_frame,text="Search By",font=("times new roman",15,"bold"),bg="red")
                search_label.grid(row=0,column=0,padx=10,pady=10,sticky=W)

                search_combo=ttk.Combobox(Search_frame,font=("times new roman",12,"bold"))
                search_combo.config(state="readonly")
                search_combo['values']=("Select","Roll No","Name")
                search_combo.current(0)
                search_combo.grid(row=0,column=1,padx=5,pady=10,sticky=W)

                search_var = StringVar()
                search_entry=ttk.Entry(Search_frame,width=14,font=("times new roman",13,"bold"))#, textvariable = search_var) #entry box for typing
                search_entry.grid(row=0,column=2,sticky=W)
                
                search_btn=Button(Search_frame,text="Search",width=12,bg="blue",cursor="hand2", command = lambda: [self.showAll_btn.config(state = NORMAL), self.searching_info(search_combo.get(), search_entry.get())])
                search_btn.grid(row=0,column=3,padx=5)

                self.showAll_btn=Button(Search_frame,text="Show All",width=12,bg="blue",cursor="hand2", command = self.fetching_info)#lambda: [self.fetching_info(), showAll_btn.config(state = DISABLED)])
                
                self.showAll_btn.grid(row=0,column=4)
                
                #Table Frame
                table_frame=LabelFrame(Right_frame,bd=2,relief=RIDGE,text="Student Details",font=("times new roman",12,"bold")) #relief is border style   
                table_frame.place(x=7.5,y=220,width=640,height=330)

                scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL) #scrollbar horizontal component
                scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL) #scrollbar vertical component

                self.student_table=ttk.Treeview(table_frame,column=("Stream","Grade","Section","Year","ID","Name","RollNo","Gender","Email","DOB","Photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set) #Treeview to display hierarchy of items with attributes
                #xscrollcommand and yscrollcommand are 2 variables for the scroll components given values scroll_x and scroll_y which are set using .set

                scroll_x.pack(side=BOTTOM,fill=X) #fill x fills x axis (capitalised)
                scroll_y.pack(side=RIGHT,fill=Y)  #fill y fills y axis (capitalised)
                scroll_x.config(command=self.student_table.xview)
                scroll_y.config(command=self.student_table.yview)
#before adding headers, we have to config the scrolls to the table and view it through diff views

                self.student_table.heading("Stream",text="Stream")
                self.student_table.heading("Grade",text="Grade")
                self.student_table.heading("Section",text="Section")
                self.student_table.heading("Year",text="Year")
                self.student_table.heading("ID",text="StudentId")
                self.student_table.heading("Name",text="Name")
                self.student_table.heading("RollNo",text="Roll No.")
                self.student_table.heading("Gender",text="Gender")
                self.student_table.heading("Email",text="Email")
                #self.student_table.heading("Phone",text="Phone")
                self.student_table.heading("DOB",text="DOB")
                self.student_table.heading("Photo",text="PhotoStatus")
                self.student_table['show']="headings" #shows headings

                self.student_table.column("Stream",width=100) #access one heading at a time with respective heading as a parameter
                self.student_table.column("Grade",width=100)
                self.student_table.column("Section",width=100)
                self.student_table.column("Year",width=100)
                self.student_table.column("ID",width=100)
                self.student_table.column("Name",width=100)
                self.student_table.column("RollNo",width=100)
                self.student_table.column("Gender",width=100)
                self.student_table.column("Email",width=150)
                #self.student_table.column("Phone",width=100)
                self.student_table.column("DOB",width=100)
                self.student_table.column("Photo",width=150)
                '''
                data = fetching_data(self)
                for i in data:
                    self.student_table.insert("", "end", values = i)
                '''
                self.student_table.pack(fill=BOTH,expand=1)
#expand allows to it to fill any space not inside the widget
#fill only fills extra space allocated into the widget

        def save_fn(self):
                #try:
                self.d, self.g, self.s, self.y = self.dep_combo.get(), self.grade_combo.get(), self.sec_combo.get(), self.year_combo.get()
                inserting_data(self)
                
                self.studentId_entry.delete(0, 'end')
                self.studentName_entry.delete(0, 'end')
                self.roll_no_entry.delete(0, 'end')
                self.gender_entry.delete(0, 'end')
                self.email_entry.delete(0, 'end')
                #self.phone_entry.delete(0, 'end')
                self.date_entry.delete(0, 'end')
                self.dep_combo.current(0)
                self.year_combo.current(0)
                self.sec_combo.current(0)
                self.grade_combo.current(0)
                self.photo_sample.set(None)
                
                messagebox.showinfo("Success", "Student info saved!")
                '''except Exception as es:
                        if "student_info.student_id" in str(es) and "1062 (23000): Duplicate entry" in str(es):
                                messagebox.showerror("Duplicate Entry", "Duplicate entry for Student ID. Try again.")
                        else:
                                messagebox.showerror("Invalid Entry", "Invalid entry. Try again.")
                        print(es, "\n", sys.exc_info()[2].tb_lineno)'''

        def take_photo_samples_fn(self):
                #global sample_face_encodings
                #global sample_face_names
                studentName_var = self.studentName_entry.get()
                studentID_var = self.studentId_entry.get()
                if studentName_var != "":
                        collect_samples(studentName_var, studentID_var)

        def reset(self):
                self.studentId_entry.delete(0, 'end')
                self.studentName_entry.delete(0, 'end')
                self.roll_no_entry.delete(0, 'end')
                self.gender_entry.delete(0, 'end')
                self.email_entry.delete(0, 'end')
                self.phone_entry.delete(0, 'end')
                self.date_entry.delete(0, 'end')
                self.dep_combo.current(0)
                self.year_combo.current(0)
                self.sec_combo.current(0)
                self.grade_combo.current(0)
                self.photo_sample.set(None)
                
        def fetching_info(self):
                for i in self.student_table.get_children():
                        self.student_table.delete(i)
                data = fetching_data(self)
                for i in data:
                    self.student_table.insert("", "end", values = i)
                self.showAll_btn.config(state = DISABLED)
                        

        def searching_info(self, search_field, search_val):
                try:
                        for i in self.student_table.get_children():
                                self.student_table.delete(i)
                        data = searching_data(self, search_field, search_val)
                        for i in data:
                            self.student_table.insert("", "end", values = i)
                except:
                       messagebox.showerror("Invalid Search", "Invalid search. Try again.")




if __name__=="__main__":
        root=Tk()
        obj=Student(root)
        root.mainloop()
