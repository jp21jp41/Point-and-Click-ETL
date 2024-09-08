# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:04:02 2024

@author: justi
"""

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

# The count values to be added to allow 'count'-based execution functions to run
count_menu = ['first', 'second', 'third']

"""

The class MultiData is meant to be able to take tkinter (GUI) 
rows given a column from a dictionary to add or delete them 
given the user's efforts.

Note: The class is not fully functional.

"""

class MultiData:
    """
    Initializer:
    - label_opt_set: holds the assets of each column
    to allow selection of variables on the GUI
    - row_assets: holds the assets of each row
    given a column
    - columns: holds the columns of the data set
    (not of the GUI)
    - value_index: holds the values of each row
    - total: holds the total count of each row
    - count: holds the count of a column
    - final_count: holds the count of the final column
    - data: the original data to be added to the class
    - true_data: holds data taken from the data columns
    - data_edit: holds the edited data given data columns
    hold dependent variables ("data") or independent variables
    ("categorical variables")
    """
    def __init__(self, label_opt_set = {}, row_assets = {},
                 columns = [], value_index = {}, total = {},
                 count = 1, final_count = 2, data = [],
                 true_data = {}, data_edit = {}):
        self.label_opt_set = label_opt_set
        self.row_assets = row_assets
        self.columns = columns
        self.value_index = value_index
        self.total = total
        self.count = count
        self.final_count = final_count
        self.data = data
        self.true_data = true_data
        self.data_edit = data_edit
        
    """
    Function to add data to the class
    - data: the data set
    """
    def addData(self, data):
        self.data = data
    
    """
    Function to create a number of GUI columns
    (could be editable pending the efficiency
     of the current version)
    - count: the initial GUI column point
    - final_count: the final GUI column point
    - data_columns: the data columns
    """
    def counts(self, count, final_count, data_columns):
        init_column = [x for x in data_columns]
        self.row_assets.update({count : {}})
        self.value_index.update({count : {}})
        self.total.update({count : 0})
        self.label_opt_set.update({count : ['', '', '']})
        self.label_opt_set[count][0] = tk.StringVar(frame)
        self.label_opt_set[count][0].set(
            "Select Columns of Variable " + str(count))
        self.label_opt_set[count][1] = tk.OptionMenu(
            frame, self.label_opt_set[count][0], *init_column,
            command = lambda z: self.newRow(z, count))
        self.label_opt_set[count][1].grid(
            row = 1, column = 2*(count) - 2)
        self.label_opt_set[count][2] = tk.Button(
            frame, text = "Submit Columns", 
            command = lambda: self.submitColumns(count))
        self.label_opt_set[count][2].grid(
            row = 2, column = 2*(count) - 2)
        self.columns = init_column
        if final_count == 1:
            return
        self.counts(count + 1, final_count - 1, init_column)
        
    
    """
    Function to change the GUI column entries
    - count: See "counts" function
    - final_count: "" "" ""
    - new_column: a data column set (ideally edited)
    """
    def replace_column(self, count, final_count, new_column):
        if len(self.label_opt_set[count]) != 4:
            self.label_opt_set[count][1].grid_forget()
            self.label_opt_set[count][1] = tk.OptionMenu(
                frame, self.label_opt_set[count][0], *new_column,
                command = lambda z: self.newRow(z, count))
            self.label_opt_set[count][1].grid(row = 1, column = 
                                              2*(count) - 2)
        if final_count == 1:
            return
        self.replace_column(count + 1, final_count - 1, new_column)
        
        
    """
    Function to add a row to the GUI of a column
    - value: the value to be added
    - count: a given column count
    - shift: a GUI row shifter (such that rows will not overlap)
    """
    def newRow(self, value, count, shift = 3):
        self.columns.remove(value)
        self.replace_column(self.count, self.final_count, self.columns)
        self.row_assets[count].update({value : ['', '']})
        self.row_assets[count][value][0] = tk.Label(
            frame, text = str(value))
        self.row_assets[count][value][1] = tk.Button(
            frame, text = "Delete", command = lambda:
                self.deleteRow(value, count))
        self.row_assets[count][value][0].grid(
            row = self.total[count] + shift, column = 2*count - 2)
        self.row_assets[count][value][1].grid(
            row = self.total[count] + shift, column = 2*count - 1)
        self.value_index[count].update({value : self.total[count]})
        self.total[count] += 1
        
        
    """
    Function to delete a given row
    - value: See "newRow" function
    - count: "" "" ""
    """
    def deleteRow(self, value, count):
        self.columns.append(value)
        self.replace_column(self.count, self.final_count, self.columns)
        self.total[count] -= 1
        self.row_assets[count][value][0].destroy()
        self.row_assets[count][value][1].destroy()
        value_check = self.value_index[count][value]
        self.row_assets[count].pop(value)
        self.value_index[count].pop(value)
        for entry in self.value_index[count]:
            if self.value_index[count][entry] > value_check:
                new_row = self.row_assets[
                    count][entry][0].grid_info()["row"] - 1
                self.row_assets[count][entry][0].grid_forget()
                self.row_assets[count][entry][1].grid_forget()
                self.row_assets[count][entry][0].grid(
                    row = new_row, column = 2*count - 2)
                self.row_assets[count][entry][1].grid(
                    row = new_row, column = 2*count - 1)
                self.value_index[count][entry] -= 1
                
    
    
    """
    Function to submit data columns and lock such entries into
    the GUI of a GUI column
    - count: See "newRow" function
    """
    def submitColumns(self, count):
        self.true_data.update({count : []})
        if len(self.value_index[count]) == 0:
            return
        for submittable in self.value_index[count]:
            self.row_assets[count][submittable][1].destroy()
            self.true_data[count].append(
                self.data[submittable])
        self.label_opt_set[count][1].destroy()
        self.label_opt_set[count][2].destroy()
        self.label_opt_set[count].append('')
        self.label_opt_set[count][0] = tk.StringVar(frame)
        self.label_opt_set[count][0].set(
            "Do the columns hold data or categorical variables?")
        self.label_opt_set[count][1] = tk.OptionMenu(
            frame, self.label_opt_set[count][0],
            *['Data', 'Categorical Variables'],
            command = lambda x: self.columnVar(x, count))
        self.label_opt_set[count][2] = tk.Button(
            frame, text = "Submit Data",
            command = lambda: self.submitData(self.true_data[count], count))
        self.label_opt_set[count][1].grid(
            row = 1, column = 2*count - 2)
        self.label_opt_set[count][2].grid(
            row = 2, column = 2*count - 2)
        
        
        
    """
    Function to add or change the option of "Data"
    or "Categorical Variables" on a GUI column
    - result: "Data" or "Categorical Variables"
    - count: See "newRow" function
    """
    def columnVar(self, result, count):
        self.label_opt_set[count][3] = result
    
    
    """
    Function to submit the data of a GUI column
    - submitted: the data columns submitted
    - count: See "newRow" function
    """
    def submitData(self, submitted, count):
        if self.label_opt_set[count][3] == 'Data':
            print('Data column set function should run')
            print(submitted)
        if self.label_opt_set[count][3] == 'Categorical Variables':
            print('Categorical Variable column set function should run')
            print(submitted)
        
        
        
    
# Instantiating a MultiData object
row_set = MultiData()    


# Error message contingent on given errors
error_msg = tk.Text(frame, height = 1, width = 20)


"""
Function to upload the data on the GUI
using a directory (currently limited
to CSV)
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
        row_set.addData(data_set)
        row_set.counts(1, 2, data_set.columns)
    except:
        error_msg.grid(row = 5)
        error_msg.insert('1.0', 'File not read')
        return
    directory_text.destroy()
    data_input.destroy()
    upload_button.destroy()

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




