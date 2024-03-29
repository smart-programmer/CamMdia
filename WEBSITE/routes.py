from flask import Flask, request, redirect, render_template, url_for, make_response
from flask_mail import Message as MailMessage
from WEBSITE import app, db, bcrypt, mail, MAIL_USERNAME
from WEBSITE.forms import MessageForm, LoginForm, UploadImage, UploadTestimonial, ReplyForm, SimpleForm, UserForm
from WEBSITE import errors
from WEBSITE.models import Message, Post, Testimonial, User, Visitors
from WEBSITE.utils import save_image, handle_new_visitor, save_image_locally, delete_s3_object
from flask_login import current_user, login_user, login_required, logout_user



# /// 5air

@app.route('/', methods=['GET', 'POST'])
def home():

    testimonials = Testimonial.query.filter_by(state="active")

    images = Post.query.all()
    images.reverse()
    images = images[:15]

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
        msg = MailMessage(string, sender=MAIL_USERNAME, 
        recipients=[MAIL_USERNAME])
        msg.body = f"""
        رسالة من {full_name}:
        ايميل:{email}
        
        محتوى الرسالة:
        {content}"""
        mail.send(msg)
        return redirect(url_for("home"))

    # visitors counter system
    response = make_response(render_template('index.html', form=form, images=images,
    testimonials=testimonials))
    did_visit = request.cookies.get("did_visit")
    if not did_visit:
        handle_new_visitor(response)
    return response

@app.route('/developers', methods=['GET', 'POST'])
def developers():
    return render_template('develpors_page.html')
    
@app.route('/images', methods=['GET'])
def images():
    path = url_for("static", filename="posts/images")

    category = request.args.get("category", type=str)
    if category:
        images = Post.query.filter_by(category=category).all()
        images.reverse()
    else:
        images = Post.query.all()
        images.reverse()

    # visitors counter system
    response = make_response(render_template('image_gallery.html', path=path, images=images))
    did_visit = request.cookies.get("did_visit")
    if not did_visit:
        handle_new_visitor(response)
    return response

@app.route('/admin/', methods=["GET"])
@login_required
def admin():
    # get visitors count
    # visitors = 0
    # with open(get_visitors_file(), "r") as visitors_file:
    #     visitors = visitors_file.read()

    visitors_count = Visitors.query.get(1).count

    # get active messages count
    messages = 0
    messages = len(Message.query.filter_by(state="active").all())
    return render_template('admin.html', visitors=visitors_count, messages_count=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("admin"))
            else:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))
    return render_template('login.html', form=form)

@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/admin/uploadImage', methods=['GET', 'POST'])
@login_required
def uploadImage():
    form = UploadImage()
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.filters.data
        url = form.url.data
        image_string, image_path = save_image(form.image.data, "static/posts/images")

        post = Post(image_string=image_string, image_path=image_path, category=category, post_title=title,
        post_description=description, project_link=url)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('uploadImage'))

    return render_template('upload_image.html', form=form)


@app.route('/admin/uploadTestimonial', methods=['GET', 'POST'])
@login_required
def uploadTestimonial():
    form = UploadTestimonial()
    if form.validate_on_submit():
        name = form.name.data
        work = form.work.data
        description = form.description.data
        testimonial = Testimonial(client_name=name, client_work=work, content=description)
        db.session.add(testimonial)
        db.session.commit()
        return redirect(url_for("uploadTestimonial"))

    return render_template('upload_testimonial.html', form=form)


@app.route('/admin/all_images', methods=["GET", "POST"])
@login_required
def all_images():
    form = SimpleForm()
    if form.validate_on_submit():
        postID = request.form.get("id")

        if request.form.get("button1"):
            return redirect(url_for("updateImage", id=postID))

        elif request.form.get("button2"):
            post = Post.query.get(int(postID))
            delete_s3_object(post.image_string, post.image_path)
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for("all_images"))

    path = url_for("static", filename="posts/images")
    page = request.args.get("page", 1, type=int)
    paginate_object = Post.query.paginate(page=int(page), per_page=1)
    return render_template('all_images.html', paginate_object=paginate_object, form=form, path=path)  


@app.route('/admin/all_testimonial', methods=["GET", "POST"])
@login_required
def all_testimonial():
    page = request.args.get("page", 1, type=int)
    paginate_object = Testimonial.query.paginate(page=int(page), per_page=2)

    form = SimpleForm()
    
    if form.validate_on_submit():
        testimonialID = request.form.get("id")

        if request.form.get("button1"):
            return redirect(url_for("updateTestimonial", id=testimonialID))

        elif request.form.get("button2"):
            testimonial = Testimonial.query.get(int(testimonialID))
            db.session.delete(testimonial)
            db.session.commit()

            return redirect(url_for("all_testimonial"))
        elif request.form.get("button3"):
            testimonial = Testimonial.query.get(int(testimonialID))
            if testimonial.state == "inactive":
                testimonial.state = "active"
            else:
                testimonial.state = "inactive"

            db.session.commit()

            return redirect(url_for("all_testimonial"))
            

    return render_template('all_testimonial.html', paginate_object=paginate_object, form=form)  

