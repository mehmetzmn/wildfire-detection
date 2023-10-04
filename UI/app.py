import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
import ssl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cameras.db'
app.config['SECRET_KEY'] = '9ccad4f9bbbba1a4090e3110'
db = SQLAlchemy(app)
app.app_context().push() # adding this line to avoid write this "with app.app_context():" line everytime on python shell

"""
TODO: Decide whether to each user has their own cameras or not.
      If so, then add a foreign key to the User table.

"""

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    cameras = db.relationship('Camera', backref='user', lazy=True)


class Camera(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=15), nullable=False)
    location = db.Column(db.String(length=15), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Camera {self.name}'
    

############ Flask Forms ############

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class RegisterForm(FlaskForm):
    # NOTE: Validate_username function name is important. It is used by FlaskForm to validate the username field.
    #       FlaskForm will look for a function that starts with "validate_" and ends with the field name.

    def validate_field_uniqueness(self, field_name, field_data):
        user = User.query.filter_by(**{field_name: field_data}).first()
        if user: raise ValidationError(f'{field_name.capitalize()} already exists! Please try a different {field_name}')

    def validate_username(self, username_to_check):
        self.validate_field_uniqueness('username', username_to_check.data)

    def validate_email_address(self, email_address_to_check):
        self.validate_field_uniqueness('email_address', email_address_to_check.data)


    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()]) # Username
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()]) # Email
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()]) # Password
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()]) # Confirm Password
    submit = SubmitField(label='Submit') # Submit



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address= form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home'))
    if form.errors != {}: # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)



@app.route('/')
def home():
    # cameras = [
    #     {'id': 1, 'name': 'Camera 1', 'location': 'Room 1'},
    #     {'id': 2, 'name': 'Camera 2', 'location': 'Room 2'},
    # ]

    # I added manually the cameras to the database,
    # so I can test the database connection
    cameras = Camera.query.all()

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