###AI_Summative_FaceRecognition attendance system using python and openCV

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) 

###Face Recognition Attendance System

This project is a face recognition attendance system that uses a webcam to capture images of students and recognize their faces to mark attendance. The system is built using Python, Flask, OpenCV, and face recognition libraries.

###Requirements

Python 3.6+
Flask
OpenCV
face recognition
imutils


###Installation

-Clone this repository to your local machine.
-Install the required dependencies using the command pip install -r requirements.txt.
-Run the app using the command python app.py
-Navigate to http://localhost:5000 in your web browser to access the application.


**#Usage**

1.Register students for a course by adding their name and image to the face_data directory.

2.Navigate to the attendance page and click the Start Attendance button to begin taking attendance.

3.The system will capture an image of each student and mark attendance for those whose faces are recognized.

4.The attendance data is stored in a CSV file in the data directory.


**#Hosting on a Local Server**

To host this application on a local server, follow these steps:

1.Install a web server software such as Apache or Nginx.

2.Install Python and the required dependencies.

3.Configure the web server to serve the Flask application.

4.Start the web server and navigate to the application URL in your web browser.


**#Hosting on Cloud**

1.To host this application on a cloud service such as AWS or Azure, follow these steps:

2.Create a new virtual machine instance and install the required dependencies.

3.Configure the virtual machine firewall to allow incoming HTTP requests.

4.Deploy the Flask application to the virtual machine using a web server such as Apache or Nginx.

5.Configure the DNS to point to the virtual machine public IP address.

6.Access the application from the DNS URL in your web browser.
