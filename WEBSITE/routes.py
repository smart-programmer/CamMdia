from flask import Flask, request, redirect, render_template, url_for
from WEBSITE import app
from WEBSITE.forms import MessageForm, LoginForm, UploadImage, UploadTestimonial, ReplyForm
import secrets

@app.route('/', methods=['GET', 'POST'])
def home():
    form = MessageForm()
    return render_template('index.html', form=form)

@app.route('/images', methods=['GET', 'POST'])
def images():
    return render_template('image_gallery.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/admin/uploadImage', methods=['GET', 'POST'])
def uploadImage():
    form = UploadImage()
    return render_template('upload_image.html', form=form)


@app.route('/admin/uploadTestimonial', methods=['GET', 'POST'])
def uploadTestimonial():
    form = UploadTestimonial()
    return render_template('upload_testimonial.html', form=form)


@app.route('/admin/all_images')
def all_images():
    return render_template('all_images.html')  


@app.route('/admin/all_testimonial')
def all_testimonial():
    return render_template('all_testimonial.html')  

@app.route('/admin/messages')
def messages():
    return render_template('messages.html')

@app.route('/admin/deleted_messages')
def deleted_messages():
    return render_template('deleted_messages.html')

@app.route('/admin/done_messages')
def done_messages():
    return render_template('done_messages.html')  


@app.route('/admin/reply')
def reply():
    form = ReplyForm()
    return render_template('reply.html', form=form)
