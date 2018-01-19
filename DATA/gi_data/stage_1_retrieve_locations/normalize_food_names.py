from pprint import pprint
import os
import re
from collections import OrderedDict


# This will normalize the food names so that any food names 
# containing trailing items enclosed in round brackets will 
# have them moved to another column


location_name_file = 'location.txt' # Look into this file, if you see a country you want to keep, add it to the next line so it can be kept track of
available_countries = ["Canada", "USA"]

def normalize_food_names(fname):
    scrubbedData_stage_0_name = fname
    scrubbedData_stage_1_name = 'ADA_GI_sql_insertion_normalized.sql'
    normalize_names(scrubbedData_stage_0_name, scrubbedData_stage_1_name)

def normalize_names(in_file_name, out_file_name):
    in_data = open(in_file_name, 'r')
    out_data = open(out_file_name,'w')
    location_name_data = open(location_name_file,'w')
    location_set = set()
    for line in in_data:
        bracket_locs = []
        # 'INSERT INTO GI_Data (food_id, food_name, glucose_gi, bread_gi, serving_size_mL, serving_size_g) VALUES ("1", "Banana cake, made with sugar", 47, 67, NULL, 60);'
        # insertion_vals = '"1", "Banana cake, made with sugar", 47, 67, NULL, 60'
        old_food_name = retrieve_food_name(line)
        bracket_locs = get_bracket_locations(old_food_name)
        if len(bracket_locs) > 0:
            country_no_brackets, line = remove_items(line, old_food_name, bracket_locs)
            line = add_column(line, "country_id", country_no_brackets)
            out_data.write(line)
            location_set.add(country_no_brackets)
        else:
            pass
    for l in location_set:
        location_name_data.write(l+"\n")

    in_data.close()
    out_data.close()
    location_name_data.close()

def add_column(line, col_name, value):
    if col_name not in get_col_names(line): # Check if the column we are adding is not in the list of columns already
        for c in available_countries:
            if c in value:
                line = line.replace(") VALUES (", ", "+ col_name +") VALUES (")
                line = line.replace(");", ", \""+c+"\");") # Only update records with 
    return line

def get_col_names(line):
    return line.split("INSERT INTO GI_Data (")[1].split(") VALUES (")[0].split(",")


def remove_items(line, old_food_name, bracket_locs):
    country_brackets = ""
    country_no_brackets = ""
    last_item = bracket_locs[len(bracket_locs)-1]
    country_brackets = old_food_name[last_item[0]:last_item[1]+1]
    country_no_brackets = old_food_name[last_item[0]+1:last_item[1]]
    if country_brackets in old_food_name and old_food_name in line:
        new_food_name = old_food_name.replace(country_brackets, "")
        line = line.replace(old_food_name, new_food_name)
    return country_no_brackets, line

def get_bracket_locations(line):
    left_bracket = []
    right_bracket = []
    bracket_locs = []
    for idx in range(len(line)):
        if line[idx] == "(":
            left_bracket.append(idx)
        if line[idx] == ")":
            right_bracket.append(idx)
    if len(left_bracket) == len(right_bracket):
        bracket_locs = list(map(lambda x,y:(x,y),left_bracket,right_bracket))
    return bracket_locs

        

def retrieve_food_name(line):
    food_name = line.split("VALUES (")[1].split(");")[0]
    food_name = food_name.split(",")[:-4]
    food_name = ",".join(food_name[1::])
    return food_name

if __name__ == "__main__":
    normalize_food_names("ADA_GI_sql_insertion.sql")