import numpy as np
import matplotlib.pyplot as plt
# import get_coordinates_in_image as gcii #would not properly import and work


def onclick(event):
    global x_click, y_click
    x_click, y_click = event.xdata, event.ydata
    plt.close()


def get_click_coordinates(gray_image):

    plt.imshow(gray_image, cmap='gray')
    cid = plt.connect('button_press_event', onclick)
    plt.show()
    plt.disconnect(cid)

    x = int(x_click)
    y = int(y_click)
    return (x, y)


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


def apply_gaussian_filter(image: np.ndarray[np.uint8]):

    kernel = np.array([[1, 4, 7, 4, 1],     # define a 5x5 Gaussian kernel
                       [4, 16, 26, 16, 4],
                       [7, 26, 41, 26, 7],  # this works
                       [4, 16, 26, 16, 4],
                       [1, 4, 7, 4, 1]]) / 273.0

    filtered_image = filter(image, kernel)
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
