
"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    CCCCCCCCCCCCCCCCCCCCCCCCCCC

Assignment Information
    Assignment:     e.g. Team project 01
    Author:          Anna-Lizette Walker, walke744@purdue.edu,Shandi Carlisle, carliss@purdue.edu,Ava Egnaczyk, aegnaczy@purdue.edu,Camille Morin, morin13@purdue.edu 
    Team ID:        LC2 - 02

Contributor:    Name, login@purdue [repeat for each]
    My contributor(s) helped me:
    [  Anna-Lizette Walker, walke744@purdue.edu,Shandi Carlisle, carliss@purdue.edu,Ava Egnaczyk, aegnaczy@purdue.edu,Camille Morin, morin13@purdue.edu ] understand the assignment expectations without
        telling me how they will approach it.
    [ Anna-Lizette Walker, walke744@purdue.edu,Shandi Carlisle, carliss@purdue.edu,Ava Egnaczyk, aegnaczy@purdue.edu,Camille Morin, morin13@purdue.edu  ] understand different ways to think about a solution
        without helping me plan my solution.
    [ Anna-Lizette Walker, walke744@purdue.edu,Shandi Carlisle, carliss@purdue.edu,Ava Egnaczyk, aegnaczy@purdue.edu,Camille Morin, morin13@purdue.edu  ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
from get_coordinates_in_image import get_click_coordinates 



def get_input_and_arrays() -> (np.ndarray[np.uint8], np.ndarray[np.uint8], int, int, int):
    '''
    Returns:
    (source_array,
    target_array,
    selection_length,
    pyramid_levels)
    '''
    source_array: np.ndarray
    target_array: np.ndarray
    while True:
        source_img_path: str = input(
            'Please Enter Source Image Path:\n').strip()
        target_img_path: str = input(
            'Please Enter Target Image Path:\n').strip()
        try:
            source_array = plt.imread(source_img_path).astype(np.uint8)
            target_array = plt.imread(target_img_path).astype(np.uint8)
        except FileNotFoundError:
            print('\
            One of the file paths entered does not exist\n\
            or was entered incorrectly.\n\
            Please try again.')
            continue
        break
    selection_length: int
    pyramid_levels: int
    while True:
        try:
            selection_length = int(
                input('Please Enter Selection Length (Square Length):\n').strip())
            pyramid_levels = int(
                input('Please Enter Pyramid Levels:\n').strip())
        except ValueError:  # Catches Letters as ints
            print(
                'A non numerical character was entered into one of the previous fields.\nPlease try again.')
            continue
        if selection_length <= 0 or pyramid_levels <= 0:
            print('\nInput values must be >0.\nPlease try again.\n')
            continue
        else:
            break

    user_input = (source_array,
                  target_array,
                  selection_length,
                  pyramid_levels)

    return user_input


def apply_gaussian_filter(image: np.ndarray):  # Recieved Help from chatGPT
    # Define a 5x5 Gaussian kernel
    gaussian_filter = np.array([[1, 4, 7, 4, 1],
                                [4, 16, 26, 16, 4],
                                [7, 26, 41, 26, 7],
                                [4, 16, 26, 16, 4],
                                [1, 4, 7, 4, 1]]) / 273.0

    # Create an empty output image
    filtered_image = np.zeros_like(image, dtype=np.float64)

    # Get the dimensions of the input image
    height, width = image.shape

    # Apply the Gaussian filter to the image
    for i in range(2, height - 2):
        for j in range(2, width - 2):
            # Extract a 5x5 neighborhood from the input image
            neighborhood = image[i - 2:i + 3, j - 2:j + 3]

            # Convolve the neighborhood with the Gaussian kernel
            filtered_pixel = np.sum(neighborhood * gaussian_filter)

            # Update the corresponding pixel in the output image
            filtered_image[i, j] = filtered_pixel

    # Clip the pixel values to the [0, 255] range and convert to uint8
    filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)

    return filtered_image




