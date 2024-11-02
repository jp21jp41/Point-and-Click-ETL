"""
Creating a Statistical Result Table from a Point-and-Click Interface
Version 2.2.11
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
        self.comparisons = {}
        self.treeview_set = {}
        self.treeview_counts = {}
        
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
    
    def data_submission(self, the_string, lost_point, previous_tree):
        print('Passed Data Submission Checkpoint')
        self.comparisons.update({lost_point : previous_tree})
    
    def to_treeview(self, the_string, lost_point = '00', previous_tree = None):
        if previous_tree != None:
            item = previous_tree.selection()[0]
            tree_value = previous_tree.item(previous_tree.focus())['values'][0]
        print(lost_point)
        print(int(lost_point[1]))
                    
        # configure the grid layout
        self.tkwindow.rowconfigure(0, weight = 3)
        self.tkwindow.rowconfigure(1, weight = 3)
        self.tkwindow.columnconfigure(0, weight = 3)
        
        exec('tree' + str(lost_point) + ' = ttk.Treeview(self.tkwindow)')
        exec(str(self.raw_name) + '.row_assets.update({"' + str(lost_point) + '" : tree' + str(lost_point) + ' })')
        exec(str(self.raw_name) + '.row_assets["' + str(lost_point) + '"].heading("#0", text="Make a selection for the first comparison item", anchor=tk.NW)')
        total_count = 0
        new_lost_point = str(lost_point[0]) + str(int(lost_point[1]) + 1)
        num_rows = [x for x in np.arange(0, len(self.data_edit['qtv_cols'][0]))]
        for num in num_rows:
            treeview_set_piece_accumulator = ''
            for value in self.data_edit:
                value_nums = [x for x in np.arange(0, len(self.data_edit[value]))]
                edit_count = 0
                for number in value_nums:
                    value_point = self.data_edit[value][number][num]
                    value_name = self.data_edit[value][number].name
                    exec('if value not in list(' + str(self.raw_name) +
                         '.treeview_set' + str(treeview_set_piece_accumulator) + '.keys()): \n    ' +
                        str(self.raw_name) + '.treeview_set.update({value_name : {}}) \n' +
                        str(self.raw_name) + '.treeview_set' + str(treeview_set_piece_accumulator) +
                             '.update({value_name : {}}) \n' +
                        str(self.raw_name) + '.treeview_counts' + 
                             str(treeview_set_piece_accumulator) + '.update({value_name : {}}) \n' +
                             'try: \n    ' +
                             str(self.raw_name) + '.treeview_set' + 
                             str(treeview_set_piece_accumulator) + '[value_name][value_point][0] += 1 \n' +
                             'except: \n    ' + 
                             str(self.raw_name) + '.treeview_counts' + 
                             str(treeview_set_piece_accumulator) + '[value_name].update({value_point : 0}) \n' +
                             'print(10) \n' +
                             str(self.raw_name) + '.treeview_counts' +
                             str(treeview_set_piece_accumulator) + 
                             '[value_name][value_point] = len(self.treeview_counts[value_name]) - 1 \n' + 
                             'print(12) \n' +
                             str(self.raw_name) + '.treeview_set' +
                             str(treeview_set_piece_accumulator) + '[value_name].update({value_point : [0, {}]}) \n' + 
                             'print(14) \n' +
                             'tree' + str(lost_point) + 
                             '.insert("", tk.END, text = value_point, values = value_name, iid = total_count, open = False) \n' +
                             'print(16) \n' +
                            'if edit_count > 0: \n    ' +
                            'print(18) \n' +
                            'treeview_set_piece_accumulator += \'["' + str(value_name) + '"]["' + str(value_point) + '"]\' \n' +
                            'total_count += 1 \n' + 
                            'print(total_count)')
                    
    
        # Potentially Defunct: Individual Iteration
        """
        for num in num_rows:
            try:
                cat_row_nums = [x for x in np.arange(0, len(self.data_edit['cat_rows']))]
                cat_row_count = 0
                for cat_row in cat_row_nums:
                    cat_row_point = self.data_edit['cat_rows'][cat_row][num]
                    cat_row_name = self.data_edit['cat_rows'][cat_row].name
                    if cat_row_name not in list(self.treeview_set.keys()):
                        self.treeview_set.update({cat_row_name : {}})
                        self.treeview_counts.update({cat_row_name : {}})
                    try:
                        self.treeview_set[cat_row_name][cat_row_point][0] += 1
                    except:
                        self.treeview_counts[cat_row_name].update({cat_row_point : 0})
                        self.treeview_counts[cat_row_name][cat_row_point] = len(self.treeview_counts[cat_row_name]) - 1
                        self.treeview_set[cat_row_name].update({cat_row_point : [0, {}]})
                        print('40')
                        exec('tree' + str(lost_point) + '.insert("", tk.END, text = cat_row_point, values = cat_row_name, iid = total_count, open = False)')
                        total_count += 1
                        cat_row_count += 1
                    cat_row_parent_value = self.treeview_counts[cat_row_name][cat_row_point]
                    treeview_set_spot = self.treeview_set[cat_row_name][cat_row_point]
                    treeview_point = treeview_set_spot[1]
                    cat_row_value = treeview_set_spot[0]
                
            except:
                print('pass')
        
        """
        
        # Defunct: Nested Iteration
        """
        for num in num_rows:
            try:
                cat_row_nums = [x for x in np.arange(0, len(self.data_edit['cat_rows']))]
                cat_row_count = 0
                for cat_row in cat_row_nums:
                    cat_row_point = self.data_edit['cat_rows'][cat_row][num]
                    cat_row_name = self.data_edit['cat_rows'][cat_row].name
                    if cat_row_name not in list(self.treeview_set.keys()):
                        self.treeview_set.update({cat_row_name : {}})
                        self.treeview_counts.update({cat_row_name : {}})
                    try:
                        self.treeview_set[cat_row_name][cat_row_point][0] += 1
                    except:
                        self.treeview_counts[cat_row_name].update({cat_row_point : 0})
                        self.treeview_counts[cat_row_name][cat_row_point] = len(self.treeview_counts[cat_row_name]) - 1
                        self.treeview_set[cat_row_name].update({cat_row_point : [0, {}]})
                        print('40')
                        exec('tree' + str(lost_point) + '.insert("", tk.END, text = cat_row_point, values = cat_row_name, iid = total_count, open = False)')
                        total_count += 1
                        cat_row_count += 1
                    cat_row_parent_value = self.treeview_counts[cat_row_name][cat_row_point]
                    treeview_set_spot = self.treeview_set[cat_row_name][cat_row_point]
                    treeview_point = treeview_set_spot[1]
                    cat_row_value = treeview_set_spot[0]
                    try:
                        cat_col_nums = [x for x in np.arange(0, len(self.data_edit['cat_cols']))]
                        for cat_col in cat_col_nums:
                            cat_col_point = self.data_edit['cat_cols'][cat_col][num]
                            cat_col_name = self.data_edit['cat_cols'][cat_col].name
                            treeview_point.update({cat_col_name : {cat_col_point : {}}})
                            treeview_point = treeview_point[cat_col_name][cat_col_point]
                            exec('tree' + str(lost_point) + '.insert("", tk.END, text = cat_col_point, values = cat_col_name, iid = total_count, open = False)')
                            total_count += 1
                    except:
                        try:
                            qtv_row_acc = 0
                            qtv_row_nums = [x for x in np.arange(0, len(self.data_edit['qtv_rows']))]
                            for qtv_row in qtv_row_nums:
                                qtv_row_point = self.data_edit['qtv_rows'][qtv_row][num]
                                qtv_row_name = self.data_edit['qtv_rows'][qtv_row].name
                                if qtv_row_name not in list(treeview_point.keys()):
                                    treeview_point.update({qtv_row_name : {}})
                                    self.treeview_counts.update({qtv_row_name : {}})
                                try:
                                    treeview_point[qtv_row_name][qtv_row_point][0] += 1
                                except:
                                    self.treeview_counts[qtv_row_name].update({qtv_row_point : 0})
                                    self.treeview_counts[qtv_row_name][qtv_row_point] = len(self.treeview_counts[qtv_row_name]) - 1
                                    treeview_point[qtv_row_name].update({qtv_row_point : [0, []]})
                                    exec('tree' + str(lost_point) + '.insert("", tk.END, text = qtv_row_point, values = qtv_row_name, iid = total_count, open = False)')
                                    exec('tree' + str(lost_point) + '.move(total_count, cat_row_parent_value, qtv_row_acc)')
                                    total_count += 1
                                treeview_parent_value = self.treeview_counts[qtv_row_name][qtv_row_point]
                                treeview_set_spot = treeview_point[qtv_row_name][qtv_row_point]
                                treeview_point = treeview_set_spot[1]
                                qtv_row_value = treeview_set_spot[0]
                                qtv_row_acc += 1
                                try:
                                    qtv_col_acc = 0
                                    qtv_col_nums = [x for x in np.arange(0, len(self.data_edit['qtv_cols']))]
                                    for qtv_col in qtv_col_nums:
                                        qtv_col_point = self.data_edit['qtv_cols'][qtv_col][num]
                                        qtv_col_name = self.data_edit['qtv_cols'][qtv_col].name
                                        if qtv_col_name not in list(treeview_point):
                                            print(len(treeview_point))
                                            prev_parent_value = treeview_parent_value
                                            treeview_parent_value = len(treeview_point)
                                            print('030')
                                            treeview_point.append(qtv_col_name)
                                            exec('tree' + str(lost_point) + '.insert("", tk.END, text = qtv_col_name, values = qtv_col_point, iid = total_count, open = False)')
                                            exec('tree' + str(lost_point) + '.move(total_count, cat_row_count, qtv_col_acc)')
                                            total_count += 1
                                            qtv_col_acc += 1
                                except:
                                    pass
                        except:
                            pass
                            
            except:
                print('pass')
                
        """
        
        # Defunct: Iterative Component
        """elif 'cat_rows' in self.data_edit:
            for cat_row in self.data_edit['cat_rows']:
                for value in cat_row:
                    print(value)
                    exec('tree' + str(lost_point) + '.insert("", tk.END, text = value, values = cat_row.name, iid = total_count, open = False)')
                    total_count += 1
        elif 'cat_cols' in self.data_edit:
            for cat_col in self.data_edit['cat_rows']:
                for value in cat_col:
                    exec('tree' + str(lost_point) + '.insert("", tk.END, text = value, values = cat_col.name, iid = total_count, open = False)')
                try:
                    exec('tree' + str(lost_point) + '.move(total_count, 0, total_count - len(cat_col_nums))')
                except:
                    pass
                total_count += 1
        
        
        data_item_set = [x for x in np.arange(0, len(self.data_edit[the_string]))]
        for item_number in data_item_set:
            exec('tree' + str(lost_point) + '.insert("", tk.END, text = self.data_edit[the_string][item_number].name, iid = total_count, open = False)')
            try:
                exec('tree' + str(lost_point) + '.move(total_count, total_count - len(cat_col_nums) - len(cat_row_nums), total_count - len(cat_col_nums))')
            except:
                try:
                    exec('tree' + str(lost_point) + '.move(total_count, 0, total_count - len(cat_col_nums))')
                except:
                    try:
                        exec('tree' + str(lost_point) + '.move(total_count, 0, total_count - len(cat_row_nums))')
                    except:
                        pass
            total_count += 1
            """
        for check_item in self.row_assets:
            if (
                    'qtv' in str(check_item)) or (
                        'cols' in str(check_item)) or (
                            'cat' in str(check_item)) or (
                                'rows' in str(check_item)):
                for item in self.row_assets[check_item]:
                    self.row_assets[check_item][item][0].grid_forget()
            if ('new_button' in str(check_item)):
                self.row_assets[check_item].grid_forget()
            self.row_assets['To Treeview'].grid_forget()
        exec('tree' + str(lost_point) + '.grid(row = 0 + int(lost_point[1]), column = 0, sticky = tk.NSEW)')
        if str(lost_point) > '00':
            exec('tree' + str(lost_point) + '.bind("<Double 1>", lambda x: ' + str(self.raw_name) + '.data_submission("' + str(the_string) + '", "' + str(new_lost_point) + 
                 '", ' + str(self.raw_name) + '.row_assets["' + str(lost_point) + '"]))')
            self.comparisons.update({lost_point : previous_tree})
        else:
            exec('tree' + str(lost_point) + '.bind("<Double 1>", lambda x: ' + str(self.raw_name) + '.to_treeview("' + str(the_string) + '", "' + str(new_lost_point) + 
                 '", ' + str(self.raw_name) + '.row_assets["' + str(lost_point) + '"]))')
        self.tkwindow.mainloop()
        
    def check_item_display(self, the_string):
        new_asset_count = 0
        if 'To Treeview' in self.row_assets:
            pass
        else:
            to_treeview_button = ttk.Button(self.tkwindow,
                                        text = "Continue",
                                        )
            to_treeview_button.grid(row = 10, column = 0)
            to_treeview_button.bind("<Button 1>", lambda x: self.to_treeview(the_string))
            self.row_assets.update({'To Treeview' : to_treeview_button})
        try:
            for asset_name in self.row_assets:
                if asset_name in self.name_hierarchy:
                    for item in self.row_assets[asset_name]:
                        self.row_assets[asset_name][item][0].destroy()
                    del self.row_assets[asset_name]
        except:
            pass
        if the_string == 'qtv_rows':
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
        
        
        
        if the_string == 'qtv_cols':
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
                        check_item_str += ' Rows'
                    elif 'col' in check_item:
                        check_item_str += ' Columns'
                    exec(str(check_item) + '_button = ttk.Button(self.tkwindow, ' +
                         'text = "' + str(check_item_str) + '",' +
                         ' cursor = "hand2", width = 40)')
                    exec(str(check_item) + '_button.grid(row = ' +
                         str(check_count) + ', column = 0)')
                    exec(str(check_item) + '_button.bind("<Button 1>",' + 
                         ' lambda x: ' + str(self.raw_name) + 
                         '.check_item_display("' + str(check_item) + '"))')
                    exec(str(self.raw_name) + 
                         '.row_assets.update({"new_button' + 
                         str(check_count) + '" : ' + 
                         str(check_item) + '_button})')
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



        
