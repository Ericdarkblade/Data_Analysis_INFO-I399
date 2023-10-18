import matplotlib.pyplot as plt


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


if __name__ == '__main__':
    import numpy as np
    grey_test = plt.imread(
        "C:\\Users\\ezmos\\OneDrive - Indiana University\\My Courses\\Fall 2023\\INFO-I 399\\Anna Help\\Final Assignment\\imgs\\clark_kent.jpg").astype(np.uint8)
    print(get_click_coordinates(grey_test))
