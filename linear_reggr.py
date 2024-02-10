#!/usr/bin/env python3

import sys                         # pentru argumentele liniei de comanda
import os
import csv
import math
import matplotlib.pyplot as plt     # for plotting and graphical suport
import numpy as np                  # for liniar regression
import pandas

from stats import average


def is_valid_csv(csv_file_path):

    X_name = ""
    Y_name = ""
    X_values = []
    Y_values = []

    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Get the header (first line)
            
            # Check if there are exactly two columns in the header
            if len(header) != 2:
                return (X_name, Y_name, X_values, Y_values, False)

            # Check if the first line contains strings (variable names)
            if not all(isinstance(col, str) for col in header):
                return (X_name, Y_name, X_values, Y_values, False)

            X_name = header[0]
            Y_name = header[1]

            # Check if the rest of the table contains only float/double values
            for row in reader:

                if len(row) != 2:
                    return (X_name, Y_name, X_values, Y_values, False)

                try:
                    X_values.append( float(row[0]) )
                    Y_values.append( float(row[1]) )
                except Exception as e:
                    sys.stderr.write("Err: the CSV should conatain numers.")
                    return (X_name, Y_name, X_values, Y_values, False)
    
    except Exception as e:
        # Handle file not found or other exceptions
        print(f"Err: {e}")
        return (X_name, Y_name, X_values, Y_values, False)

    return (X_name, Y_name, X_values, Y_values, True)




#     (1 x1)                        (y1)
#     (1 x2)       (slope)          (y2)
# A = (... )   X = (intercept)  B = (..)      
#     (1 xn)                        (yn)
#    
#            
# X = (A * A') ^ (-1) * A' * B
def liniar_regression_algorithm(X_values, Y_values):
    # X_values => list of OX correspondent of each point
    # Y_values => list of OY correspondent of each point

    isVerticalBar = True

    for x in X_values:
        if x != X_values[0]:
            isVerticalBar = False

    if isVerticalBar is True:
        slope = X_values[0]
        intercept = 0.0
        return (slope, intercept)
    
    slope = 0.0
    intercept = 0.0

    N = int(len(X_values))

    A = np.ones((N, 2))     # matrix
    B = np.ones((N, 1))     # matrix

    for i in range(0, N):
        A[i, 1] = X_values[i]
        B[i, 0] = Y_values[i]

    # X = (A * A') ^ (-1) * A' * B
    X = np.dot(A.T, A)      # *
    X = np.linalg.inv(X)    # ^-1
    X = np.dot(X, A.T)      # *
    X = np.dot(X, B)        # *
    # A.T = A transpose

    slope = X[1, 0]
    intercept = X[0, 0]

    return (slope, intercept)

def liniar_regression_plot(X_name, Y_name, X_values, Y_values, slope, intercept):

    print(f"d : Y = {slope :.2f} * X + {intercept :.2f}")

    diff = max(X_values) - min(X_values)    # the line will go +20% to the right and -20% to the left
    X_range = np.linspace(min(X_values) - 0.2 * diff, max(X_values) + 0.2 * diff, 100)
    Y_range = slope * X_range + intercept

    plt.plot(X_range, Y_range, color='green')
    
    plt.scatter(X_values, Y_values, color='blue')

    plt.title("Liniar regression")
    plt.xlabel(X_name)
    plt.ylabel(Y_name)

    plt.show()



def main():

    # ./lin_reggr.py inputdata.csv
    nr_args = len(sys.argv)

    if nr_args == 1:
        sys.stderr.write("Err: please add the path for the input CSV file.\n")
        sys.exit(1)     # exit code

    if nr_args > 2:
        sys.stderr.write("Err: too many arguments\n\n")
        print("Script expects only a single CSV file as argument.")
        sys.exit(1)     # exit code

    file = sys.argv[1]

    if os.path.isfile(file) is False:
        sys.stderr.write(f"Err: no such file {file}.\n")
        sys.exit(1)     # exit code

    if file.endswith('.csv') is False:
        sys.stderr.write(f"Err: the file {file} is not a CSV file.\n\n")
        print("A CSV file should be named using this format : *.csv")
        print("Example : input-data.csv")
        sys.exit(1)     # exit code

    # reading from input file
    (X_name, Y_name, X_values, Y_values, validate) = is_valid_csv(file)
    
    if validate is False:
        sys.stderr.write(f"Err: innvalid CSV pattern.\n\n")

        print("The CSV should look:")
        print("variable 1, variable 2")
        print("1.5, 2.5")
        print("1.6, 27.9")
        print("1.7, 45.5")
        print("2.0, 50.5")

        sys.exit(1)     # exit code

    # calculatting the coeffiecients of the approximation polynom
    (slope, intercept) = liniar_regression_algorithm(X_values, Y_values)

    liniar_regression_plot(X_name, Y_name, X_values, Y_values, slope, intercept)



if __name__ == "__main__":
    main()
