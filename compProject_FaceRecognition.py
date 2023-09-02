import cv2
import numpy as np
import face_recognition
from datetime import datetime 
import csv
import os
from os import listdir
from os.path import isfile, join


def collect_samples(sample_name, student_id):
	vid_capture = cv2.VideoCapture(0)	#opens the video stream.

	img_captured = False
	while True:
		if not vid_capture.isOpened():	#checks if vid stream is open.
			vid_capture.open()	#opens vid stream if vid stream hadn't been opened.

		return_val, frame = vid_capture.read()	#captures single frame from camera.
		rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)	#OpenCV uses BGR format, whereas face_recognition uses RGB - we change it here.

		face_locations = face_recognition.face_locations(rgb_img)	#finding the coordinates for each face in the img
		face_encodings = face_recognition.face_encodings(rgb_img, face_locations)	#generates array of faces.

		for (top_coord, right_coord, bottom_coord, left_coord), face_encoding in zip(face_locations, face_encodings):	#Going through each face in the frame.
			img_dir = os.path.dirname(os.path.realpath(__file__))+"//Sample_Imgs/" 
			if cv2.waitKey(1) & 0xFF == ord("y"):	#writes the frame into memory, then closes the window if user presses "y".
				img_dir = os.path.dirname(os.path.realpath(__file__))+"//Sample_Imgs/" 
				cv2.imwrite("{}{}_{}_sample_img.jpg".format(img_dir, sample_name, student_id), frame)
				#print("Sample image captured!")
				img_captured = True
				continue

			#cv2.imwrite("{}{}_sample_img.jpg".format(img_dir, sample_name), frame)
			cv2.rectangle(frame, (left_coord, top_coord), (right_coord, bottom_coord), (214, 119, 30), 2)	#drawing rectangles around the faces.
			#Syntax: cv2.rectangle(<img>, <start pt>, <end pt>, <colour - BGR format>, <thickness - -1 means filled rectangle>)
			cv2.rectangle(frame, (left_coord, bottom_coord - 30), (right_coord, bottom_coord), (214, 119, 30), -1)	#a label below the rectangle.
			#cv2.circle(frame, (int((top_coord+bottom_coord)/2),int((left_coord+right_coord)/2)), int((top_coord+bottom_coord)/2), (102, 148, 227), 10)
			cv2.putText(frame, "Face detected - press 'y'", (left_coord + 5, bottom_coord - 5), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA, False)
			

		cv2.imshow("Taking Samples", frame)	#displays the frame.

		if cv2.waitKey(1) & 0xFF == ord("q") or img_captured:	#closes the window if user presses 'q'.
			break

	vid_capture.release()
	cv2.destroyAllWindows()



def load_images(): #sample_name):	#encodes the sample images as arrays.
	sample_face_encodings, sample_face_names = [], []
	img_found = False
	try:
		img_dir = os.path.dirname(os.path.realpath(__file__))+"/Sample_Imgs/"  	 #image directory.
		onlyfiles = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]
		for i in onlyfiles: 
			
			if i[::-1][:15][::-1] == "_sample_img.jpg":
				img_found = True
				sample_name2 = i.split("_")[0]
				student_id = i.split("_")[1]
				sample_face_names.append(sample_name2+"_"+student_id)
				sample_img2 = face_recognition.load_image_file("{}{}_{}_sample_img.jpg".format(img_dir, sample_name2, student_id))	#loads the image from the file.
				
				try:
					sample_face_encoding2 = face_recognition.face_encodings(sample_img2)[0]
					sample_face_encodings.append(sample_face_encoding2)
				except IndexError:
					print("Couldn't detect any faces in {}'s image!".format(sample_name2))		#exception handling.
					continue
		if img_found == False:
			print("No sample images taken!")
			quit()
	
	except Exception as es:
		print("You haven't given us a sample for this name yet!")
		quit()

	return sample_face_encodings, sample_face_names 


