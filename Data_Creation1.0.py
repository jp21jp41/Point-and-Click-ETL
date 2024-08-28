# Creating a Statistical Result Table from a Point-and-Click Interface
# Version 1.0
# Justin Pizano

import pandas as pnd
import math
import tkinter as tk
import numpy as np
import scipy.stats as stats
from datetime import datetime


data_file = 'C:/Users\justi\OneDrive\Documents\Volunteering\APDREO_07-18-2024 19-58-59-47_timeSeries.csv'
data_set = pnd.read_csv(data_file)

# Function to create a list
def createList(start, end):
    return [item for item in range(start, end + 1)]

data_file





## Class for a given country
class Country:
    def __init__(self, name):
        self.name = name
        self.IndicatorData = {}
    
    
    def addIndicators(self, dex, indicators):
        self.IndicatorData.update({dex : indicators})
    
    


## Function to create a list of years
def yeardata(years, data, dict):
    dict.update({years[0] : Year(years[0], data[0])})
    if len(years) == 1 or len(data) == 1:
        if len(years) != len(data):
            print('There will either be missing data or missing years because of an excess')
        return
    yeardata(years[1:], data[1:], dict)
    
    

     

## class for a given Indicator Data set
class IndicatorData:
    def __init__(self, name, dex, country, years, data):
        self.name = name
        self.dex = dex
        self.years = years
        self.data = data
        self.country = country
        self.yeardata = {}
        yeardata(years, data, self.yeardata)
    
    
    def add_to_country(self, country, dex):
        country.addIndicators(dex, self)
    



## class for a given year
class Year:
    def __init__(self, year, data):
        self.year = year
        self.data = data
        self.leap = False



        

class YearAggregate:
    def __init__(self, year, data, indicator):
        self.year = year
        self.data = data
        self.indicator = indicator
        self.sum = data[0]
    def addData(self, new_data):
        self.data.append(new_data)
        self.sum += new_data
    def computeAvg(self, sum, data):
        self.avg = self.sum / len(self.data)



"""
Documentation

This project is a data-oriented project.
The goal is to make a sort of streamlined
program that can select from countries and,
given the year and the category of data,
can compare countries to see whether or
not they have statistically significant
differences of values.
"""

"""
Data should be made such that:
   Each country should have indicators.
   Each indicator should have years listed.
   If a year is listed as "NaN", then
   it should listed as a year of a given
   country's indicator.

"""

## Note to self: Use anaconda or another
## OS to test programs on

# Convert countries to variables
def name_convert(name):
    name_nums = createList(0, len(name) - 1)
    for entry in name_nums:
        if name[entry].isspace():
            name = name[:name.index(' ')] + '_' + name[name.index(' ') + 1:]
    return name.lower()



# List of number entries of the data list
data_num_list = createList(0, len(data_set) - 1)
data_num_list
data_year_entries = []

for column in data_set.columns:
    try:
        data_year_entries.append(datetime.strptime(column, '%Y').year)
    except ValueError:
        pass


print(data_year_entries)


indicator_aggregate = {}
country_list = {}
dexdict = {}

aggregate_data = []
aggregate_check = {}

country_strings = []
country_selector = {}

revdex = {}
indicator_index = []

specified_data = {}
specified_years = {}
col_count = 0
numbered_countries = []
row_count = 0

for column in data_set.columns:
    col_count += 1
    for row in data_num_list:
        if row_count < len(data_num_list):
            specified_data.update({row : []})
            specified_years.update({row : []})
        if column == 'Indicator Name':
            the_indicator_name = data_set[column][row]
            indicator_index.append(the_indicator_name)
            if the_indicator_name not in dexdict:
                dexdict.update({the_indicator_name : row})
                revdex.update({row : the_indicator_name})
                indicator_aggregate.update({the_indicator_name : []})
        if column == 'Country Name':
            country_string = data_set[column][row]
            country_strings.append(country_string)
            country_name = name_convert(country_string)
            if country_name not in country_list:
                the_country = Country(country_string)
                country_list.update({country_name : the_country})
                country_selector.update({country_string : country_name})
            else:
                the_country = country_list[country_name]
        try:
            column == datetime.strptime(column, "%Y").year
            data_point = data_set[column][row]
            if not math.isnan(data_point):
                specified_data[row].append(data_point)
                specified_years[row].append(column)
                if column not in aggregate_check:
                    aggregate_check.update({column : {indicator_index[row] : YearAggregate(column, [data_point], indicator_index[row])}})
                elif indicator_index[row] not in aggregate_check[column]:
                    aggregate_check[column].update({indicator_index[row] : YearAggregate(column, [data_point], indicator_index[row])})
                else:
                    aggregate_check[column][indicator_index[row]].addData(data_point)
        except ValueError:
            pass
        row_count += 1
        if col_count == len(data_set.columns):
            print(indicator_index[row])
            entry_indicator = IndicatorData(indicator_index[row], row, country_strings[row], specified_years[row], specified_data[row])
            print(entry_indicator)
            entry_indicator.add_to_country(country_list[country_selector[country_strings[row]]], dexdict[indicator_index[row]])






