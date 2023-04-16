import os
import csv
import pickle
import face_recognition

def register_faces():
    face_encodings = {}
    face_data_path = 'face_data'
    students_csv = 'students.csv'

    students = {}

    # Read the student information from the CSV file
    with open(students_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students[row['face_data_folder']] = {
                'enrollment_number': row['enrollment_number'],
                'Cohortno': row['Cohortno'],
                'name': row['name'],
                'Field': row['Field'],
                'course': row['course'],
            }

    for person_folder in os.listdir(face_data_path):
        person_images_path = os.path.join(face_data_path, person_folder)

        for image_name in os.listdir(person_images_path):
            image_path = os.path.join(person_images_path, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) > 0:
                face_encoding = encodings[0]
                face_encodings[person_folder] = {
                    'encoding': face_encoding,
                    'info': students.get(person_folder)
                }

    with open('dataset_faces.dat', 'wb') as f:
        pickle.dump(face_encodings, f)

if __name__ == '__main__':
    register_faces()
