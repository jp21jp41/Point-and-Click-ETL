"""
Creating a Statistical Result Table from a Point-and-Click Interface
Version 2.2.1
Justin Pizano
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


def prepend(the_item, the_list):
    itemlist = [the_item]
    for item in the_list:
        itemlist.append(item)
        return(itemlist)
            
  
        
"""

The class MultiData is meant to be able to take tkinter (GUI) 
rows given a column from a dictionary to add or delete them 
given the user's efforts.

Note: The class is not fully functional.

"""

class MultiData():
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
    def __init__(self, count = 1, final_count = 2):
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
        self.hierarchical_data = [{}]
        self.data_hierarchy_count = 0
        self.given_data_aggregate = {}
        
        
    def createHierarchicalData(self, data_set):
        data_rows = {}
        data_num_list = [x for x in np.arange(
            0, len(data_set['Categorical Variables'][0]))]
        variable_columns = [
            x for x in np.arange(
            0, len(data_set['Categorical Variables']))]
        print(len(variable_columns))
        the_data_columns = [x for x in np.arange(
            0, len(data_set['Data']))]
        print(len(the_data_columns))
        
        row_count = 0
        for data_column in the_data_columns:
            for data in data_num_list:
                if not math.isnan(data_set['Data'][data_column][data]):
                    
                    try:
                        data_rows[data_set['Data'][data_column].name].append(
                            data_set['Data'][data_column][data])
                    except:
                        data_rows.update({data_set['Data'][data_column].name : [
                            data_set['Data'][data_column][data]]})
        print(data_rows)
        self.hierarchical_data[0].update(data_rows)
        
    """
    The following function must be both iterative and recursive.
    It is meant to take all of the variables and put them such that
    all data is accessible in a combination of forms through dictionaries
    """
    
    """
    def variableSet(self, variables, data_set, name, data,
                    dictionary = self.hierarchical_data,
                    mem_count = 0, memory = []):
        if len(variables) == 1:
            try:
                dictionary[variables[0]][data_rows[data_set['Data'][data_column].name]].append(
                    data_set['Data'][data_column][data])
            except:
                try:
                    dictionary[variables[0]].update({
                        data_rows[data_set['Data'][data_column].name] : data_set['Data'][data_column][data]
                        })
                except:
                    dictionary.update({
                        variables[0] :
                        {data_rows[data_set['Data'][data_column].name] : data_set['Data'][data_column][data]}
                        })
                        
             """   
            
                            

    """
    def createDataCategories(self, data_set, var_memory, 
                             data_column, data_row,
                             the_memory):
        new_memory = the_memory
        data_point = data_set['Data'][data_column].name
        data_point1 = '["' + str(data_point) + '"]'
        entry = data_set['Data'][data_column][data_row]
        new_entry = '["' + str(entry) + '"]'
        print(new_memory)
        if len(var_memory) == 0:
            try:
                print(data_point1)
                print(new_entry)
                exec('self.hierarchical_data' + str(new_memory) +
                     str(data_point1))
                #+ '.append(' + str(entry) + ')')
                print('300')
            except:
                exec('self.hierarchical_data' + str(new_memory) + 
                     '.update({"' + str(data_point) + '" : ' + str(new_entry) + '})')
            return
        if len(var_memory) >= 1:
            var11 = var_memory[0][0]
            var12 = var_memory[0][1]
            specvar1 = data_set[var11][var12][data_row]
            specvar2 = '["' + str(specvar1) + '"]'
            if new_memory != '':
                try:
                    print(specvar2)
                    exec('self.hierarchical_data' + str(new_memory) +
                         str(specvar2))
                except:
                    exec('self.hierarchical_data' + str(new_memory) +
                         '.update({"' + str(specvar1) + '" : {} })')
            else:
                exec('self.hierarchical_data' + str(new_memory) +
                     '.update({"' + str(specvar1) + '" : {} })')
        new_memory += '["' + specvar1 + '"]'
        self.createDataCategories(data_set, var_memory[1:],
                             data_column, data_row, new_memory)
    
    """
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
            *["Data", "Categorical Variables"],
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
            if self.label_opt_set[count][3] in self.submit_check:
                return
            self.submit_check.append('Data')
            self.label_opt_set[count][1].destroy()
            self.label_opt_set[count][2].destroy()
            
        if self.label_opt_set[count][3] == 'Categorical Variables':
            if self.label_opt_set[count][3] in self.submit_check:
                return
            self.submit_check.append('Categorical Variables')
            self.label_opt_set[count][1].destroy()
            self.label_opt_set[count][2].destroy()
        if len(self.submit_check) == self.final_count:
            for the_count in self.row_assets:
                for the_value in self.row_assets[the_count]:
                    try:
                        self.data_edit[self.submit_check[the_count - 1]].append(self.data[the_value])
                    except:
                        self.data_edit.update({self.submit_check[the_count - 1] : [self.data[the_value]]})
            
            self.createHierarchicalData(self.data_edit)
            frame.destroy()
    
    
    

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



        

