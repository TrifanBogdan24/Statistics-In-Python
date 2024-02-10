#!/usr/bin/env python3

import sys                         # pentru argumentele liniei de comanda
import os
import csv
import math
import matplotlib.pyplot as plt     # for plotting and graphical suport
import numpy as np                  # for liniar regression

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


def average(values):
    # expects a list of doubles (vector)

    if len(values) == 0:
        sys.stderr.write("Err: empty data for average.")
        sys.exit(1)

    sum = 0.0

    for el in values:
        sum += el

    n = float(len(values))
    avg = sum / n

    # aproximarea cu doua zecimale
    rounded = round(avg, 2)
    return rounded

def deviation_from_mean(values):
    # expects a list of doubles (vector)

    avg = average(values)
    d = []

    for val in values:
        # aproximarea cu doua zecimale a diferentei
        diff = val - avg
        rounded = round(diff, 2)
        d.append(rounded)

    return d
    

def mean_standard_deviation(values):
    # expects a list of doubles (vector)

    Dv = deviation_from_mean(values)
    n = float(len(values))

    sum = 0.0

    for el in Dv:
        sum = sum + el * el

    dev = math.sqrt(sum / (n * (n - 1.0)))
    
    # aproximarea cu doua zecimale
    rounded = round(dev, 2)
    return rounded



def covariance(X_values, Y_values):
    # X_values = expects a list of doubles (vector)
    # Y_values = expects a list of doubles (vector)
    
    X_avg = average(X_values)
    Y_avg = average(Y_values)

    cov = 0.0
    n = int(len(X_values))

    for i in range(0, n):
        cov = cov + (X_values[i] - X_avg) * (Y_values[i] - Y_avg)

    cov = cov / (float(n))
    
    # aproximarea cu doua zecimale
    rounded = round(cov, 2)
    return rounded


def correlation(X_values, Y_values):
    # X_values = expects a list of doubles (vector)
    # Y_values = expects a list of doubles (vector)

    X_avg = average(X_values)
    Y_avg = average(Y_values)
    
    sumOfProds = 1.0    # for numerator
    X_sum = 0.0         # for denumitor
    Y_sum = 0.0         # for denumitor

    for i in range(0, len(X_values)):
        sumOfProds = sumOfProds + (X_values[i] - X_avg) * (Y_values[i] - Y_avg)
        X_sum = X_sum + (X_values[i] - X_avg) * (X_values[i] - X_avg)        
        Y_sum = Y_sum + (Y_values[i] - Y_avg) * (Y_values[i] - Y_avg)

    if X_sum == 0.0 or Y_sum == 0.0:
        # no correlation between the variables
        # either one of them is constant
        return 0.0
    
    # coeficientul de corelatie
    corr = sumOfProds / (math.sqrt(X_sum) * math.sqrt(Y_sum))

    if corr < -1.0 or corr > 1.0:
        sys.stderr.write("Oopss... Something went wrong while calculating the correlation.")

    # aproximarea cu doua zecimale
    rounded = round(corr, 2)
    return rounded

def rounded_valuesor(vect):
    # valorile vor fi aproximate si afisate cu 2 zecimale
    ret_values = []
    
    for el in vect:
        ret_values.append(float(el))
    
    return ret_values


