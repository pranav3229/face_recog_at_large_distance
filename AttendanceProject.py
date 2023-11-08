import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime

# path = '/home/postman/face_recog/Face-Recognition-with-Masks/dataset'
# images = []     # LIST CONTAINING ALL THE IMAGES
# className = []    # LIST CONTAINING ALL THE CORRESPONDING CLASS Names
# myList = os.listdir(path)
# print(myList)
# print("Total Classes Detected:",len(myList))

# for x,cl in enumerate(myList):
#         curImg = cv2.imread(f'{path}/{cl}')
#         images.append(curImg)
#         className.append(os.path.splitext(cl)[0])

# print(className)

# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList

# def markAttendance(name):
#     #reading and writing csv at the same time
#     with open('Attendance.csv','r+') as f:
#         myDataList = f.readlines()
#         nameList =[]
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0]) #append only names in list

#         if name not in  line:
#             now = datetime.now()
#             dt_string = now.strftime("%H:%M:%S")
#             f.writelines(f'\n{name},{dt_string}')



# encodeListKnown = findEncodings(images)
# print(len(encodeListKnown))
# print('Encodings Complete')

# cap = cv2.VideoCapture(0)

# while True:
#     # Webcam Image
#     success, img = cap.read()
#     imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     #Webcam Encoding
#     facesCurFrame = face_recognition.face_locations(imgS,number_of_times_to_upsample=3)
#     encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#     #Find Matches
#     for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#         # matches = face_recognition.compare_faces(encodeListKnown, encodeFace,0.9)
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace,0.6)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         print(faceDis)
#         matchIndex = np.argmin(faceDis)

#         if matches[matchIndex]:
#             name = className[matchIndex].upper()
#             print(name)
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 #Because we reduced size of image above
#             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
#             markAttendance(name)

#         # if faceDis[matchIndex] < 0.50:
#         #     name = className[matchIndex].upper()
#         #     markAttendance(name)
#         # else:
#         #     name = 'Unknown'
#         # print(name)
#         # y1, x2, y2, x1 = faceLoc
#         # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#         # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#         # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)



#     cv2.imshow('Webcam', img)
#     cv2.waitKey(1)


# import face_recognition
# import cv2
# import numpy as np
# import os
# from datetime import datetime

path = '/home/postman/face_recog/Face-Recognition-with-Masks/dataset'
images = []  # List containing all the images
className = []  # List containing all the corresponding class Names
myList = os.listdir(path)
print(myList)
print("Total Classes Detected:", len(myList))

for x, cl in enumerate(myList):
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])

print(className)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    # reading and writing csv at the same time
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])  # append only names in list

        if name not in nameList:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dt_string}')


encodeListKnown = findEncodings(images)
print(len(encodeListKnown))
print('Encodings Complete')

cap = cv2.VideoCapture(0)

frame_count = 0
frame_interval = 3  # Process every 5th frame

while True:
    success, img = cap.read()

    if frame_count % frame_interval == 0:  # Process only every frame_interval frame
        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        if len(encodesCurFrame) > 0:
            faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame[0])  # Considering the first detected face

            if faceDis is not None and len(faceDis) > 0:
                matchIndex = np.argmin(faceDis)

                if faceDis[matchIndex] < 0.7:  # Adjust the threshold as needed
                    name = className[matchIndex].upper()
                    markAttendance(name)
                else:
                    name = 'Unknown'
                print(name)
                for (top, right, bottom, left), name in zip(facesCurFrame, [name]):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    frame_count += 1

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


