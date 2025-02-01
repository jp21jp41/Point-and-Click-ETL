"""
Creating a Statistical Result Table from a Point-and-Click Interface
Version 2.2.4
Justin Pizano
"""

import pandas as pnd
import math
import tkinter as tk
import numpy as np
import scipy.stats as stats
from tkinter import ttk
from tkinter.messagebox import showinfo

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
count_menu = ['Categorical Rows', 'Categorical Columns', 'Quantitative Rows', 'Quantitative Columns']


    
# Prepend will be kept with other files even if it isn't used
def prepend(the_item, the_list):
    itemlist = [the_item]
    for item in the_list:
        itemlist.append(item)
    return(itemlist)
            

"""
The MultiData class helps instantiate the tkinter GUI's.
"""

class MultiData():
    def __init__(self, raw_name, tkwindow, count = 1, final_count = 4):
        self.raw_name = raw_name
        self.tkwindow = tkwindow
        self.label_opt_set = {}
        self.row_assets = {}
        self.columns = []
        self.value_index = {}
        self.total = {}
        self.count = count
        self.final_count = final_count
        self.data = []
        self.true_data = {}
        self.data_edit = {}
        self.submit_check = []
        self.name_hierarchy = {}
        
    def createNameHierarchy(self):
        for item in self.data_edit:
            if item == 'qtv_rows':
                qtv_num_set = np.arange(0, len(self.data_edit['qtv_rows']))
                for point in qtv_num_set:
                    try:
                        self.name_hierarchy['qtv_rows'].append(self.data_edit['qtv_rows'][point].name)
                    except:
                        self.name_hierarchy.update({'qtv_rows' : [self.data_edit['qtv_rows'][point].name]})
            
            
            if item == 'qtv_cols':
                qtv_num_set = np.arange(0, len(self.data_edit['qtv_cols']))
                for point in qtv_num_set:
                    try:
                        self.name_hierarchy['qtv_cols'].append(self.data_edit['qtv_cols'][point].name)
                    except:
                        self.name_hierarchy.update({'qtv_cols' : [self.data_edit['qtv_cols'][point].name]})
            
            
            if item == 'cat_rows':
                qtv_num_set = np.arange(0, len(self.data_edit['cat_rows']))
                for point in qtv_num_set:
                    try:
                        self.name_hierarchy['cat_rows'].append(self.data_edit['cat_rows'][point].name)
                    except:
                        self.name_hierarchy.update({'cat_rows' : [self.data_edit['cat_rows'][point].name]})
            
            
            if item == 'cat_cols':
                qtv_num_set = np.arange(0, len(self.data_edit['cat_cols']))
                for point in qtv_num_set:
                    try:
                        self.name_hierarchy['cat_cols'].append(self.data_edit['cat_cols'][point].name)
                    except:
                        self.name_hierarchy.update({'cat_cols' : [self.data_edit['cat_cols'][point].name]})
            
            print(self.name_hierarchy)
            
            print('check')
        return
        
    def addData(self, data):
        self.data = data
    
    def counts(self, count, final_count, data_columns):
        none_button = tk.Button(
            self.tkwindow, text = "None", 
            command = lambda : self.submitData(count, "None"))
        none_button.grid(row = 1, column = 2*(count) - 2)
        init_column = [x for x in data_columns]
        column_setter = count_menu[count - 1]
        self.row_assets.update({count : {}})
        self.value_index.update({count : {}})
        self.total.update({count : 0})
        self.label_opt_set.update({count : ['', '', '', '', '']})
        self.label_opt_set[count][0] = none_button
        self.label_opt_set[count][1] = tk.StringVar(self.tkwindow)
        self.label_opt_set[count][1].set(column_setter)
        self.label_opt_set[count][2] = tk.OptionMenu(
            self.tkwindow, self.label_opt_set[count][1], *init_column,
            command = lambda z: self.newRow(z, count))
        self.label_opt_set[count][2].grid(
            row = 2, column = 2*(count) - 2)
        self.label_opt_set[count][3] = tk.Button(
            self.tkwindow, text = "Submit Columns", 
            command = lambda: self.submitData(count, column_setter))
        self.label_opt_set[count][3].grid(
            row = 3, column = 2*(count) - 2)
        self.columns = init_column
        if final_count == 1:
            return
        self.counts(count + 1, final_count - 1, init_column)
    
    
    def newRow(self, value, count, shift = 4):
        self.columns.remove(value)
        self.replace_column(self.count, self.final_count, self.columns)
        self.row_assets[count].update({value : ['', '']})
        self.row_assets[count][value][0] = tk.Label(
            self.tkwindow, text = str(value))
        self.row_assets[count][value][1] = tk.Button(
            self.tkwindow, text = "Delete", command = lambda:
                self.deleteRow(value, count))
        self.row_assets[count][value][0].grid(
            row = self.total[count] + shift, column = 2*count - 2)
        self.row_assets[count][value][1].grid(
            row = self.total[count] + shift, column = 2*count - 1)
        self.value_index[count].update({value : self.total[count]})
        self.total[count] += 1
        
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
        
    def replace_column(self, count, final_count, new_column):
        print('18')
        if len(self.label_opt_set[count]) != 5:
            self.label_opt_set[count][2].grid_forget()
            self.label_opt_set[count][2] = tk.OptionMenu(
                self.tkwindow, self.label_opt_set[count][1], *new_column,
                command = lambda z: self.newRow(z, count))
            self.label_opt_set[count][2].grid(row = 2, column = 
                                              2*(count) - 2)
        if final_count == 1:
            return
        self.replace_column(count + 1, final_count - 1, new_column)
        
    
    
    def columnVar(self, result, count):
        self.label_opt_set[count][4] = result
    
    
    def check_item_display(self, the_item, the_string):
        new_asset_count = 0
        try:
            for item in self.row_assets[the_string]:
                self.row_assets[the_string][item][0].destroy()
            del self.row_assets[the_string]
            """
            for item in self.row_assets:
                if item == 
                self.row_assets[item][0].destroy()
            """ 
        except:
            pass
        if the_string == 'Quantitative Rows Only':
            for label_item in self.name_hierarchy['qtv_rows']:
                display = tk.Label(self.tkwindow,
                               text = label_item + ' -> data')
                display.grid(row = new_asset_count, column = 2)
                try:
                    self.row_assets[the_string][label_item].append(display)
                except:
                    try:
                        self.row_assets[the_string].update({label_item : [display]})
                    except:
                        self.row_assets.update({the_string : {label_item : [display]}})
                new_asset_count += 1
        
        
        
        if the_string == 'Quantitative Columns Only':
            for label_item in self.name_hierarchy['qtv_cols']:
                display = tk.Label(self.tkwindow,
                               text = label_item + ' -> data')
                display.grid(row = new_asset_count, column = 2)
                try:
                    self.row_assets[the_string][label_item].append(display)
                except:
                    try:
                        self.row_assets[the_string].update({label_item : [display]})
                    except:
                        self.row_assets.update({the_string : {label_item : [display]}})
                new_asset_count += 1
        
    
    def submitData(self, count, result):
        self.label_opt_set[count][4] = result
        if len(self.value_index[count]) == 0 and result != 'None':
            return
        self.label_opt_set[count][0].destroy()
        self.label_opt_set[count][2].destroy()
        self.label_opt_set[count][3].destroy()
        self.true_data.update({count : []})
        for submittable in self.value_index[count]:
            self.row_assets[count][submittable][1].destroy()
            self.true_data[count].append(
                self.data[submittable])
        if self.label_opt_set[count][4] in self.submit_check:
            return
        if self.label_opt_set[count][4] == 'Categorical Rows':
            self.submit_check.append('cat_rows')
        if self.label_opt_set[count][4] == 'Categorical Columns':
            self.submit_check.append('cat_cols')
        if self.label_opt_set[count][4] == 'Quantitative Rows':
            self.submit_check.append('qtv_rows')
        if self.label_opt_set[count][4] == 'Quantitative Columns':
            self.submit_check.append('qtv_cols')
        if self.label_opt_set[count][4] == 'None':
            self.submit_check.append('None')
        if len(self.submit_check) == self.final_count:
            for the_count in self.row_assets:
                for the_value in self.row_assets[the_count]:
                    try:
                        self.data_edit[self.submit_check[the_count - 1]].append(self.data[the_value])
                    except:
                        self.data_edit.update({self.submit_check[the_count - 1] : [self.data[the_value]]})
            
            
            self.createNameHierarchy()
            self.tkwindow.destroy()
            
            # create new window
            self.tkwindow = tk.Tk()
            self.tkwindow.geometry('1000x800')
            
            # create a treeview
            tree = ttk.Treeview(self.tkwindow)
            tree.heading('#0', text='Make a selection for the first comparison item', anchor=tk.NW)
            
            check_count = 0
            
            for check_item in self.submit_check:
                if 'qtv' in check_item:
                    check_item_str = "Quantitative"
                    if 'row' in check_item:
                        check_item_str += ' Rows Only'
                    elif 'col' in check_item:
                        check_item_str += ' Columns Only'
                    exec(str(check_item) + '_only_button = ttk.Button(self.tkwindow, ' +
                         'text = "' + str(check_item_str) + '",' +
                         ' cursor = "hand2", width = 40)')
                    exec(str(check_item) + '_only_button.grid(row = ' +
                         str(check_count) + ', column = 0)')
                    exec(str(check_item) + '_only_button.bind("<Button 1>",' + 
                         ' lambda x: ' + str(self.raw_name) + 
                         '.check_item_display(x, "' + str(check_item_str) + '"))')
                    check_count += 1
                    
                    
            

# 'row_set', the MultiData object
row_set = MultiData('row_set', frame)


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
        row_set.counts(1, 4, data_set.columns)
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



        