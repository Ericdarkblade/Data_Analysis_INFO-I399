"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    Replace this line with a description of your program.

Assignment Information
    Assignment:     e.g. Ind HW4 - PY 1
    Author:         Name, login@purdue.edu
    Team ID:        LC# - ## (e.g. LC1 - 01; for section LC1, team 01)

Contributor:    Name, login@purdue [repeat for each]
    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
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

# Write any import statements here (and delete this comment).
import numpy as np

# This function will load data from the text file into a Numpy Array
# You do not need to add or change any code in this funciton
# Call this function by assigning it to a variable in your main program to access the data
def load_data():
    data = np.loadtxt('CRNH0203-2022-IN_Bedford_5_WNW.txt', usecols=(1,2,10,11))

    return data


# This function will save an array as a csv file named "output.csv"
# in your current working directory.
# Call this funciton at the end of your main program to save your final
# array as a csv.
def export_data(array):
    np.savetxt('output.csv', array, delimiter=',')


def main():
    # Write your code here (and delete this comment).
    print("Hello")


if __name__ == '__main__':
    main()


