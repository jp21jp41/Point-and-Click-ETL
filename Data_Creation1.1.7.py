# Creating a Statistical Result Table from a Point-and-Click Interface
# Version 1.1.7: Tkinter uploader
# Justin Pizano


# Import libraries
import pandas as pnd
import math
import tkinter as tk
import numpy as np
import scipy.stats as stats

"""

Tkinter has to be used for the GUI. The first tkinter,
'frame', has to be instantiated with the ability to upload the
dataset, to indicate whether variables are one-column or
multi-column, and to list those columns to be submitted.

"""

frame = tk.Tk()
frame.title("Data Creation")
frame.geometry('800x400')

"""

The class MultiData is meant to be able to take tkinter rows given a column
from a dictionary to add or delete them given the user's efforts.

Note: The class is not fully functional.

"""

class MultiData:
    """
    
    MultiData initializer:
    
    - self: the MultiData object
    
    - deletion_storage: a dictionary with a given count, then a number per row,
    with a storage item label and deletion button on each row
    (expected to be initially empty)
    
    - count_set: a dictionary with given counts, and the total number of rows
    per dictionary (expected to be initially empty)
    
    - value_set: a dictionary with given counts, and the values of the labels
    of each row (currently not fully functional, expected to be initially empty)
    
    """
    def __init__(self, deletion_storage = {}, count_set = {}, value_set = {}):
        self.deletion_storage = deletion_storage
        self.count_set = count_set
        self.value_set = value_set
    
    """
    
    Function to create a new count dictionary with each of count_set and
    deletion_storage if the count is already part of the dictionary
    
    self: the MultiData object
    
    count: the count to be added if necessary
    
    """
    def newCount(self, count):
        if count in self.deletion_storage:
            return
        self.deletion_storage.update({count : {}})
        self.count_set.update({count : 0})
    
    """
    
    Function to add a new tkinter row
    
    self: the MultiData object
    
    count: the count of the specific item
    
    number: an integer that specifies the tkinter row
    
    shift: an integer that keeps the numbers in line with the rows
    
    box: a box item (created before the newRow attempt)
    
    button: a button item (created before the newRow attempt)
    
    value: a specified value that should not be repeated. If it is
    on the same column as where the new row attempt takes place, no
    additional row is created. If the new row attempt is on a separate
    column from where the value is, the old row must be deleted, meaning
    the row must be destroyed using 'grid_destroy()', the value must be
    deleted from the old 'value_set', and the count_set value must be
    decremented, all while the new row ends up being the replacement.
    At the same time, should there be any rows below the deleted
    row, they have to be moved up one row each.
    """
    def newRow(self, count, number, shift, box, button, value):
        for point in self.value_set:
            if value in self.value_set[point]:
                if point == count:
                    return
                else:
                    self.deleteRow(point, self.value_set[point].index(value), shift)
        try:
            self.value_set[count].append(value)
        except:
            self.value_set.update({count : [value]})
        self.deletion_storage[count].update({number : [box, button]})
        self.count_set[count] += 1
        self.deletion_storage[count][number][0].grid(row = number + shift, column = (2*count - 2))
        self.deletion_storage[count][number][1].grid(row = number + shift, column = (2*count - 1))
    
    """
    
    Function to delete a given row.
    
    self: the MultiData object
    
    count: the count of the row to be deleted
    
    number: the number order of the row to be deleted
    
    shift: the shift of the row
    
    """
    def deleteRow(self, count, number, shift):
        print(count)
        print(number)
        self.deletion_storage[count][number][0].destroy()
        self.deletion_storage[count][number][1].destroy()
        self.deletion_storage[count].pop(number)
        self.count_set[count] -= 1
        self.value_set[count].pop(number)
        for point in self.deletion_storage[count]:
            if point > number:
                print(point)
                self.deletion_storage[count][point][0].grid_forget()
                self.deletion_storage[count][point][1].grid_forget()
                self.deletion_storage[count][point][0].grid(row = shift + point - 1, column = (2*count - 2))
                self.deletion_storage[count][point][1].grid(row = shift + point - 1, column = (2*count - 1))


