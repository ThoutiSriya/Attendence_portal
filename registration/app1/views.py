from tkinter import messagebox
from django.shortcuts import render, HttpResponse, redirect
from app1.models import stu, fac, attendence
from django.contrib.auth import authenticate, login
import cv2
import os
# import sqlite3
import numpy as np
from PIL import Image
import pickle
import face_recognition
import time
from datetime import datetime,date
from django.contrib import messages
import tkinter as tk
e1 = "a"
# Create your views here.

def Facsign(request):
    return render(request, 'Facsign.html')

def Facsave(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pass1 = request.POST.get('pass1')
        email = request.POST.get('email')
        type1 = request.POST.get('type1')
        print(name, email, pass1, type1)
        my_model = fac(name=name, pass1=pass1, email=email, type1=type1)
        my_model.save()
        return render(request, 'login.html')


def addFace(ref_id, name):
    n = 5
    try:
        f = open("ref_name.pkl", "rb")
        ref_dictt = pickle.load(f)
        f.close()
    except:
        ref_dictt = {}
    ref_dictt[ref_id] = name
    f = open("ref_name.pkl", "wb")
    pickle.dump(ref_dictt, f)
    f.close()

    try:
        f = open("ref_embed.pkl", "rb")
        embed_dictt = pickle.load(f)
        f.close()
    except:
        embed_dictt = {}

    def msg(k):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Info", "Image "+str(k+1)+"/"+str(n) +
                            " has been captured\nClick OK to Continue\nPress Enter to Close")

    def close():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Info", "Turning Off Camera...\nClick OK to end the Program")

    for i in range(n):
        webcam = cv2.VideoCapture(0)
        while True:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            key = cv2.waitKey(1)
            if key == 9: #9 - tab, 32 = space key == 32
                face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                if face_locations != []:
                    face_encoding = face_recognition.face_encodings(frame)[0]
                    if ref_id in embed_dictt:
                        embed_dictt[ref_id] += [face_encoding]
                    else:
                        embed_dictt[ref_id] = [face_encoding]
                    webcam.release()
                    cv2.waitKey(1)
                    msg(i)
                    break
            elif key == 13: # 13= enter
                webcam.release()
                close()
                cv2.destroyAllWindows()
    print(ref_dictt)
    print(embed_dictt)
    webcam.release()
    close()
    cv2.destroyAllWindows()

    f = open("ref_embed.pkl", "wb")
    pickle.dump(embed_dictt, f)
    f.close()

def Stusign(request):
    return render(request, 'Stusign.html')