@app.route('/admin/messages', methods=["GET", "POST"])
@login_required
def messages():
    form = SimpleForm()
    if form.validate_on_submit():
        messageID = request.form.get("id")
        message = Message.query.get(int(messageID))

        if request.form.get("button1"):
            return redirect(url_for("reply", emailID=messageID))

        elif request.form.get("button2"):
            db.session.delete(message)
            db.session.commit()
        
        elif request.form.get("button3"):
            message.state = "read"
            db.session.commit()
        
        return redirect(url_for("messages"))


    page = request.args.get("page", 1, type=int)
    paginate_object = Message.query.filter_by(state="active").paginate(page=int(page), per_page=1)
    return render_template('messages.html', paginate_object=paginate_object, form=form)

@app.route('/admin/done_messages', methods=["GET", "POST"])
@login_required
def done_messages():
    form = SimpleForm()

    if form.validate_on_submit():
        messageID = request.form.get("id")
        message = Message.query.get(int(messageID))

        if request.form.get("button1"):
            message.state = "active"
            db.session.commit()
        
        elif request.form.get("button2"):
            db.session.delete(message)
            db.session.commit()

        return redirect(url_for("done_messages")) if not request.args.get("page") else redirect(url_for("done_messages", page=request.args.get("page")))

    page = request.args.get("page", 1, type=int)
    paginate_object = Message.query.filter_by(state="read").paginate(page=int(page), per_page=6)
    return render_template('done_messages.html', paginate_object=paginate_object, form=form)  


@app.route('/admin/reply/<emailID>', methods=["GET", "POST"])
@login_required
def reply(emailID):
    form = ReplyForm()

    email_id = emailID
    replied_to_email = Message.query.get(email_id)
    if form.validate_on_submit():
        subject = form.subject.data
        email = replied_to_email.email
        content = form.message.data
        
        #send mail
        string = f"""{subject}"""
        msg = MailMessage(string, sender=MAIL_USERNAME, 
        recipients=[email])
        msg.body = f"""
        ردا على الايميل الذي ارسل على:{request.host}



        {content}
        """
        mail.send(msg) 
        return redirect(url_for("messages"))
    return render_template('reply.html', form=form)


@app.route("/image/<id>")
def detail_view(id):
    postId = id
    post = Post.query.get(id)

    path = url_for("static", filename="posts/images")

    # visitors counter system
    response = make_response(render_template("image_details.html", post=post, path=path))
    did_visit = request.cookies.get("did_visit")
    if not did_visit:
        handle_new_visitor(response)
    return response


@app.route('/admin/updateImage/<id>', methods=['GET', 'POST'])
@login_required
def updateImage(id):
    form = UploadImage()
    postID = id
    post = Post.query.get(postID)
    if form.validate_on_submit():
        post.post_title = form.title.data
        post.post_description = form.description.data
        post.category = form.filters.data
        post.project_link = form.url.data

        db.session.commit()

        return redirect(url_for('updateImage', id=postID))
    elif request.method == "GET":
        form.title.data = post.post_title
        form.description.data = post.post_description
        form.filters.data = post.category
        form.url.data = post.project_link

    path = url_for("static", filename="posts/images")

    return render_template('update_image.html', form=form, post=post, path=path)


@app.route('/admin/updateTestimonial/<id>', methods=['GET', 'POST'])
@login_required
def updateTestimonial(id):
    form = UploadTestimonial()
    testimonialID = id
    testimonial = Testimonial.query.get(testimonialID)
    if form.validate_on_submit():
        testimonial.client_name = form.name.data
        testimonial.client_work = form.work.data
        testimonial.content = form.description.data

        db.session.commit()

        return redirect(url_for('updateTestimonial', id=testimonialID))
    elif request.method == "GET":
        form.name.data = testimonial.client_name
        form.work.data = testimonial.client_work
        form.description.data = testimonial.content


    return render_template('update_testimonial.html', form=form, testimonial=testimonial)


@app.route('/admin/list_of_admins', methods=["GET", "POST"])
@login_required
def list_of_admins():
    if not current_user.role == "MasterAdmin":
        return redirect(url_for("admin"))
    users = User.query.all()
    form = SimpleForm()
    if form.validate_on_submit():
        if request.form.get("button1"):
            id = request.form.get("id")
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("list_of_admins"))

        
    return render_template('list_of_admins.html', users=users, form=form)  

@app.route('/admin/register_admin', methods=["GET", "POST"])
@login_required
def register_admin():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        full_name = form.full_name.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        permission_level = form.permission.data
        
        user = User(username=username, full_name=full_name, email=email, password=password,
        role=permission_level)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("admin"))
    else:
        form.username.data = ""
        form.full_name.data = ""
        form.email.data = ""
        form.password.data = ""
    return render_template('register_admin.html', form=form)  


@app.route('/admin/edit_admin/<adminID>', methods=["GET", "POST"])
@login_required
def edit_admin(adminID):
    admin = User.query.get(adminID)
    if current_user.role != "MasterAdmin":
        return redirect(url_for("admin"))
    else:
        if current_user.id != admin.id and admin.role == "MasterAdmin":
            return redirect(url_for("list_of_admins"))

    form = UserForm()
    if form.validate_on_submit():
        admin.username = form.username.data
        admin.full_name = form.full_name.data
        admin.email = form.email.data
        admin.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        if current_user.role == "MasterAdmin":
            admin.role = form.permission.data
        else:
            admin.role = admin.role
    
        db.session.commit()

        return redirect(url_for("admin"))
    else:
        form.username.data = admin.username
        form.full_name.data = admin.full_name
        form.email.data = admin.email

    return render_template('edit_admin.html', admin=admin, form=form)  

    