# MultiData object instantiated

row_set = MultiData()

"""

Function to create a data list with a submit button that allows the data
columns to be selected given the columns are one-variable ('One' ends up
selected on the highest 'OptionMenu')

- value: the selected previous 'OptionMenu' value (only currently necessary given the 
lambda function of the 'OptionMenu')

- count: the count value of the button (there is only three: 1, 2, 3)

- data_columns: the selected columns of the data frame (to be shown to be selected
on the newly created 'OptionMenu')

The function of course is not yet ready to be implemented.

"""




def submission_list(value, count, data_columns):
    exec('list_text' + str(count) + ' = tk.Label(frame, height = 1, width = 15, text = str(value))')
#   exec('list_text' + str(count) + '.grid(row = 6, column = ' +
#         str(2*(count) - 2) + ')')
    exec('list_deletion' + str(count) + ' = tk.Button(frame,' +
         ' text = "Delete")')
    row_set.newCount(count)
    exec('row_set.newRow(count, len(row_set.deletion_storage[count]), 6, list_text' +
         str(count) + ', list_deletion' + str(count) + ', value)')
    print(row_set.count_set)



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
    exec('option_string' + str(count) + ' = tk.StringVar(frame, name = "selmenu" + str(count))')
    exec('option_string' + str(count) + '.set("Select your ' +
                                        count_menu[count - 1].lower() + ' variable")')
    if value == 'One':
        exec('var_' + str(count) + '_options = tk.OptionMenu(frame, option_string' + 
                                                str(count) + ', *' + str(data_columns) + 
                                                ', value, command = lambda x: var_submission(x, '
                                                + str(count) + ', ' + str(data_columns) + '))')
        exec('var_' + str(count) + '_options.grid(row = 1, column = ' + str(2*count - 2) + ')')
    elif value == 'Multiple':
        exec('var_' + str(count) + '_options = tk.OptionMenu(frame, option_string' + 
                                                str(count) + ', *' + str(data_columns) + 
                                                ', value, command = lambda x: submission_list(x, '
                                                + str(count) + ', ' + str(data_columns) + '))')
        exec('var_' + str(count) + '_options.grid(row = 1, column = ' + str(2*count - 2) + ')')



"""

Function to create a submit button that allows the data columns to be selected
given the columns are one-variable ('One' ends up selected on the highest
'OptionMenu')

- value: the selected previous 'OptionMenu' value (only currently necessary given the 
lambda function of the 'OptionMenu')

- count: the count value of the button (there is only three: 1, 2, 3)

- data_columns: the selected columns of the data frame (to be shown to be selected
on the newly created 'OptionMenu')

The function of course is not yet ready to be implemented.

"""

def var_submission(value, count, data_columns):
    try:
        exec('var_' + str(count) + '_sub.grid_forget()')
    except:
        pass
    exec('var_' + str(count) + '_sub = tk.Button(frame, text = "Submit")')
    exec('var_' + str(count) + '_sub.grid(row = 2, column = ' + str(2*count - 2) + ')')







# Error message contingent on given errors
error_msg = tk.Text(frame, height = 1, width = 20)

# The count values to be added to allow 'count'-based execution functions to run
count_menu = ['First', 'Second', 'Third']

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
    exec('starting_string' + str(count) + '.set(count_menu[count - 1] + " variable set")')
    exec('var_' + str(count) + '_menu = tk.OptionMenu(frame, starting_string' + 
                                                      str(count) + ', *["One", "Multiple"], command = lambda x: selection(x, ' +
                                                      str(count) + ', ' + str(cols) + '))')
    exec('var_' + str(count) + '_menu.grid(row = 0, column = ' + str(2*(count) - 2) + ')')
    exec('var_' + str(count) + '_menu.config(width = 20)')
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