def mask_target_image(x_target, y_target, size, target_array):

    mask = np.ones(target_array.shape)
    mask[y_target-size//2:y_target+size//2,
         x_target-size//2:x_target+size//2] = 0

    return mask


def mask_source_image(x_source, y_source, size, source_array):

    mask = np.zeros(source_array.shape)

    mask[y_source-size//2, y_source+size//2,
         x_source-size//2:x_source+size//2] = 1

    return mask


def subsampled_image(image: np.ndarray[np.uint8]):

    subsampled = image[::2, ::2]                    # ask if this is correct

    return subsampled


def upsample(image: np.ndarray[np.uint8]):
    height, width = image.shape
    upsampled = np.zeros((height*2, width*2))
    upsampled[::2, ::2] = image

    # upsampled_image = upsample(subsampled_image())
    # plt.imshow(upsampled_image)
    # plt.show()

    return upsample


def make_gray(image: np.ndarray[np.uint8]):
    gray_image = np.dot(image[..., :3],                       # this works
                        [0.2989, 0.5870, 0.1140])
    return gray_image


def pyramid_source(source_array, pyramid_levels):

    for i in range(pyramid_levels):
        next_image = apply_gaussian_filter(source_array)
        next_image = subsampled_image(next_image)

        mask_source = subsampled_image(mask_source_image(source_array))

        # at this point, in loop 1, my_images = [image.jpg,next_image]
        source_array.append(next_image)

        large_image = upsample(next_image)
        large_image = apply_gaussian_filter(large_image)
        large_image_gaussian = apply_gaussian_filter(next_image)

        laplacian_image = source_array-large_image_gaussian

        laplacian_image.append(laplacian_image)

        masked_image = mask_source*laplacian_image

        multiplied_array_source = np.array(masked_image*laplacian_image)

    return multiplied_array_source


def pyramid_target(target_array, pyramid_levels):
    pyramid_levels = get_input_and_arrays[4]
    target_array = get_input_and_arrays[0]

    for i in range(pyramid_levels):
        next_image = apply_gaussian_filter(target_array[i])
        next_image = subsampled_image(next_image)

        mask_target = subsampled_image(mask_target_image(target_array))

        # at this point, in loop 1, my_images = [image.jpg,next_image]
        target_array.append(next_image)

        large_image = upsample(next_image)
        large_image = apply_gaussian_filter(large_image)
        large_image_gaussian = apply_gaussian_filter(next_image)

        laplacian_image = target_array-large_image_gaussian

        laplacian_image.append(laplacian_image)

        masked_image = mask_target*laplacian_image

        multiplied_array_target = np.array(masked_image*laplacian_image)

    return multiplied_array_target


def main():

    get_inputs = get_input_and_arrays()

    # Unpacking User Input
    source_array = get_inputs[0]
    target_array = get_inputs[1]
    selection_length = get_inputs[2]
    pyramid_levels = get_inputs[3]

    # Greyscaling Images
    gray_source = make_gray(source_array)
    gray_target = make_gray(target_array)

    # Select Positions
    source_location = get_click_coordinates(gray_source)
    x_source = source_location[0]
    y_source = source_location[1]
    target_location = get_click_coordinates(gray_target)
    x_target = target_location[0]
    y_target = target_location[1]

    # Mask Images
    source_mask = mask_source_image(
        x_source, y_source, selection_length, source_array)
    target_mask = mask_target_image(
        x_target, y_target, selection_length, target_array)

    # Apply Gausian Blur/Filter
    source_mask_filter = apply_gaussian_filter(source_mask)
    target_mask_filter = apply_gaussian_filter(target_mask)

    # Blur & Subsample Image
    pyramid_source_array = pyramid_source(source_mask_filter, pyramid_levels)
    pyramid_target_array = pyramid_target(target_mask_filter, pyramid_levels)

    plt.imshow(pyramid_source_array)
    plt.imshow(pyramid_target_array)


if __name__ == '__main__':

    main()
