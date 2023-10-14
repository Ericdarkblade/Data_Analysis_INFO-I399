import numpy as np
import matplotlib.pyplot as plt

from get_coordinates_in_image import get_click_coordinates

source_image = input("Enter the CSV source image file name: ")
target_image = input("Enter the CSV target image file name: ")
cut_size_height = input('please enter the height of the pixels to cut: ')
cut_size_width = input('please input the width of the pixels to cut: ')
pyramid = float(input("please tell me the number of level for the pyramid: "))


def apply_gaussian_filter(image):

    kernel = np.array([[1, 4, 7, 4, 1],              # this filter is correct   :) yay i did one part right
                       [4, 16, 26, 16, 4],
                       # define a 5x5 Gaussian kernel
                       [7, 26, 41, 26, 7],
                       [4, 16, 26, 16, 4],
                       [1, 4, 7, 4, 1]]) / 273.0

    filtered_image = filter(image, kernel)

    return filtered_image


def mask_target_image():
    # yeah i dont know what the 100s are this is just what im getting from the example slides, is it the size?
    img = get_click_coordinates

    mask = np.ones(img.shape)
    x, y, size = 50, 50, 20                   # i dont know what the 50 50 20 are
    mask[y-size//2:y+size//2, x-size//2:x+size//2] = 0

    return float(mask)


def mask_source_image():

    # should this be the actual image i am going ot use or should  i put that as a variable in the parenthesis for when i use it later in the main function
    img = np.random.rand(100, 100)

    mask = np.zeros(img.shape)
    x, y, size = 50, 50, 20
    mask[y-size//2:y+size//2, x-size//2:x+size//2] = 1

    return mask


def subsampled_image(image):

    image = np.random.rand(100, 100)
    subsampled = image[::2, ::2]

    return subsampled


def upsample(image):
    height, width = image.shape
    upsampled = np.zeros((height*2, width*2))
    upsampled[::2, ::2] = image

    image = np.random.rand(100, 100)

    upsampled_image = upsample(subsampled_image())
    plt.imshow(upsampled_image)
    plt.show()

    return upsample


def make_gray():
    # im confused as to what te 100, 100 values are
    image = np.random.rand(100, 100, 3)
    # Example random RGB image                     # i also dont know if it works
    gray_image = np.dot(image[..., :3],
                        [0.2989, 0.5870, 0.1140])
    plt.imshow(gray_image, cmap='gray')
    plt.show()


def pyramid_guy(source_image):
    for i in range(pyramid):
        next_image = apply_gaussian_filter(source_image[i])
        next_image = subsampled_image(next_image)

        mask_source = subsampled_image(mask_source_image(source_image))

        # at this point, in loop 1, my_images = [image.jpg,next_image]
        source_image.append(next_image)

        large_image = upsample(next_image)
        large_image = apply_gaussian_filter(large_image)
        large_image_gaussian = apply_gaussian_filter(next_image)

        laplacian_image = source_image-large_image_gaussian

        laplacian_image.append(laplacian_image)

        masked_image = mask_source*laplacian_image

        multiplied_array_source = np.array(masked_image*laplacian_image)

    return multiplied_array_source


def pyramid_guy(target_image):
    for i in range(pyramid):
        next_image = apply_gaussian_filter(target_image[i])
        next_image = subsampled_image(next_image)

        mask_target = subsampled_image(mask_target_image(target_image))

        # at this point, in loop 1, my_images = [image.jpg,next_image]
        target_image.append(next_image)

        large_image = upsample(next_image)
        large_image = apply_gaussian_filter(large_image)
        large_image_gaussian = apply_gaussian_filter(next_image)
        laplacian_image = source_image-large_image_gaussian

        laplacian_image.append(laplacian_image)

        masked_image = mask_target*laplacian_image

        multiplied_array_target = np.array(masked_image*laplacian_image)

    return multiplied_array_target


def image_to_array(image_path):

    return plt.imread(image_path)


img_array = image_to_array(source_image)
# Get the x and y coordinates from a mouse click on the image


def onclick(event):
    global x, y
    x, y = event.xdata, event.ydata
    plt.close()


fig = plt.figure()

plt.imshow(img)
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
print(f"You clicked on x = {x}, y = {y}")

x, y = get_click_coordinates(img_array)
# Display the image with a red circle around the clicked point

plt.imshow(img_array, cmap='gray')
plt.scatter(x, y, c='red', s=100, marker='o', edgecolors='r')
plt.show()
