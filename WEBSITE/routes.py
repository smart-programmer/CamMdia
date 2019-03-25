from flask import Flask, request, redirect, render_template, url_for
from flask_mail import Message as MailMessage
from WEBSITE import app, db, bcrypt, mail
from WEBSITE.forms import MessageForm, LoginForm, UploadImage, UploadTestimonial, ReplyForm, SimpleForm
from WEBSITE import errors
from WEBSITE.models import Message, Post
from WEBSITE.utils import save_image

@app.route('/', methods=['GET', 'POST'])
def home():

    images = Post.query.all()
    images.reverse()
    images = images[:15]

    path = url_for("static", filename="posts/images")

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

        #send mail
        string = f"""{subject}"""
        msg = MailMessage(string, sender=email, 
        recipients=["gbeast123488@gmail.com"])
        msg.body = f"""
        رسالة من {full_name}
        محتوى الرسالة:
        {content}"""
        mail.send(msg)
        return redirect(url_for("home"))
    return render_template('index.html', form=form, images=images, path=path)

@app.route('/images', methods=['GET'])
def images():
    path = url_for("static", filename="posts/images")

    category = request.args.get("category", type=str)
    if category:
        images = Post.query.filter_by(category=category).all()
    else:
        images = Post.query.all()

    return render_template('image_gallery.html', path=path, images=images)

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
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.filters.data
        url = form.url.data
        image_string = save_image(form.image.data, "static/posts/images")

        post = Post(image_string=image_string, category=category, post_title=title,
        post_description=description, project_link=url)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('uploadImage'))

    return render_template('upload_image.html', form=form)


@app.route('/admin/uploadTestimonial', methods=['GET', 'POST'])
def uploadTestimonial():
    form = UploadTestimonial()
    return render_template('upload_testimonial.html', form=form)


@app.route('/admin/all_images', methods=["GET", "POST"])
def all_images():
    form = SimpleForm()
    form.button1.content = "Delete"
    form.button2.text = "Delete"
    if form.validate_on_submit():
        postID = request.form.get("id")

        if request.form.get("button1"):
            return redirect(url_for("all_images"))
        else:
            post = Post.query.get(int(postID))
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for("all_images"))

    page = request.args.get("page", 1, type=int)
    paginate_object = Post.query.paginate(page=int(page), per_page=1)
    return render_template('all_images.html', paginate_object=paginate_object, form=form)  


@app.route('/admin/all_testimonial')
def all_testimonial():
    return render_template('all_testimonial.html', messages=messages)  

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
