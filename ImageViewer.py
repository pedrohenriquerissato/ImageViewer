import cv2
import os
import glob
import platform
import sys
from send2trash import send2trash
from natsort import natsorted, ns

def image_viewer(__self__, start_index):
    """Process user entries and prepare to display specific images"""
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
        if key == IMAGE_PREVIOUS and i != 0:  
            i -= 1
        elif key == IMAGE_NEXT and i < size_of_list:  
            i += 1
        elif key == IMAGE_FORWARD:
            if i + 10 < size_of_list:
                i += 10
            else:
                show_image(images[size_of_list])
        elif key == IMAGE_BACKWARD:
            if i - 10 > 0:
                i -= 10
            else:
                show_image(images[0])
        elif key == IMAGE_DELETE:
            send2trash(images[i])
            images.pop(i)
            size_of_list = len(images)
            if i > size_of_list:
                i = size_of_list

        show_image(images[i])

    cv2.destroyAllWindows()
    exit()


def get_all_files(__self__):
    """Get all images files from supported filetypes.

    Allowed filetypes:
    bmp, dib, exr, hdr, jp2, jpe, jpeg, jpg, pbm, pfm, pgm, pic, png, pnm, ppm, 
    pxm, ras, sr, tif, tiff, webp
    """
    filetypes = ["*.bmp", "*.dib", "*.jpeg", "*.jpg", "*.jpe", "*.jp2", "*.png", 
    "*.webp", "*.pbm", "*.pgm", "*.ppm", "*.pxm", "*.pnm", "*.pfm", "*.sr", 
    "*.ras", "*.tiff", "*.tif", "*.exr", "*.hdr", "*.pic"]

    files = []
    for type in filetypes:
        files.extend(glob.glob(__self__ + "/" + type))

    files_sorted = natsorted(files, key=lambda y: y.lower())
    return [f for f in files_sorted]


def show_image(__self__):
    """Creates the window and displays an image file"""
    name = 'ImageViewer'
    frame = cv2.imread(__self__, 1)
    cv2.namedWindow(name, cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_KEEPRATIO)
    cv2.setWindowTitle(name, __self__)
    cv2.imshow(name, frame)


if __name__ == "__main__":
    # Shortcuts bindings - DEFAULT: WSL (Windows System for Linux)
    IMAGE_NEXT = 46  # .
    IMAGE_PREVIOUS = 44  # ,
    IMAGE_FORWARD = 47  # /
    IMAGE_BACKWARD = 59  # ;
    IMAGE_DELETE = 100  # d

    if os.path.isdir(sys.argv[1]):
        if len(sys.argv) == 3:
            image_viewer(sys.argv[1], int(sys.argv[2]))
        else:
            image_viewer(sys.argv[1], '')
    else:
        raise Exception("Invalid path")
