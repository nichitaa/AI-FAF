import cv2
import matplotlib.pyplot as plt
from first import to_rgb

face_cascade = cv2.CascadeClassifier('./haar/face.xml')


def get_face_coords(img):
    # to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # find faces coordinates
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 1:
        return faces[0]

    return None


def plot_rectangles(img, rectangles):
    rgb = to_rgb(img)

    for [x, y, w, h] in rectangles:
        cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), thickness=1)

    plt.imshow(rgb)
    plt.show()

# 2
# path = 'test_images/41F890.jpg'
# original = cv2.imread(path)
# rect = get_face_coords(original)
# if rect is None:
#     print(f'Invalid image (could not find exactly one face)')
# else:
#     print(f'Face coordinates are: {rect}')
#     plot_rectangles(original, [rect])