def Stusave(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pass1 = request.POST.get('pass1')
        email = request.POST.get('email')
        ids = request.POST.get('ids')
        type1 = request.POST.get('type1')
        r = stu.objects.filter(email = email)
        print(len(r))
        if(len(r) == 0):
            print(name, email, pass1, ids, type1)
            my_model = stu(name=name, pass1=pass1, email=email, ids=ids, type1=type1)
            my_model.save()
            addFace(ids, name)
            return render(request, 'login.html')
        else:
            # return HttpResponse("user is already exist")
            msg1 = "user is already exists"
            context = {
                'msg1':msg1,
            }
            return render(request, 'msg.html', context)

def detecting(request):
    stud = stu.objects.get(email=e1)
    
    def close(msg1):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(msg1)
        # "Info", "Turning Off Camera...\nClick OK to end the Program")
            
        
    f = open("ref_name.pkl", "rb")
    ref_dictt = pickle.load(f)
    f.close()
    f = open("ref_embed.pkl", "rb")
    embed_dictt = pickle.load(f)
    f.close()
    
    known_face_encodings = []
    known_face_names = []
    for ref_id, embed_list in embed_dictt.items():
        for embed in embed_list:
            known_face_encodings += [embed]
            known_face_names += [ref_id]
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    dates = []
    times = []
    names = []
    l = len(times)
    t_end = time.time() + 60*10
    v = []
    while time.time() < t_end:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if stud.ids == name:
                        face_names.append(name)
                        v.append(1)
                if len(times) < len(face_names):
                    names.append(name)
                    dates.append(str(datetime.today()).split()[0])
                    times.append(datetime.now().strftime("%H:%M:%S"))
        process_this_frame = not process_this_frame
        print(process_this_frame)
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35),
                        (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            if name == "Unknown":
                cv2.putText(
                        frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                cv2.putText(
                        frame, ref_dictt[name], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == 13:
            msg1 = "Turning Off Camera...Click OK to end the Program"
            close(msg1)
            break
    if(len(v) > 0):
        l = len(times)
        for i in range(l):
            print(name)
            print(int(names[i]))
            s_id = names[i]
            try:
                attendence_objects = attendence.objects.filter(ids=s_id)
                m = None
                most_recent_date = datetime.min
                for attendance_obj in attendence_objects:
                    attendance_date = datetime.combine(attendance_obj.date, datetime.min.time())
                    if attendance_date > most_recent_date:
                        m = attendance_obj
                        most_recent_date = attendance_date
            except attendence.DoesNotExist:
                m = None
            if m == None:
                temp = attendence(ids=s_id, date=dates[i], ftime=times[i], cnt=1, stime=times[i], status="absent")
                temp.save()
                msg1 = "detect your face after 1 min to get present for the day"
                close(msg1)
            else:
                print(m.cnt)
                if(m.cnt == '2'):
                    if(m.date.isoformat() != dates[i]):
                        temp = attendence(ids=s_id, date=dates[i], ftime=times[i], cnt=1, stime=times[i], status="absent")
                        temp.save()
                    else:
                        msg1 = "your attendence is already noted"
                        close(msg1)
                elif(m.cnt == '1'):
                    if(m.date.isoformat() == dates[i]):
                        m.stime = times[i]
                        m.save() 
                        print(repr(m.ftime), repr(m.stime))

                        ftime_datetime = datetime.combine(date.today(), m.ftime)
                        stime_datetime = datetime.combine(date.today(), datetime.strptime(m.stime, "%H:%M:%S").time())
                        
                        time_diff = stime_datetime - ftime_datetime
                        if(time_diff.total_seconds() >= 60):
                            m.cnt = 2
                            m.status = "present"
                            m.save()
                            msg1 = "done, you are present for day"
                            close(msg1)
                        else:
                            msg1 = "1 minute is not over"
                            close(msg1)
                    else:
                        temp = attendence(ids=s_id, date=dates[i], ftime=times[i], cnt=1, stime=times[i], status="absent")
                        temp.save()
                        # msg1 = "1 day is over so you are absent for the day"
                        # close(msg1)
    else:
        msg1 = "your face is not detectedd"
        close(msg1)
    video_capture.release()
    cv2.destroyAllWindows()
    return render(request,'msg.html')

def viewing(request):
    print(e1)
    r = stu.objects.get(email = e1)
    rows = attendence.objects.filter(ids = r.ids)
    context = {'rows': rows}
    return render(request, 'Stuview.html', context)

def LoginPage1(request):
    return render(request, 'login.html')

def LoginPage(request):
    if request.method == 'POST':
        type1 = request.POST.get('type1')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        print("hello")
        if(type1 == 'f'):
            obj = fac.objects.all()
            for i in obj:
                if(i.email == email and i.pass1 == pass1):
                    return render(request, 'Facdash.html')
            return HttpResponse("invalid credentialss")
        else:
            obj = stu.objects.all()
            for i in obj:
                if(i.email == email and i.pass1 == pass1):
                    global e1
                    e1 = email
                    return render(request, 'Studash.html')
            msg1 = "invalid credentials"
            context = {
                'msg1': msg1,
            }
            return render(request, 'msg.html', context)
            # return HttpResponse("invalid credentialss")
    return render(request, 'login.html')

def HomePage(request):
    return render(request, 'home.html')

def display(request):
    return render(request, 'home.html')

def Studash(request):
    return render(request, 'Studash.html')



# def SignupPage(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('pass1')
#         type1 = request.POST.get('type1')
#         print(name, pass1, email, type1)
#     return render(request, 'signup.html')

# def save_form(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         pass1 = request.POST.get('pass1')
#         email = request.POST.get('email')
#         type1 = request.POST.get('type1')
#         print(name, email, pass1)
#         if(type1 == 's'):
#             my_model = stu(name=name, pass1=pass1, email=email, type1=type1)
#             my_model.save()
#             return render(request, 'Stulogin.html')
#         else:
#             my_model = fac(name=name, pass1=pass1, email=email, type1=type1)
#             my_model.save()
#             return render(request, 'Faclogin.html')
#     return HttpResponse("dfdf")

# def training():

#     path = 'dataset' # Path for samples already taken

#     recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
#     detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#     #Haar Cascade classifier is an effective object detection approach


#     def Images_And_Labels(path): # function to fetch the images and labels

#         imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
#         faceSamples=[]
#         ids = []

#         for imagePath in imagePaths: # to iterate particular image path

#             gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
#             img_arr = np.array(gray_img,'uint8') #creating an array

#             id = int(os.path.split(imagePath)[-1].split(".")[1])
#             faces = detector.detectMultiScale(img_arr)

#             for (x,y,w,h) in faces:
#                 faceSamples.append(img_arr[y:y+h,x:x+w])
#                 ids.append(id)

#         return faceSamples,ids

#     print ("Training faces. It will take a few seconds. Wait ...")

#     faces,ids = Images_And_Labels(path)
#     print(faces, ids)
#     recognizer.train(faces, np.array(ids))
#     recognizer.write('trainer/trainer.yml')  # Save the trained model as trainer.yml
#     print("Model trained, Now we can recognize your face.")