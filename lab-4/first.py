import cv2
import matplotlib.pyplot as plt
import numpy as np


def blur(img, kernel_size=(11, 11)):
    return cv2.GaussianBlur(img, kernel_size, 0)


# https://www.codespeedy.com/how-to-sharpen-an-image-in-python-using-opencv/
def sharpen(img):
    sharpen_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(img, -1, sharpen_filter)


def to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def plot(original, modified):
    original = to_rgb(original)
    modified = to_rgb(modified)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.imshow(original)
    ax1.set_title('Original')
    ax2.imshow(modified)
    ax2.set_title('Modified')
    plt.show()

# 1
# path = 'test_images/41F890.jpg'
# original = cv2.imread(path)
# blured = blur(original)
# sharpened = sharpen(original)
#
# plot(original, blured)
# plot(original, sharpened)
