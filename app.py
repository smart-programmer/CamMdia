from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/images', methods=['GET', 'POST'])
def images():
    return render_template('image_gallery.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/admin/uploadImage', methods=['GET', 'POST'])
def uploadImage():
    return render_template('upload_image.html')

@app.route('/admin/messages')
def messages():
    return render_template('messages.html')

@app.route('/admin/deleted_messages')
def deleted_messages():
    return render_template('deleted_messages.html')

@app.route('/admin/done_messages')
def done_messages():
    return render_template('done_messages.html')  

if __name__ == '__main__':
    app.run(debug=True)