def analysis(X_name, Y_name, X_values, Y_values, lin_coeff, quad_coeff, cubic_coeff, plot_index):
    

    # plt.plot(3, 2)

    Xavg = average(X_values)
    Xd = deviation_from_mean(X_values)
    Xstd_dev = mean_standard_deviation(X_values)

    print(f"{X_name} : {rounded_valuesor(X_values)}")
    print(f"{Y_name} : {rounded_valuesor(Y_values)}")

    print()
    print(f"Average : {Xavg :.2f}")
    print(f"Deviation (from average) : {Xd}")
    print(f"Mean standard deviation : {Xstd_dev :.2f}")
    print(f"Confidence interval : {Xavg :.2f} ± {Xstd_dev :.2f}")

    text = ''       # th text will be displayed alongside with the plots
    # text += f"{X_name} : {rounded_valuesor(X_values)}\n"
    # text += f"{Y_name} : {rounded_valuesor(Y_values)}\n\n" 
    text += f"Average : {Xavg :.2f}\n"
    # text += f"Deviation (from average) : {Xd}\n"
    text += f"Mean standard deviation : {Xstd_dev :.2f}\n"
    text += f"Confidence interval : {Xavg :.2f} ± {Xstd_dev :.2f}\n"


    covXY = covariance(X_values, Y_values)
    print()
    print(f"Covariance between {X_name} and {Y_name} : {covXY :.2f}")
    text += (f"Covariance between {X_name} and {Y_name} : {covXY :.2f}\n")
    
    
    if covXY > 0:
        print(f"An increase of {X_name} might result in an increase of {Y_name}.")
        print(f"A decrease of {X_name} might result in a decrease of {Y_name}.")

        text += (f"An increase of {X_name} might result in an increase of {Y_name}.\n")
        text += (f"A decrease of {X_name} might result in a decrease of {Y_name}.\n")

    else:
        print(f"An increase of {X_name} might result in a decrease of {Y_name}.")
        print(f"A decrease of {X_name} might result in an increase of {Y_name}.")

        text += (f"An increase of {X_name} might result in a decrease of {Y_name}.\n")
        text += (f"A decrease of {X_name} might result in an increase of {Y_name}.\n")

    corrXY = correlation(X_values, Y_values)
    print()

    if corrXY < -1.0 or corrXY > 1.0:
        # an error has occured
        print(f"Correlation between {X_name} and {Y_name} : ???")
    else:
        print(f"Correlation between {X_name} and {Y_name} : {corrXY :.2f}")
        text += (f"Correlation between {X_name} and {Y_name} : {corrXY :.2f}\n")


    abscorrXY = abs(corrXY)

    if abscorrXY == 0.0:
        print(f"There is no correlation between {X_name} and {Y_name}")
        text += (f"There is no correlation between {X_name} and {Y_name}.\n")
    elif 0.0 < abscorrXY and abscorrXY <= 0.2:
        print(f"Between {X_name} and {Y_name}, there is a VERY WEAK correlation.")
        text += (f"Between {X_name} and {Y_name}, there is a VERY WEAK correlation.\n")
    elif 0.2 < abscorrXY and abscorrXY <= 0.4:
        print(f"Between {X_name} and {Y_name}, there is a WEAK correlation.")
        text += (f"Between {X_name} and {Y_name}, there is a WEAK correlation.\n")
    elif 0.4 < abscorrXY and abscorrXY <= 0.6:
        print(f"Between {X_name} and {Y_name}, there is a MODERATE correlation.")
        text += (f"Between {X_name} and {Y_name}, there is a MODERATE correlation.\n")
    elif 0.6 < abscorrXY and abscorrXY <= 0.8:
        print(f"Between {X_name} and {Y_name}, there is a STRONG correlation.")
        text += (f"Between {X_name} and {Y_name}, there is a STRONG correlation.\n")
    elif 0.8 < abscorrXY and abscorrXY < 1.0:
        print(f"Between {X_name} and {Y_name}, there is a VERY STRONG correlation.")
        text += (f"Between {X_name} and {Y_name}, there is a VERY STRONG correlation.\n")
    elif abscorrXY == 1.0:
        print(f"{X_name} and {Y_name} are correlated.")
        text += (f"{X_name} and {Y_name} are correlated.\n")


    print(f"Liniar regression : Y = {lin_coeff[0] :.2f} * X + {lin_coeff[1] :.2f}")
    print(f"Quadratic regression : Y = {quad_coeff[0] :.2f} * X^2 + {quad_coeff[1] :.2f} * X + {quad_coeff[2] :.2f}")
    print(f"Cubic regression : Y = {cubic_coeff[0] :.2f} * X^3 + {cubic_coeff[1] :.2f} * X^2 + {cubic_coeff[2] :.2f} * X + {cubic_coeff[3] :.2f}")
    

    text += (f"Liniar regression : Y = {lin_coeff[0] :.2f} * X + {lin_coeff[1] :.2f}\n")
    text += (f"Quadratic regression : Y = {quad_coeff[0] :.2f} * X^2 + {quad_coeff[1] :.2f} * X + {quad_coeff[2] :.2f}\n")
    text += (f"Cubic regression : Y = {cubic_coeff[0] :.2f} * X^3 + {cubic_coeff[1] :.2f} * X^2 + {cubic_coeff[2] :.2f} * X + {cubic_coeff[3] :.2f}\n")
    
    # plt.text(0.5, 0.5, text, fontsize = 9.5, color='black', ha='left', va='center')
    # plt.axis('off')
    # plt.show()

    # plt.tight_layout()

