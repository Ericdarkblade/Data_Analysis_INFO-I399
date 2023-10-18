import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
from get_coordinates_in_image import get_click_coordinates

# -> (np.ndarray[np.uint8], np.ndarray[np.uint8], int, int, int):


def get_input_and_arrays():
    source_array: np.ndarray
    target_array: np.ndarray
    while True:
        source_img_path: str = input(
            'Please Enter Source Image Path:\n').strip()
        target_img_path: str = input(
            'Please Enter Target Image Path:\n').strip()
        try:
            source_array = mplimg.imread(source_img_path).astype(np.uint8)
            target_array = mplimg.imread(target_img_path).astype(np.uint8)
            break
        except FileNotFoundError:
            print('\
            One of the file paths entered does not exist\n\
            or was entered incorrectly.\n\
            Please try again.')
            continue
        break
    selection_width: int  # not working
    selection_height: int  # not working
    pyramid_levels: int  # not working
    # while True:
    #     try:
    #         selection_width = int(
    #             input('Please Enter Selection Width:\n').strip())
    #         selection_height = int(
    #             input('Please Enter Selection Height:\n').strip())
    #         pyramid_levels = int(
    #             input('Please Enter Pyramid Levels:\n').strip())
    #         break
    #     except ValueError:  # Catches Letters as ints
    #         print(
    #             'A non numerical character was entered into one of the previous fields.\nPlease try again.')
    #         continue
    #     if selection_width <= 0 or selection_height <= 0 or pyramid_levels <= 0:
    #         print('\nInput values must be >0.\nPlease try again.\n')
    #         continue
    #     else:
    #         break
    size_check = (selection_width, selection_height, pyramid_levels)
    while size_check == True:
        if selection_width <= 0 or selection_height <= 0 or pyramid_levels <= 0:
            print('\nInput values must be >0.\nPlease try again.\n')
        else:
            size_check = False
    # input_flag=True
    # while input_flag:
    #     try:
    #         selection_width = int(
    #             input('Please Enter Selection Width:\n').strip())
    #         selection_height = int(
    #             input('Please Enter Selection Height:\n').strip())
    #         pyramid_levels = int(
    #             input('Please Enter Pyramid Levels:\n').strip())
    #         if selection_width <= 0 or selection_height <= 0 or pyramid_levels <= 0:
    #             print('\nInput values must be >0.\nPlease try again.\n')
    #             continue
    #         else:
    #             input_flag=False  # This break is added inside the "else" block.
    #     except ValueError:  # Catches Letters as ints
    #         print('A non-numerical character was entered into one of the previous fields.\nPlease try again.')
    #         continue
    user_input = [source_array,
                  target_array,
                  selection_width,
                  selection_height,
                  pyramid_levels]
    return user_input


def apply_gaussian_filter(image):
    kernel = np.array([[1, 4, 7, 4, 1],     # define a 5x5 Gaussian kernel
                       [4, 16, 26, 16, 4],
                       [7, 26, 41, 26, 7],  # this works
                       [4, 16, 26, 16, 4],
                       [1, 4, 7, 4, 1]]) / 273.0
    array = np.pad(array, (2, 2), 'constant', constant_values=(0, 0))
    r, c = array.shape  # rows,columns
    output_array = np.zeros(r, c)
    filtered_image = filter(image, kernel)  # probably needs to be changed
    return filtered_image


def mask_target_image(x_target, y_target, size, target_array):
    img = target_array
    mask = np.ones(img.shape)
    mask[y_target-size//2:y_target+size//2,
         x_target-size//2:x_target+size//2] = 0
    return float(mask)


def mask_source_image(x_source, y_source, size, source_array):
    img = source_array
    mask = np.zeros(img.shape)
    mask[y_source-size//2, y_source+size//2,
         x_source-size//2:x_source+size//2] = 1
    # source_array[y_source-size//2,y_source+size//2, x_source-size//2:x_source+size//2]= target_array[y_source-size//2,y_source+size//2, x_source-size//2:x_source+size//2]
    return mask


def subsampled_image(image):
    subsampled = image[::2, ::2]                    # ask if this is correct
    return subsampled


def upsample(image):
    height, width = image.shape
    upsampled = np.zeros((height*2, width*2))
    upsampled[::2, ::2] = image
    upsampled_image = upsample(subsampled_image())
    plt.imshow(upsampled_image)
    plt.show()
    return upsample


def make_gray(image):
    gray_image = np.dot(image[..., :3],                       # this works
                        [0.2989, 0.5870, 0.1140])
    plt.imshow(gray_image, cmap='gray')
    plt.show()


def pyramid_source(source_array, pyramid_levels):
    # pyramid_levels=get_input_and_arrays(4)
    # source_array=get_input_and_arrays(1)
    pyramid_levels = get_input_and_arrays()
    source_array = get_input_and_arrays()
    print(pyramid_levels, source_array)
    for i in range(pyramid_levels):
        next_image = apply_gaussian_filter(source_array[i])
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
    # pyramid_levels=get_input_and_arrays[4]
    # target_array=get_input_and_arrays[0]
    pyramid_levels = get_input_and_arrays()
    source_array = get_input_and_arrays()
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
    source_array = get_inputs[0]
    target_array = get_inputs[1]
    selection_area = get_inputs[3]
    pyramid_levels = get_inputs[4]
    source_location = get_click_coordinates(source_array)
    x_source = source_location[0]
    y_source = source_location[1]
    target_location = get_click_coordinates(target_array)
    x_target = target_location[0]
    y_target = target_location[1]
    gray_source = make_gray(source_array)
    gray_target = make_gray(target_array)
    pyramid_source_array = pyramid_source(gray_source, pyramid_levels)
    pyramid_target_array = pyramid_target(gray_target, pyramid_levels)
    source_array[y_source-size//2, y_source+size//2, x_source-size//2:x_source+size //
                 2] = target_array[y_source-size//2, y_source+size//2, x_source-size//2:x_source+size//2]
    # define size for above
    plt.imshow(source_array)


if __name__ == '__main__':
    main()
