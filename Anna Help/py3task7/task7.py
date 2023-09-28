# %%
import numpy as np

# %%


def load_data():
    data = np.loadtxt('CRNH0203-2022-IN_Bedford_5_WNW.txt',
                      usecols=(1, 2, 10, 11))

    return data


# This function will save an array as a csv file named "output.csv"
# in your current working directory.
# Call this funciton at the end of your main program to save your final
# array as a csv.
def export_data(array):
    np.savetxt('output.csv', array, delimiter=',')


# %%
data = load_data()
date_column = 0
time_column = 1
max_temp_column = 2
min_temp_column = 3


def clean_column(temparute_column):
    # Put this in a function so that this is easier

    # Write function for special case row 0

    top_row_temp = data[0][temparute_column]

    # Clean Condition C
    if top_row_temp == -9999:
        for row_index in range(1, data.shape[0]):
            current_temp = data[row_index][temparute_column]
            if current_temp != -9999:
                top_row_temp = current_temp
                data[0][temparute_column] = top_row_temp  # Changing Array
                break

    # Iterates from row 1 to n
    for row_index in range(1, data.shape[0]):
        current_temp = data[row_index][temparute_column]
        if current_temp == -9999:
            temp_below = data[row_index + 1][temparute_column]
            temp_above = data[row_index - 1][temparute_column]

            # Clean Condition A
            if temp_below != -9999:
                new_temp = (temp_below + temp_above) / 2
                data[row_index][temparute_column] = new_temp

            # Clean Condition B
            else:
                new_temp = temp_above
                data[row_index][temparute_column] = new_temp


clean_column(max_temp_column)
clean_column(min_temp_column)

# %%

# Instructions say to use {16919}, which is too small. value should be {17519} b/c 8760 x 2 - 1 = 17519

# -1 is needed so that every interpolated row has an original row above and below
# else the last row is just a clone of the row above, thus not interpolated.

interpolated_data = np.zeros((data.shape[0] * 2 - 1, 4))

# Fill interpolated data with original data

# Slicey dicey way
# The line below slices every other row from the origianl array, and we just set the sliced array = to the old array. When the array is not sliced we get the data to be on every even row. This is actually kind of cool.

interpolated_data[::2][:] = data

# loops through all gap rows, which have a row above and below for interpolation

for gap_row_i in range(1, interpolated_data.shape[0] - 1, 2):
    interpolated_row = interpolated_data[gap_row_i]
    interpolated_row_above = interpolated_data[gap_row_i - 1]
    interpolated_row_below = interpolated_data[gap_row_i + 1]
    # Copy Date Above

    interpolated_row[date_column] = interpolated_row_above[date_column]
    interpolated_row[time_column] = interpolated_row_above[time_column] + 30

    # Average of Row Above and Below
    interpolated_row[max_temp_column] = interpolated_row_above[max_temp_column] + \
        interpolated_row_below[max_temp_column] / 2
    interpolated_row[min_temp_column] = interpolated_row_above[min_temp_column] + \
        interpolated_row_below[min_temp_column] / 2

export_data(interpolated_data)

# %%
