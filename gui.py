import tkinter as tk
import os
from register_faces import register_faces
from attendance import mark_attendance

def on_register_faces_click():
    register_faces()
    status_label.config(text="Faces registered successfully!")

def on_mark_attendance_click():
    attendance = mark_attendance()
    status_label.config(text=f"Attendance: {', '.join(attendance)}")

root = tk.Tk()
root.title("Facial Recognition Attendance System")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

register_faces_button = tk.Button(frame, text="Register Faces", command=on_register_faces_click)
register_faces_button.grid(row=0, column=0, padx=10, pady=10)

mark_attendance_button = tk.Button(frame, text="Mark Attendance", command=on_mark_attendance_click)
mark_attendance_button.grid(row=0, column=1, padx=10, pady=10)

status_label = tk.Label(frame, text="")
status_label.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