def scattered_points_plot(X_name, Y_name, X_values, Y_values, plot_index):
    
    # the plot will contain only the points provided by the two vectors
    plt.subplot(3, 2, plot_index)
    plt.scatter(X_values, Y_values, color='blue')

    plt.title("Scatter Plot")
    plt.xlabel(X_name)
    plt.ylabel(Y_name)

def liniar_regression_plot(X_name, Y_name, X_values, Y_values, plot_index):
    
    # the plot will scatter the points
    # and will draw the liniar dependancy betweem them
    # d : Y = m * X + n
    
    plt.subplot(3, 2, plot_index)
    plt.scatter(X_values, Y_values, color='blue')

    # Calculate linear regression
    (slope, intercept) = np.polyfit(X_values, Y_values, 1)
    coefficients = []
    coefficients.append(slope)
    coefficients.append(intercept)
    regression_line = slope * np.array(X_values) + intercept

    plt.plot(X_values, regression_line, color='green')

    plt.title("Liniar Regression Plot")
    plt.xlabel(X_name)
    plt.ylabel(Y_name)

    return coefficients

def quadrtic_regression_plot(X_name, Y_name, X_values, Y_values, plot_index):

    # the plot will scatter the points
    # and will draw the quadratic dependancy betweem them
    # d : Y = a * X^2 + b * X + c

    plt.subplot(3, 2, plot_index)
    plt.scatter(X_values, Y_values, color='blue')

    # Calculate quadratic regression
    coefficients = np.polyfit(X_values, Y_values, 2)
    quadratic_regression = np.poly1d(coefficients)

    # Plot the quadratic regression curve with green color
    X_curve = np.linspace(min(X_values), max(X_values), 100)
    plt.plot(X_curve, quadratic_regression(X_curve), color='green')


    plt.title("Quadratic Regression")
    plt.xlabel(X_name)
    plt.ylabel(Y_name)
    
    return coefficients

def cubic_regression_plot(X_name, Y_name, X_values, Y_values, plot_index):

    # the plot will scatter the points
    # and will draw the cubic dependancy betweem them
    # d : Y = a * X^3 + b * X^2 + c * X + d

    plt.subplot(3, 2, plot_index)
    plt.scatter(X_values, Y_values, color='blue')

    # Calculate cubic regression
    coefficients = np.polyfit(X_values, Y_values, 3)
    cubic_regression = np.poly1d(coefficients)

    # Generate X values for the curve
    X_curve = np.linspace(min(X_values), max(X_values), 100)

    # Plot the cubic regression curve with green color
    plt.plot(X_curve, cubic_regression(X_curve), color='green')

    # Label the axes
    plt.title("Cubic Regression")
    plt.xlabel(X_name)
    plt.ylabel(Y_name)

    return coefficients

def chart_bars(X_name, Y_name, X_values, Y_values, plot_index):

    # the plot will contain the chart bars

    plt.subplot(3, 2, plot_index)
    plt.bar(X_values, Y_values, width = 0.1)
    plt.xlabel(X_name)
    plt.ylabel(Y_name)
    plt.title(f"Chart bars for {Y_name}")

def main():

    # ./stats.py inputdata.csv
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

    scattered_points_plot(X_name, Y_name, X_values, Y_values, 1)
    chart_bars(X_name, Y_name, X_values, Y_values, 2)
    
    lin_coeff = liniar_regression_plot(X_name, Y_name, X_values, Y_values, 3)
    quad_coeff = quadrtic_regression_plot(X_name, Y_name, X_values, Y_values, 4)
    cubic_coeff = cubic_regression_plot(X_name, Y_name, X_values, Y_values, 5)
    
    analysis(X_name, Y_name, X_values, Y_values, lin_coeff, quad_coeff, cubic_coeff, 6)

    # will show all plots
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()
