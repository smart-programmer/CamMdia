import os
import secrets
from WEBSITE import app
from PIL import Image


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


