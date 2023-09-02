from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk #Pillow Library
from attendance_2 import Attendance 
from student import Student
from compProject_FaceRecognition_06012022 import *
import numpy as np

class Face_Recognition_System:
        def __init__(self,root):
                self.root=root #initialising root
                self.root.geometry("1530x790+0+0")
                self.root.title("Face Recognition")


        #Image 1
                img=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/university.jpg") 
                img=img.resize((500,130),Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg=ImageTk.PhotoImage(img) #variable goes inside parameter
                

                f_lb1=Label(self.root,image=self.photoimg)
                f_lb1.place(x=0,y=0,width=500,height=130) #place requires axes
        #Image 2
                img1=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/face.jpg") 
                img1=img1.resize((500,130),Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg1=ImageTk.PhotoImage(img1) #variable goes inside parameter

                f_lb1=Label(self.root,image=self.photoimg1)
                f_lb1.place(x=500,y=0,width=550,height=130) #place requires axes
        #Image 3
                img2=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/princeton.jpg") 
                img2=img2.resize((500,130),Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg2=ImageTk.PhotoImage(img2) #variable goes inside parameter

                f_lb1=Label(self.root,image=self.photoimg2)
                f_lb1.place(x=1000,y=0,width=550,height=130) #place requires axes
        #background image
                img3=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/pink.jpg") 
                img3=img3.resize((1530,710),Image.ANTIALIAS) #ANTIALIAS converts high level img to low level
                self.photoimg3=ImageTk.PhotoImage(img3) #variable goes inside parameter

                bg_img=Label(self.root,image=self.photoimg3)
                bg_img.place(x=0,y=130,width=1530,height=710) #place requires axes

                title_lbl=Label(bg_img,text="Face Recognition Attendance System",font=("Helvetica",25,"bold"),bg="white",fg="black") #bg is background, fg is foreground
                title_lbl.place(x=0,y=0,width=1530,height=45)
        #Student button
                img4=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/teen.jpg") 
                img4=img4.resize((300,230),Image.ANTIALIAS) 
                self.photoimg4=ImageTk.PhotoImage(img4)

                b1=Button(bg_img,image=self.photoimg4,cursor="hand2", command = lambda: self.StudentWindow_fn(Student))  #cursor hand changes cursor over button
                b1.place(x=325,y=90,width=220,height=220)

                b1_1=Button(bg_img,text="Student Details",cursor="hand2",font=("Helvetica",15,"bold"),bg="white",fg="black", command = lambda: self.StudentWindow_fn(Student)) 
                b1_1.place(x=325,y=290,width=220,height=40)

        # Detect Face Button
                img5=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/face_detector1.jpg") 
                img5=img5.resize((300,230),Image.ANTIALIAS) 
                self.photoimg5=ImageTk.PhotoImage(img5)

                b1=Button(bg_img,image=self.photoimg5,cursor="hand2", command = self.FR_fn) 
                b1.place(x=650,y=90,width=220,height=220)

                b1_1=Button(bg_img,text="Face Detector",cursor="hand2",font=("Helvetica",15,"bold"),bg="white",fg="black", command = self.FR_fn)
                b1_1.place(x=650,y=290,width=220,height=40)
        #Attendance Button
                img6=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/clg.jpg") 
                img6=img6.resize((300,230),Image.ANTIALIAS) 
                self.photoimg6=ImageTk.PhotoImage(img6)

                b1=Button(bg_img,image=self.photoimg6,cursor="hand2", command = lambda: self.AttendanceWindow_fn(Attendance)) 
                b1.place(x=975,y=90,width=220,height=220)

                b1_1=Button(bg_img,text="Attendance",cursor="hand2",font=("Helvetica",15,"bold"),bg="white",fg="black", command = lambda: self.AttendanceWindow_fn(Attendance)) 
                b1_1.place(x=975,y=290,width=220,height=40)

        #Exit
                img11=Image.open(os.path.dirname(os.path.realpath(__file__))+"/img/exit.jpg") 
                img11=img11.resize((300,230),Image.ANTIALIAS) 
                self.photoimg11=ImageTk.PhotoImage(img11)

                b1=Button(bg_img,image=self.photoimg11,cursor="hand2", command = self.root.quit) 
                b1.place(x=650,y=390,width=220,height=220)

                b1_1=Button(bg_img,text="Exit",cursor="hand2",font=("Helvetica",15,"bold"),bg="white",fg="black", command = self.root.quit) 
                b1_1.place(x=650,y=590,width=220,height=40)

                
                

                
        def AttendanceWindow_fn(self, Attendance):
                self.AttendanceWindow = Toplevel(self.root)
                Attendance(self.AttendanceWindow)

        def StudentWindow_fn(self, Student):
                self.StudentWindow = Toplevel(self.root)
                Student(self.StudentWindow)
                #print((Student.sample_face_encodings, Student.sample_face_names))

        def FaceRecognitionWindow_fn(self, Face_Recognition):
                self.FaceRecognitionWindow = Toplevel(self.root)
                Face_Recognition(self.FaceRecognitionWindow)
                
        def FR_fn(self):
                sample_face_encodings, sample_face_names = load_images()
                face_recognition_fn(sample_face_encodings, sample_face_names)



if __name__=="__main__":
        master=Tk()
        obj=Face_Recognition_System(master)
        master.mainloop()