import cv2


def is_grey_scale(img):
    # must have 3 dimensions (height, width, and color channels)
    if len(img.shape) != 3:
        return False
    # must have 3 color channels (red, green, and blue)
    if img.shape[2] != 3:
        return False
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # for each pixel get the values of red, green, and blue
            b, g, r = img[i, j]
            # image is not grayscale if those values are different from each-other
            if r != g != b:
                return False
    return True


def is_portrait_or_square(img):
    height, width = img.shape[:2]
    return height >= width


def get_eyes_coords(img):
    # 476435, D87D5F, E2BD04
    eye_cascade = cv2.CascadeClassifier("./haar/eye.xml")
    eyes = eye_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=7)

    if len(eyes) >= 2:
        eye1 = eyes[0]
        eye2 = eyes[1]
        eye1_coord = (eye1[0] + eye1[2] // 2, eye1[1] + eye1[3] // 2)
        eye2_coord = (eye2[0] + eye2[2] // 2, eye2[1] + eye2[3] // 2)
        if abs(eye1_coord[1] - eye2_coord[1]) <= 5:
            return eyes
    return False


def is_head_proportional(img):
    head_cascade = cv2.CascadeClassifier("./haar/frontal_face.xml")
    head_rect = head_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=7)

    if len(head_rect) == 1:
        head_x, head_y, head_width, head_height = head_rect[0]

        head_area = head_width * head_height
        image_area = img.shape[0] * img.shape[1]

        head_ratio = (head_area / image_area)

        if 0.2 <= head_ratio <= 0.5:
            return head_rect
    return False
