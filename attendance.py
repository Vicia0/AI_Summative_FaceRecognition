import cv2
import face_recognition
import pickle
import tkinter
import numpy as np
from tkinter import messagebox
from PIL import Image, ImageTk
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Load the known faces and encodings data
with open('face_encodings.pkl', 'rb') as f:
    known_faces_data = pickle.load(f)

video_capture = cv2.VideoCapture(0)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)
google_sheet_id = '1g0zmuSQKG5m4hYKGAdj3rpoWlvGij-kYg3NLKUUKeL4'
sheet = client.open_by_key(google_sheet_id).sheet1

def mark_attendance():
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)

    # Find all the faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face has a match in the known faces
        matches = face_recognition.compare_faces([data['encoding'] for data in known_faces_data.values()], face_encoding)

        # Find the closest match
        face_distances = face_recognition.face_distance([data['encoding'] for data in known_faces_data.values()], face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            # If a match is found, add the attendance data to the Google Sheet
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y %H:%M:%S")
            face_data = list(known_faces_data.values())[best_match_index]['info']
            sheet.append_row([face_data['enrollment_number'], face_data['name'], face_data['course'], date_time])
            messagebox.showinfo("Attendance", f"Attendance marked for {face_data['name']}")

def show_video():
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pil = Image.fromarray(frame_rgb)
    frame_tk = ImageTk.PhotoImage(frame_pil)

    video_label.config(image=frame_tk)
    video_label.image = frame_tk
    video_label.after(10, show_video)

root = tkinter.Tk()
root.title("Facial Recognition Attendance System")

video_label = tkinter.Label(root)
video_label.pack()

show_video()

take_attendance_button = tkinter.Button(root, text="Take Attendance", command=mark_attendance)
take_attendance_button.pack()

root.mainloop()
