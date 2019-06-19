import cv2
import os
import glob
import platform
import sys
from send2trash import send2trash
from natsort import natsorted, ns


def image_viewer(__self__, start_index):
	images = get_all_files(__self__)
	size_of_list = len(images)
	i = 0
	if start_index != '': 
		if (start_index >= 0 and start_index <= size_of_list):
			show_image(images[start_index])
			i = start_index
	else:
		show_image(images[i])
	key = 0
	while key != 27:
		key = cv2.waitKey()
		print(key)
		if key == IMAGE_PREVIOUS and i != 0:  # comma char
			i-=1
		elif key == IMAGE_NEXT and i < size_of_list:  # dot char
			i+=1
		elif key == IMAGE_FORWARD:
			if i + 10 < size_of_list:
				i+=10
			else:
				show_image(images[size_of_list])
		elif key == IMAGE_BACKWARD:
			if i - 10 > 0:
				i-=10
			else:
				show_image(images[0])
		elif key == IMAGE_DELETE:  # d - deletes file
			send2trash(images[i])
			images.pop(i)
			size_of_list = len(images)
			if i > size_of_list:
				i = size_of_list
			# elif i != size_of_list:
			# 	i+=1

		show_image(images[i])


	cv2.destroyAllWindows()
	exit()


def get_all_files(__self__):
	files = glob.glob(__self__ + "/*.*")
	files_sorted = natsorted(files, key=lambda y: y.lower())
	return [f for f in files_sorted]


def show_image(__self__):
	frame = cv2.imread(__self__, 1)
	cv2.imshow('ImageViewer', frame)
	cv2.setWindowProperty('ImageViewer', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_OPENGL)
	cv2.setWindowTitle('ImageViewer', __self__)


if __name__ == "__main__":
	# Shortcuts bindings - DEFAULT: WSL (Windows System for Linux)
	IMAGE_NEXT = 46 # .
	IMAGE_PREVIOUS = 44 # ,
	IMAGE_FORWARD = 47  # /
	IMAGE_BACKWARD = 59 # ;
	IMAGE_DELETE = 100 # d

	if os.path.isdir(sys.argv[1]):
		if len(sys.argv) == 3:
			image_viewer(sys.argv[1], int(sys.argv[2]))
		else:
			image_viewer(sys.argv[1], '')
	else:
		raise Exception("Invalid path")
