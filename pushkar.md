### 4 NOV

- face_recognition.compare_faces -> param tolerance: How much distance between faces to consider it a match. Lower is more strict. 0.6 is typical best performance. -> no changes seen
- face_recognition.face_locations -> param number_of_times_to_upsample: How many times to upsample the image looking for faces. Higher numbers find smaller faces. -> 3 -> no delay approx 1.4 metres, 5-> 3-4 secs delay.
- face_recognition.face_locations -> param model: Which face detection model to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate
                  deep-learning model which is GPU/CUDA accelerated (if available). The default is "hog".

                  with face_locations.hog + face_locations.number_of_times_to_upsample=3 + compare_faces.tolerance = 0.6 -> approx 1.5 meters
