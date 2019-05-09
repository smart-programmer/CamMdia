import os
import secrets
from WEBSITE import app
from PIL import Image
import datetime


def save_image(image_file, path):

	#if image_file:
	
	# create a random name
	random_hex = secrets.token_hex(20)

	# get file extention via os module
	_, extention = os.path.splitext(image_file.filename)

	# create image name
	image_filename = random_hex + extention

	# specify image path
	image_path = os.path.join(app.root_path, path, image_filename)

	# resize image with pillow and save it 
	new_size = (600, 600)
	image = Image.open(image_file)
	image.thumbnail(new_size)
	image.save(image_path)

	## image_file.save(image_path)

	return image_filename

	#return None


def handle_new_visitor(response):
	expire_date = datetime.datetime.now()
	expire_date = expire_date + datetime.timedelta(days=100000)
	response.set_cookie("did_visit", "True", expires=expire_date)
	increase_visitors_counter()

def get_visitors_file():
	return os.getcwd()+"/WEBSITE/static/visitors.txt"#url_for("static", filename="visitors.txt")

def increase_visitors_counter():
	with open(get_visitors_file(), "r+") as visitors_file:
		number = int(visitors_file.read())
		number += 1
		visitors_file.truncate(0)
		visitors_file.seek(0)
		visitors_file.write(str(number))