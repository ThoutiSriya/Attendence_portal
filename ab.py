import cv2
import os
# import sqlite3
import numpy as np
from PIL import Image
n = 5
import os
import pickle
import numpy as np
import cv2
import face_recognition
import numpy as np
from datetime import datetime
import time
embed_dictt = {}
ref_id = 2
for i in range(n):
    key = cv2. waitKey(1)
    # webcam = cv2.VideoCapture(0)
    webcam = cv2.VideoCapture(0)
    time.sleep(1)
    while True:
        check, frame = webcam.read()
        # if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
        #     cv2.imshow("Capturing", frame)
        # else:
        #     print("Invalid frame dimensions")
        # # check, frame = webcam.read()
        # print(frame)
        cv2.imshow("Capturing", frame)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        key = cv2.waitKey(1)
        if key == 32:
            face_locations = face_recognition.face_locations(
                rgb_small_frame)
            if face_locations != []:
                face_encoding = face_recognition.face_encodings(frame)[0]
                print(face_encoding)
                if ref_id in embed_dictt:
                    embed_dictt[ref_id] += [face_encoding]
                else:
                    embed_dictt[ref_id] = [face_encoding]
                webcam.release()
                cv2.waitKey(1)
                break
        elif key == 13:
            webcam.release()
            cv2.destroyAllWindows()
print()
print(embed_dictt )
print()
known_face_encodings = []
known_face_names = []
for ref_id, embed_list in embed_dictt.items():
    for embed in embed_list:
        known_face_encodings += [embed]
        known_face_names += [ref_id]

print(known_face_encodings)
print()
print(known_face_names)