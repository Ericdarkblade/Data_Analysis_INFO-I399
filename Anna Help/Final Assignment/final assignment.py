import numpy as np
import matplotlib.pyplot as plt
import get_coordinates_in_image as handout


def apply_gaussian_filter(image):
    # this filter is correct   :) yay i did one part right
    kernel = np.array([[1, 4, 7, 4, 1],
                       [4, 16, 26, 16, 4],
                       # define a 5x5 Gaussian kernel
                       [7, 26, 41, 26, 7],
                       [4, 16, 26, 16, 4],
                       [1, 4, 7, 4, 1]]) / 273.0

    filtered_image = filter(image, kernel)
    return filtered_image


def get_user_input() -> None:
    
    
    while True:
        source_img_path: str = input(
            'Please Enter Source Image Path:\n').strip()
        target_img_path: str = input(
            'Please Enter Target Image Path:\n').strip()
        









    selection_width: int
    selection_height: int
    pyramid_levels: int
    while True:
        try:
            selection_width = int(
                input('Please Enter Selection Width:\n').strip())
            selection_height = int(
                input('Please Enter Selection Height:\n').strip())
            pyramid_levels = int(
                input('Please Enter Pyramid Levels:\n').strip())
        except ValueError:  # Catches Letters as ints
            print(
                'A non numerical character was entered into one of the previous fields.\nPlease try again.')

        if selection_width or selection_height or pyramid_levels <= 0:
            print('Input values must be >0.\nPlease try again.')
            continue
        else:
            break

        np.asarray(source_img_path)
