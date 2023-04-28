import face_recognition
import cv2
import numpy as np
import os
import csv
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Load known faces and names
def load_known_faces():
    known_faces = []
    known_names = []

    # Load known faces from face_data directory
    for file in os.listdir('face_data'):
        image = face_recognition.load_image_file(f'face_data/{file}')
        face_encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(face_encoding)
        known_names.append(os.path.splitext(file)[0])

    return known_faces, known_names

def mark_attendance(name):
    try:
        sheet = client.open('Attendance').sheet1
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        sheet.insert_row([name, date, time])
    except Exception as e:
        print(f'Error: {e}')

def recognize_student(frame, face_locations, face_encodings, known_faces, known_names):
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_faces, face_encoding)

        # If a match was found, mark the attendance for that student
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            mark_attendance(name)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left+6, bottom-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    return frame
def add_attendance(name):
    try:
        sheet = client.open('Attendance').sheet1
        today = date.today().strftime('%m/%d/%Y')
        present = sheet.find(today).row
        names = sheet.row_values(1)
        if name in names:
            col = names.index(name) + 1
            sheet.update_cell(present, col, 'Present')
            print(name + " is marked as present.")
        else:
            print(name + " is not recognized.")
    except:
        print('Error: Could not update attendance.')

