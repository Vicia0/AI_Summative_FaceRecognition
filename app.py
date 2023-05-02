from flask import Flask
import face_recognition
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from google.oauth2 import service_account
from flask import render_template
from flask import Flask, render_template, request, flash
import cv2
import face_recognition
import pickle
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, redirect, url_for
import os.path
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask
import csv
from flask import Flask, render_template, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv
import os
from datetime import datetime
from imutils.video import VideoStream
from utils import *
import tkinter
import Tkinter


app = Flask(__name__)
app.secret_key = 'secretkey'

# set up Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Attendance').sheet1



# Load the known faces and their encodings
face_encodings = []
known_face_names = []
for file in os.listdir('face_data'):
    try:
        image = face_recognition.load_image_file(os.path.join('face_data', file))
        face_encoding = face_recognition.face_encodings(image)[0]
        face_encodings.append(face_encoding)
        name = os.path.splitext(file)[0]
        known_face_names.append(name)
    except Exception as e:
        print(f"Error loading face data from {file}: {e}")

# Load the face detection cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# Initialize the camera
try:
    cam = cv2.VideoCapture(0)
except Exception as e:
    print(f"Error initializing camera: {e}")
    cam = None

# home page
@app.route('/')
def home():
    try:
        students = sheet.get_all_records()
    except Exception as e:
        print(f"Error retrieving students from Google Sheets: {e}")
        students = []
    return render_template('index.html', students=students)

# attendance page
@app.route('/attendance')
def take_attendance():
    return render_template('attendance.html')


# handle attendance data
@app.route('/attendance_data', methods=['POST'])
def attendance_data():
    if request.method == 'POST':
        # Process the attendance data here
        # ...
        return jsonify({'success': True})


# save attendance to Google Sheets
@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    # Load the attendance sheet
    with open('Attendance.csv', 'a+') as f:
        writer = csv.writer(f)
        try:
            # Load the image of the student's face
            _, img = cam.read()
            # Convert to grayscale for face recognition
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect the face in the image
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                # Crop the face from the image
                face_img = img[y:y+h, x:x+w]
                # Encode the face for recognition
                encodings = face_recognition.face_encodings(face_img)
                if len(encodings) > 0:
                    # Compare the face with existing faces in the face_data folder
                    matches = face_recognition.compare_faces(face_encodings, encodings[0])
                    if True in matches:
                        # If the face matches, mark attendance for the corresponding name
                        name = known_face_names[matches.index(True)]
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        writer.writerow([name, dt_string])
                        return render_template('success.html', name=name)
            return render_template('failure.html')
        except:
            return render_template('failure.html')

# add new student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        enrollment_number = request.form['enrollment_number']
        course = request.form['course']

        # Get the image file
        image_file = request.files['image_file']
        if image_file:
            # Create the face_data directory if it does not exist
            face_data_dir = 'face_data'
            if not os.path.exists(face_data_dir):
                os.makedirs(face_data_dir)

            # Save the image file to the face_data directory
            image_path = os.path.join(face_data_dir, f'{enrollment_number}.jpg')
            image_file.save(image_path)

            # Add the student's details to the CSV file
            with open('students.csv', 'a') as f:
                f.write(f'{name},{enrollment_number},{course},{image_path}\n')

            # Redirect to the home page with a success message
            message = f'Student {name} with enrollment number {enrollment_number} added successfully!'
            return redirect(url_for('home', message=message))

        # If no file was provided, show an error message
        error_message = 'Please provide an image file'
        return render_template('add_student.html', error_message=error_message)

    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)

