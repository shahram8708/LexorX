from flask import Blueprint, render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm, GenerateForm, GenerateImageForm
from app.models import User, GeneratedImage
from app import db
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image
import base64
from google import genai
from google.genai import types
from io import BytesIO

bp = Blueprint('main', __name__)

API_KEY = "api_key"
client = genai.Client(api_key=API_KEY)

@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/generate", methods=['GET', 'POST'])
@login_required
def generate():
    form = GenerateForm()
    if form.validate_on_submit():
        prompt = form.prompt.data

        
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        filename = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = base64.b64decode(part.inline_data.data)
                image = Image.open(BytesIO(image_data))
                filename = secrets.token_hex(8) + '.png'
                filepath = os.path.join('app/static/images', filename)
                image.save(filepath)

                
                generated = GeneratedImage(prompt=prompt, image_file=filename, author=current_user)
                db.session.add(generated)
                db.session.commit()
                break

        flash('Image generated!', 'success')
        return redirect(url_for('main.generate'))

    images = GeneratedImage.query.filter_by(author=current_user).order_by(GeneratedImage.date_created.desc()).all()
    return render_template('generate.html', form=form, images=images)

@bp.route("/generate_image", methods=['GET', 'POST'])
@login_required
def generate_image():
    form = GenerateImageForm()
    if form.validate_on_submit():
        prompt = form.prompt.data
        uploaded_image = form.image.data  

        
        image = Image.open(uploaded_image)

        
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        filename = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = base64.b64decode(part.inline_data.data)
                image = Image.open(BytesIO(image_data))
                filename = secrets.token_hex(8) + '.png'
                filepath = os.path.join('app/static/images', filename)
                image.save(filepath)

                
                generated = GeneratedImage(prompt=prompt, image_file=filename, author=current_user)
                db.session.add(generated)
                db.session.commit()
                break

        flash('Image generated successfully!', 'success')
        return redirect(url_for('main.generate_image'))

    images = GeneratedImage.query.filter_by(author=current_user).order_by(GeneratedImage.date_created.desc()).all()
    return render_template('generate_image.html', form=form, images=images)

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route("/history")
@login_required
def history():
    images = GeneratedImage.query.filter_by(author=current_user).order_by(GeneratedImage.date_created.desc()).all()
    return render_template('history.html', images=images)
