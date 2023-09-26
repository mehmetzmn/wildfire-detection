import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
import ssl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cameras.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    pass


class Camera(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=15), nullable=False)
    location = db.Column(db.String(length=15), nullable=False)

    def __repr__(self):
        return f'Camera {self.name}'


@app.route('/')
def home():
    cameras = [
        {'id': 1, 'name': 'Camera 1', 'location': 'Room 1'},
        {'id': 2, 'name': 'Camera 2', 'location': 'Room 2'},
    ]

    return render_template('home.html', cameras=cameras, id=id)


@app.route('/camera/<int:id>', methods=['POST', 'GET'])
def camera(id):
    ROOT_STATIC_IMAGES = '../UI/static/images'
    # ROOT = '.' # os.path.listdir(ROOT) --> ['static', 'templates', 'app.py']

    camera_names = os.listdir(ROOT_STATIC_IMAGES)
    camera_paths = [os.path.join("/images/", camera_name) for camera_name in camera_names]
    
    image_paths = []
    for camera_path in camera_paths:
        if camera_path.startswith('/'):
            camera_path = camera_path[1:]  # Remove the leading slash
            if camera_path.startswith(f'images/camera{id}'):  # Check if camera_path matches the requested ID
                image_names = os.listdir(os.path.join('../UI/static', camera_path))
                for image_name in image_names:
                    image_paths.append(os.path.join(camera_path, image_name))
        
    
    if request.method == 'POST':

        selected_images = request.form.getlist('selected_images')
        select_all = request.form.get('select_all') == 'on'

        if select_all:
            # Select all images if the "Select All" checkbox is checked
            selected_images = [image_path for image_path in image_paths]
            print(selected_images)

        # return selected_images

        recipient_email = request.form['email']
        # selected_images = request.form.getlist('selected_images')
        selected_images = [os.path.join('../UI/static', image_path) for image_path in selected_images]
        print(selected_images)
        print(os.getcwd())

        mail_sender = 'mehmetbmw98@gmail.com'
        password = 'ocaysptewajeaarv'
        mail_receiver = recipient_email
        
        subject = 'Check out these selected images'


        msg = MIMEMultipart()
        msg['From'] = mail_sender
        msg['To'] = mail_receiver
        msg['Subject'] = subject

        for image_path in selected_images:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                print(type(image_data))
                image_attachment = MIMEImage(image_data)
                image_attachment.add_header('Content-Disposition', 'attachment', filename=image_path)
                msg.attach(image_attachment)

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(mail_sender, password)
                server.sendmail(mail_sender, mail_receiver, msg.as_bytes())
                server.quit()
            return 'Email sent successfully!'
        except Exception as e:
            return 'Error sending email: ' + str(e)
    else:
        return render_template('camera.html', id=id, image_paths=image_paths)
    


@app.route('/')
def logout():
    # logout user
    pass


if __name__ == "__main__":
    app.run(debug=True)