"""
---------- Outdated version -----------
# For-loop to create a dictionary of country name keys 
# with country object values
for row in data_num_list:
    the_indicator_name = data_set.loc[row].iloc[2]
    if the_indicator_name not in dexdict:
        dexdict.update({the_indicator_name : row})
    country_string = data_set.loc[row].iloc[0]
    country_strings.append(country_string)
    country_name = name_convert(country_string)
    if country_name not in country_list:
        the_country = Country(country_string)
        country_list.update({country_name : the_country})
        country_selector.update({country_string : country_name})
    else:
        the_country = country_list[country_name]
    specified_data = []
    specified_years = []
    for year in data_year_entries:
        data_point = data_set.loc[row].iloc[year]
        current_year = data_set.columns[year]
        if not math.isnan(data_point):
            specified_data.append(data_point)
            specified_years.append(current_year)
            if the_indicator_name not in indicator_aggregate:
                indicator_aggregate.update({the_indicator_name : []})
            indicator_aggregate[the_indicator_name].append(data_point)
            if current_year not in aggregate_check:
                aggregate_check.update({current_year : {the_indicator_name : YearAggregate(current_year, [data_point], the_indicator_name)}})
            elif the_indicator_name not in aggregate_check[current_year]:
                aggregate_check[current_year].update({the_indicator_name : YearAggregate(current_year, [data_point], the_indicator_name)})
            else:
                aggregate_check[current_year][the_indicator_name].addData(data_point)
            
    entry_indicator = IndicatorData(the_indicator_name, row, the_country, specified_years, specified_data)
    entry_indicator.add_to_country(the_country, dexdict[the_indicator_name])
    



ratio_test = np.var(data_1_test) / np.var(data_2_test)
ratio_test

if 1/4 < ratio_test < 4:
    tresult_test = stats.ttest_ind(data_1_test, data_2_test, equal_var = True)
else:
    tresult_test = stats.ttest_ind(data_1_test, data_2_test, equal_var = False)



Note: Indicator names have to be made such a way
that the data can be easily accessible
(likely through an key system of integers).
The same is possible given the countries

"""


class FinalDataStorage:
    def __init__(self, comparisons = [], statistics = [], test_types = [], pvalues = [], results = []):
        self.comparisons = comparisons
        self.statistics = statistics
        self.test_types = test_types
        self.pvalues = pvalues
        self.results = results
    
    def addtoStorage(self, new_comparisons = [], new_statistics = [], new_test_types = [], new_pvalues = [], new_results = []):
        self.comparisons.append(new_comparisons)
        self.statistics.append(new_statistics)
        self.test_types.append(new_test_types)
        self.pvalues.append(new_pvalues)
        self.results.append(new_results)




class StatisticalStorage:
    def __init__(self, null_hypotheses = [], alt_hypotheses = [], 
    statistics = [], test_types = [], pvalues = [], results = []):
        self.null_hypotheses = null_hypotheses
        self.alt_hypotheses = alt_hypotheses
        self.statistics = statistics
        self.test_types = test_types
        self.pvalues = pvalues
        self.results = results
    
    def addtoStorage(new_null_hypotheses, new_alt_hypotheses, new_statistics, new_test_types, new_pvalues, new_results):
        self.null_hypotheses.append(new_null_hypotheses)
        self.alt_hypotheses.append(new_alt_hypotheses)
        self.statistics.append(new_statistics)
        self.test_types.append(new_test_types)
        self.pvalues.append(new_pvalues)
        self.results.append(new_results)
    


final_data = FinalDataStorage()
added_statistics = StatisticalStorage()


import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# create root window
root = tk.Tk()
root.title('IMF Data Analytics')
root.geometry('1000x800')

# configure the grid layout
root.rowconfigure(0, weight = 3)
root.columnconfigure(0, weight = 3)

root.columnconfigure(1, weight = 3)



# create a treeview
tree = ttk.Treeview(root)
tree.heading('#0', text='Make a selection for the first comparison item', anchor=tk.NW)


def spec_vs_aggregate(event):
    spec_agg_button.grid_forget()
    
    
    
    total_count = 0
    country_count = 0
    
    for country in country_list:
        tree.insert('', tk.END, text = country_list[country].name, iid = total_count, open = False)
        total_count += 1
    
    country_count = 0
    
    for country in country_list:
        indicator_count = 0
        for indicator in country_list[country].IndicatorData:
            tree.insert('', tk.END, text = country_list[country].IndicatorData[indicator].name, iid = total_count, open = False)
            tree.move(total_count, country_count, indicator_count)
            total_count += 1
            indicator_count += 1
        country_count += 1
    
    indicator_count = 0
    
    for country in country_list:
        for indicator in country_list[country].IndicatorData:
            year_count = 0
            for year in country_list[country].IndicatorData[indicator].years:
                tree.insert('', tk.END, text = year, values = dexdict[country_list[country].IndicatorData[indicator].name], tags = country, iid = total_count, open = False)
                tree.move(total_count, country_count + indicator_count, year_count)
                total_count += 1
                year_count += 1
            indicator_count += 1
    tree.grid(row = 0, column = 0, sticky = tk.NSEW)
    tree.bind('<Double 1>', lambda x: doubleclick00(x, tree))


