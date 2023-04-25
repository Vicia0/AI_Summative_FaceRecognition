# AI_Summative_FaceRecognition
**#Face Recognition Attendance System**

This project is a face recognition attendance system that uses a webcam to capture images of students and recognize their faces to mark attendance. The system is built using Python, Flask, OpenCV, and face recognition libraries.

**#Requirements**
Python 3.6+
Flask
OpenCV
face recognition
imutils

**#Installation**
Clone this repository to your local machine.
Install the required dependencies using the command pip install -r requirements.txt.
Run the app using the command python app.py
Navigate to http://localhost:5000 in your web browser to access the application.

**#Usage**
Register students for a course by adding their name and image to the face_data directory.
Navigate to the attendance page and click the Start Attendance button to begin taking attendance.
The system will capture an image of each student and mark attendance for those whose faces are recognized.
The attendance data is stored in a CSV file in the data directory.

**#Hosting on a Local Server**
To host this application on a local server, follow these steps:

Install a web server software such as Apache or Nginx.
Install Python and the required dependencies.
Configure the web server to serve the Flask application.
Start the web server and navigate to the application URL in your web browser.

**#Hosting on Cloud**
To host this application on a cloud service such as AWS or Azure, follow these steps:

Create a new virtual machine instance and install the required dependencies.
Configure the virtual machine firewall to allow incoming HTTP requests.
Deploy the Flask application to the virtual machine using a web server such as Apache or Nginx.
Configure the DNS to point to the virtual machine public IP address.
Access the application from the DNS URL in your web browser.
