from flask import Flask, request, redirect, render_template, url_for
from WEBSITE import app, db, bcrypt, mail
from WEBSITE.forms import MessageForm, LoginForm, UploadImage, UploadTestimonial, ReplyForm
from WEBSITE import errors
from WEBSITE.models import Message

@app.route('/', methods=['GET', 'POST'])
def home():
    form = MessageForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        content = form.content.data
        subject = form.subject.data
        message = Message(full_name=full_name, email=email,
                          content=content, subject=subject)
        db.session.add(message)
        db.session.commit()
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
    page = request.args.get("page", 1, type=int)
    paginate_object = Message.query.filter().paginate(page=int(page), per_page=5)
    return render_template('messages.html', paginate_object=paginate_object)

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