spec_agg_button = ttk.Button(root,
                       text="Compare a country's year to a year aggregate of a given indicator",
                       cursor="hand2",
                       width = 40)

spec_agg_button.grid(row = 0, column = 0)
spec_agg_button.bind('<Button 1>', spec_vs_aggregate)




# ____________________________________________ #

def doubleclick00(event, selected_tree):
    try:
        comparison_button.grid_forget()
        selection_box2.grid_forget()
        selection_box2.delete('1.0', 'end')
    except:
        pass
    try:
        tree1.destroy()
    except:
        pass
    tree1 = ttk.Treeview(root)
    tree1.heading('#0', text = 'Make a selection for the second comparison item', anchor = tk.NW)
    item = tree.selection()[0]
    revvalue = tree.item(tree.focus())['values'][0]
    selected_country = tree.item(tree.focus())['tags'][0]
    selected_year = tree.item(tree.focus())['text']
    full_selection = []
    full_selection.append(country_list[selected_country].name)
    full_selection.append(revdex[revvalue])
    full_selection.append(selected_year)
    tree1.insert('', tk.END, text = revdex[revvalue], iid = 0, open = False)
    tree1.insert('', tk.END, text = selected_year, values = revvalue, tags = 'check_year', iid = 1, open = False)
    tree1.move(1, 0, 0)
    tree1.insert('', tk.END, text = "Total", iid = 2, values = revvalue, tags = 'check_indicator', open = False)
    tree1.move(2, 0, 1)
    
    full_selection_string = country_list[selected_country].name + ', ' + revdex[revvalue] + ', ' + selected_year
    tree1.grid(row = 0, column = 1, sticky = tk.NSEW)
    selection_box1 = tk.Text(root, height = 5, width = 30)
    selection_box1.grid(row = 1, column = 0, sticky = tk.NW)
    selection_box1.insert('end', full_selection_string)
    root.rowconfigure(1, weight = 1)
    tree1.bind('<Double 1>', lambda x: doubleclick10(x, tree1, full_selection, full_selection_string))


comparison_button = ttk.Button(root,
                       text='Submit',
                       cursor="hand2",
                       width=15)

selection_box2 = tk.Text(root, height = 5, width = 30, spacing1 = 0, padx = 0, pady = 0)

def doubleclick10(event, selected_tree, selection, selection_string):
    try:
        comparison_button.grid_forget()
        selection_box2.delete('1.0', 'end')
    except:
        pass
    new_full_selection = []
    new_full_selection_string = ''
    if selected_tree.item(selected_tree.focus())['tags'][0] == 'check_indicator':
        new_full_selection_string = revdex[selected_tree.item(selected_tree.focus())['values'][0]] + ', total'
        new_full_selection.append(revdex[selected_tree.item(selected_tree.focus())['values'][0]])
    if selected_tree.item(selected_tree.focus())['tags'][0] == 'check_year':
        new_full_selection_string = revdex[selected_tree.item(selected_tree.focus())['values'][0]] + ', ' + selected_tree.item(selected_tree.focus())['text']
        new_full_selection.append(revdex[selected_tree.item(selected_tree.focus())['values'][0]])
        new_full_selection.append(selected_tree.item(selected_tree.focus())['text'])
    selection_box2.grid(row = 1, column = 1, sticky = tk.NE)
    selection_box2.insert('end', new_full_selection_string)
    comparison_button.grid()
    comparison_button.bind('<Button 1>', lambda x: clickstorage(x, selection, 
    selection_string, new_full_selection, new_full_selection_string))



def clickstorage(event, selection1, selection1string, selection2, selection2string):
    print(
    country_list[country_selector[
    selection1[0]]].IndicatorData[dexdict[
    selection1[1]]].yeardata[selection1[2]])
    print('First')
    print(selection1string)
    print(selection1)
    print('Second')
    print(selection2string)
    print(selection2)
    the_year = country_list[country_selector[
    selection1[0]]].IndicatorData[
    dexdict[selection1[1]]].yeardata[selection1[2]]
    if len(selection2) == 1:
        created_data = indicator_aggregate[selection2[0]]
    else:
        created_data = aggregate_check[selection2[1]][selection2[0]].data
    stat_result = stats.ttest_1samp(created_data, the_year.data)
    print(stat_result)
    if stat_result.pvalue <= 0.05:
        the_result = "There is no significant difference between " + selection1string + " and " + selection2string
    else:
        the_result = "There is a significant difference between " + selection1string + " and " + selection2string
    final_data.addtoStorage(selection1string + ' vs ' + selection2string, stat_result.statistic, 'One Sample T-test', stat_result.pvalue, the_result)
    print(final_data)



# run the app
root.mainloop()


