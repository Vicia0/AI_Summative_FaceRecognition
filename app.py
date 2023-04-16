import os
import csv
import base64
import uuid
import cv2
import numpy as np
from io import BytesIO
from flask import Flask, render_template, request, redirect
from PIL import Image
from attendance import mark_attendance

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        image_data = request.form['image_data']
        imgdata = base64.b64decode(image_data.split(',')[1])
        img = Image.open(BytesIO(imgdata))
        img = np.array(img)

        attendance_result = mark_attendance(img)

        # If you want to show the result to the user, you can return it here
        return f"Attendance Result: {attendance_result}"

    return render_template('attendance.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        enrollment_number = request.form['enrollment_number']
        cohortno = request.form['cohortno']
        field = request.form['Field']
        course = request.form['course']
        image_data = request.form['image_data']

        # Save student information to students.csv
        with open('students.csv', 'a', newline='') as csvfile:
            fieldnames = ['enrollment_number', 'cohortno', 'name', 'Field', 'course', 'face_data_folder']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            face_data_folder = uuid.uuid4().hex
            writer.writerow({
                'enrollment_number': enrollment_number,
                'cohortno': cohortno,
                'name': name,
                'Field': field,
                'course': course,
                'face_data_folder': face_data_folder
            })

        # Save student image to face_data folder
        face_data_dir = os.path.join('face_data', face_data_folder)
        os.makedirs(face_data_dir, exist_ok=True)

        imgdata = base64.b64decode(image_data.split(',')[1])
        img = Image.open(BytesIO(imgdata))
        img.save(os.path.join(face_data_dir, 'face.jpg'))

        return redirect('/')

    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)
