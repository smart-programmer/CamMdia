import os
from flask import url_for
import secrets
from WEBSITE import app
from PIL import Image
import datetime
import boto3


def save_image_locally(image_file, path):
	
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

	if os.environ.get("online"):
		return image_filename, image_path
	else:
		return image_filename, url_for("static", filename="posts/images/"+ image_filename) # a new url for the local image is returned here because the images_path variable has a url relative to the whole os which is ok when we save the image but when displaying the image on the server we need a path relative to the server not the os which is what url_for returns



def save_image(image_file, path):
	if os.environ.get("online"):	
		# connect to s3
		# s3_client = boto3.client('s3')
		s3_resource = boto3.resource('s3')
		my_bucket = s3_resource.Bucket("cam-media-static-files")

		# save image locally
		image_filename, local_path = save_image_locally(image_file, path)

		# upload image to s3 
		my_bucket.upload_file(Filename=local_path, Key=image_filename)

		# remove image from local machine
		os.remove(local_path)

		s3_path = "https://s3-us-west-2.amazonaws.com/cam-media-static-files/" + image_filename # or: https://cam-media-static-files.s3.amazonaws.com/
		
		return image_filename, s3_path


	else:
		return save_image_locally(image_file, path)


def delete_s3_object(object_name, object_path):
	if os.environ.get("online"):
		s3_resource = boto3.resource('s3')
		s3_resource.Object('cam-media-static-files', object_name).delete()
	else:
		local_image_path = app.root_path + object_path # the function os.path.join didn't work here, NOTE: see the comment in the "save_image_locally" function to know why we need a new image path relative to the os to delete the image
		os.remove(local_image_path)

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