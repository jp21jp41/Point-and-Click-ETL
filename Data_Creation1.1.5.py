# Creating a Statistical Result Table from a Point-and-Click Interface
# Version 1.1.5: Tkinter uploader
# Justin Pizano


# Import libraries
import pandas as pnd
import math
import tkinter as tk
import numpy as np
import scipy.stats as stats
import tkinter as tk

"""

Tkinter has to be used for the GUI. The first tkinter,
'frame', has to be instantiated with the ability to upload the
dataset, to indicate whether variables are one-column or
multi-column, and to list those columns to be submitted.

"""
frame = tk.Tk()
frame.title("Data Creation")
frame.geometry('800x200')


"""

Function to create an 'OptionMenu' for a given selection of
'One' or 'Multiple' columns.

- value: the selected previous 'OptionMenu' value (only currently necessary given the 
lambda function of the 'OptionMenu')

- count: the count value of the button (there is only three: 1, 2, 3)

- data_columns: the selected columns of the data frame (to be shown to be selected
on the newly created 'OptionMenu')

The function is not yet ready to be implemented

"""
def selection(value, count, data_columns):
    print(value)
    print(count)
    exec('option_string' + str(count) + ' = tk.StringVar(frame)')
    exec('option_string' + str(count) + '.set("Select your ' +
                                                count_menu[count - 1] + ' variable")')
    exec('var_' + str(count) + '_options = tk.OptionMenu(frame, option_string' + 
                                                str(count) + ', *' + str(data_columns) + 
                                                ', value, command = lambda x: var_submission(x, '
                                                + str(count) + ', ' + str(data_columns) + '))')
    exec('var_' + str(count) + '_options.grid(row = 1, column = ' + str(count) + ')')


"""

Function to create a submit button that allows the data columns to be selected
based on whether the columns are 'One' or 'Multiple'

- value: the selected previous 'OptionMenu' value (only currently necessary given the 
lambda function of the 'OptionMenu')

- count: the count value of the button (there is only three: 1, 2, 3)

- data_columns: the selected columns of the data frame (to be shown to be selected
on the newly created 'OptionMenu')

- allowance (not yet implemented): the allowed amount of columns, which will
allow how many columns to be added to the data.

The function of course is not yet ready to be implemented.

"""

def var_submission(value, count, data_columns):
    print(value)
    print(count)
    print(data_columns)
    exec('var_' + str(count) + '_sub = tk.Button(frame, text = "Submit")')
    exec('var_' + str(count) + '_sub.grid(row = 2, column = ' + str(count) + ')')


# Error message contingent on given errors
error_msg = tk.Text(frame, height = 1, width = 20)

# The count values to be added to allow 'count'-based execution functions to run
count_menu = ['first', 'second', 'third']

"""

Function to allow the data to be put into columns, with execution functions running
to form menus as part of the Tkinter interface

data: the dataset recovered

total_count: a number to count down to 1 recursively (should be 1, 2, or 3)

count: the count value to allow menus to be implemented through execution functions

The function is (currently) implementing as it should.

"""
def var_subs(data, total_count, count):
    cols = []
    for col in data.columns:
        cols.append(col)
    exec('starting_string' + str(count) + ' = tk.StringVar(frame)')
    exec('starting_string' + str(count) + '.set("Do you want to select one column for your ' + 
                                                count_menu[count - 1] + ' variable or multiple?")')
    exec('var_' + str(count) + '_menu = tk.OptionMenu(frame, starting_string' + 
                                                str(count) + ', *["One", "Multiple"], command = lambda x: selection('
                                                + str(x) + ', ' +
                                                str(count) + ', ' + str(cols) + '))')
    exec('var_' + str(count) + '_menu.grid(row = 0, column = ' + str(count) + ')')
    if total_count == 1:
        return
    var_subs(data, total_count - 1, count + 1)


"""

Function to allow the data to be uploaded through a Tkinter interface
with the ability to input a directory and submit it as a CSV file

"""

def data_upload():
    try:
        error_msg.delete('1.0', 'end')
        error_msg.grid_forget()
    except:
        pass
    the_directory = data_input.get(1.0, "end-1c")
    try:
        data_set = pnd.read_csv(the_directory)
        print(data_set.columns)
    except:
        error_msg.grid(row = 5)
        error_msg.insert('1.0', 'File not read')
        return
    directory_text.grid_forget()
    data_input.grid_forget()
    upload_button.grid_forget()
    var_subs(data_set, 3, 1)


# The label of the Tkinter submission page that indicates
# Where to submit the dataset directory
directory_text = tk.Label(frame,
                  text = "Enter the directory to your dataset")


# The grid addition of the previously noted label 
directory_text.grid()

# The textbox of the Tkinter submission page to submit
# The dataset directory on
data_input = tk.Text(frame,
                   height = 5,
                   width = 20)


# The grid addition of the previously noted textbox
data_input.grid()

# The button to upload the dataset
upload_button = tk.Button(frame,
                        text = "Upload the dataset",
                        command = data_upload)


# The grid addition of the button
upload_button.grid()


# The creation of a label that will hold an error should it occur
# and its grid addition
lbl = tk.Label(frame, text = "")
lbl.grid()
frame.mainloop()
