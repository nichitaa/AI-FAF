import cv2
import csv
import os
import ast
from second import get_face_coords, plot_rectangles
from third import is_grey_scale, is_head_proportional, is_portrait_or_square, get_eyes_coords


def is_valid_image(path, verbose=False, should_plot=False):
    original = cv2.imread(path)

    verbose_print(f'\nChecking {path} image...', verbose)

    if is_grey_scale(original):
        verbose_print('[RGB] ERROR: image is grayscale', verbose)
        return False
    else:
        verbose_print('[RGB] OK', verbose)

    if not is_portrait_or_square(original):
        verbose_print('[PORTRAIT] ERROR: image is not portrait orientation or square', verbose)
        return False
    else:
        verbose_print('[PORTRAIT] OK', verbose)

    eyes_coords = get_eyes_coords(original)
    if eyes_coords is False:
        verbose_print('[EYES] ERROR: could not detect subject eyes', verbose)
        return False
    else:
        verbose_print('[EYES] OK', verbose)
        maybe_plot_rectangles(original, eyes_coords, should_plot)

    face_coords = get_face_coords(original)
    if face_coords is None:
        verbose_print('[FACE] ERROR: could not detect exactly one face', verbose)
        return False
    else:
        verbose_print('[FACE] OK', verbose)
        maybe_plot_rectangles(original, [face_coords], should_plot)

    head_coords = is_head_proportional(original)
    if head_coords is False:
        verbose_print('[HEAD] ERROR: failed head proportion threshold check', verbose)
        return False
    else:
        verbose_print('[HEAD] OK', verbose)
        maybe_plot_rectangles(original, head_coords, should_plot)

    return True


def verbose_print(value, verbose=True):
    if verbose:
        print(value)


def maybe_plot_rectangles(img, rectangles, flag=True):
    if flag:
        plot_rectangles(img, rectangles)


def get_parsed_csv(path):
    file = open(path, 'r')
    csv_data = list(csv.DictReader(file, delimiter=","))
    file.close()
    return csv_data


def get_accuracy(csv_path, images_directory_path, verbose=False, should_plot=False):
    csv_data = get_parsed_csv(csv_path)
    files = os.listdir(images_directory_path)

    correct = 0
    wrong = 0
    total = len(csv_data)

    for file_name in files:
        path = f'{images_directory_path}/{file_name}'
        valid = is_valid_image(path, verbose, should_plot)
        csv_result = next((item for item in csv_data if item["new_path"] == path), None)
        if csv_result is not None:
            label = csv_result['label']
            if ast.literal_eval(label) == valid:
                verbose_print(f'[RESULT-SUCCESS] for {path}', verbose)
                correct += 1
            else:
                verbose_print(f'[RESULT-ERROR] for {path}', verbose)
                wrong += 1

    verbose_print(f'\ntotal={total}, correct={correct}, wrong={wrong}', verbose)
    return correct / total
