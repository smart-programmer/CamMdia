import os
import secrets
from WEBSITE import app
from PIL import Image
import datetime
import boto3


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

	return image_filename, image_path

	#return None


def save_image_online(image_file, path):
	if os.environ.get("online"):	
		# s3_client = boto3.client('s3')
		s3_resource = boto3.resource('s3')
		my_bucket = s3_resource.Bucket("cam-media-static-files")

		image_filename, local_path = save_image(image_file, path)

		my_bucket.upload_file(Filename=local_path, Key=image_filename)

		os.remove(local_path)

		s3_path = "https://cam-media-static-files.s3.amazonaws.com/" + image_filename
		
		return image_filename, s3_path


	else:
		save_image(image_file, path)



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