def face_recognition_fn(sample_face_encodings, sample_face_names):
	vid_capture = cv2.VideoCapture(0)

	identified_faces = []

	while True:
		return_val, frame = vid_capture.read()	#captures a single frame.
		
		if not vid_capture.isOpened():	#sometimes, vid_capture may not open the vid stream.
			vid_capture.open()	#if it doesn't open the stream, we open it here.

		rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)	#OpenCV uses BGR format, whereas face_recognition uses RGB - we change it here.

		face_locations = face_recognition.face_locations(rgb_img)	#finding the coordinates for each face in the img
		face_encodings = face_recognition.face_encodings(rgb_img, face_locations)	#generates array of faces.

		cv2.rectangle(frame, (20, 15), (340, 55), (214, 119, 30), -1)	#a label below the rectangle.
		cv2.putText(frame, str("Press 'q' to close"), (30, 45), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA, False)

		for (top_coord, right_coord, bottom_coord, left_coord), face_encoding in zip(face_locations, face_encodings):	#Going through each face in the frame.
			face_matches = face_recognition.compare_faces(sample_face_encodings, face_encoding)		#comparing faces to sample pics.

			display_name_id = "Unknown"	#name to be displayed if face is not recognised.

			face_distances = face_recognition.face_distance(sample_face_encodings, face_encoding)
			best_match_ind = np.argmin(face_distances)	#finds min distanced face in the array, 'face_distances'
			if face_matches[best_match_ind]:	#if the index exists in the matches list, we set the name to the corresponding sample name.
				display_name_id = sample_face_names[best_match_ind]
				
				date = datetime.now().strftime("%d-%m-%Y")
				time = datetime.now().strftime("%H:%M:%S")
				identified_faces.append(display_name_id)


				mark_attendance(date, time, display_name_id.split("_")[0], display_name_id.split("_")[1])	#marks attendance as soon as it sees the face.
			try:
				cv2.rectangle(frame, (left_coord, top_coord), (right_coord, bottom_coord), (214, 119, 30), 2)	#drawing rectangles around the faces.
				#Syntax: cv2.rectangle(<img>, <start pt>, <end pt>, <colour - BGR format>, <thickness - -1 means filled rectangle>)
				cv2.rectangle(frame, (left_coord, bottom_coord - 30), (right_coord, bottom_coord), (214, 119, 30), -1)	#a label below the rectangle.
				#cv2.circle(frame, (int((top_coord+bottom_coord)/2),int((left_coord+right_coord)/2)), int((top_coord+bottom_coord)/2), (102, 148, 227), 10)
				cv2.putText(frame, str(display_name_id.split("_")[0]+", Student ID: "+display_name_id.split("_")[1]), (left_coord + 5, bottom_coord - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA, False)
				#Syntax: cv2.putText(<img>, <text>, <origin>, <font>, <fontScale AKA size>, 
				#<colour>, <thickness>, <lineType - cv2.line_AA stands for anti-aliased line, 
				#basically its a smoothly curved line.>, <if text starts from bottom-left - default: False>)
			except:
				pass

		cv2.imshow("Face Recognition", frame)	#displays the frame.
		if cv2.waitKey(1) & 0xFF == ord("q"):	#quits if user presses enter.
			break

	vid_capture.release()	#releasing the video stream.
	cv2.destroyAllWindows()	#destroying the OpenCV window.

	return list(dict.fromkeys(identified_faces))	#returning list of ppl indentified after removing duplicate names.

def mark_attendance(date, time, name, student_id):
	csv_input = []
	student_id_date = []
	while True:
		try:
			with open(os.path.dirname(os.path.realpath(__file__))+"/Attendance_register_25_7_21.csv", "r", newline = "") as file:
				reader_object = csv.reader(file)
				for i in reader_object:
					csv_input.append(i)
					
					if i != ["\n"] and i != ["Student ID", "Name", "Date", "Time", "Present/Absent"]:
						student_id_date.append([i[0], i[2]])
			break
		except FileNotFoundError:
			with open(os.path.dirname(os.path.realpath(__file__))+"/Attendance_register_25_7_21.csv", "w", newline = "") as file:
				writer_object = csv.writer(file)
				title = ["Student ID", "Name", "Date", "Time", "Present/Absent"]
				writer_object.writerow(title)


	with open(os.path.dirname(os.path.realpath(__file__))+"/Attendance_register_25_7_21.csv", "w", newline = "") as file:
		writer_object = csv.writer(file)
		title = ["Student ID", "Name", "Date", "Time", "Present/Absent"]
		if title not in csv_input:
			csv_input.append(title)
		
		if student_id_date != [] and student_id_date[len(student_id_date)-1][1] != date and student_id_date[len(student_id_date)-1][1] != "" and csv_input[len(csv_input)-1] != ["\n"]:
			csv_input.append("\n")
		
		if [student_id, date] not in student_id_date:
			csv_input.append([student_id, name, date, time, "Present"])
		writer_object.writerows(csv_input)