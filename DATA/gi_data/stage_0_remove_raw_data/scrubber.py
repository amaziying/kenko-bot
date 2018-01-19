from pprint import pprint
import os
import re
from collections import OrderedDict

DELIMITER = ";"

# Notes: Rows must have
    # Food ID
    # Food Name
    # glucose_gi
    # bread_gi
    # serving size (mL or g)
# Food items that do not have these fields are removed

def scrubMe(fname):
    scrubbedData_stage_0_name = fname
    scrubbedData_stage_1_name = 'ADA_GI_out_stage_1.txt'
    scrubbedData_stage_2_name = 'ADA_GI_out_stage_2.txt'
    scrubbedData_stage_3_name = 'ADA_GI_out_stage_3.txt'
    scrubbedData_stage_4_name = 'ADA_GI_out_stage_4.txt'
    scrubbedData_stage_5_name = 'ADA_GI_out_stage_5.txt'
    scrubbedData_stage_6_name = 'ADA_GI_out_stage_6.txt'
    ada_gi_sql_file_name = 'ADA_GI_sql_insertion.txt'

    scrubbedData_serving_size = 'scrubbedData_serving_size.txt' # ID + Serving size
    groupData_name = 'ADA_GI_group_data.txt'
    ada_food_group_file_name = 'ADA_food_groups.txt'

    extractUniqueIDs(scrubbedData_stage_0_name, scrubbedData_stage_1_name)
    extract_name_GI(scrubbedData_stage_1_name, scrubbedData_stage_2_name)
    concat_name_GI(scrubbedData_stage_2_name, scrubbedData_stage_3_name)
    seperateIDs(scrubbedData_stage_3_name, scrubbedData_stage_4_name)
    clean_names(scrubbedData_stage_4_name, scrubbedData_stage_5_name)

    extract_serving_size(scrubbedData_stage_1_name, scrubbedData_serving_size)
    combine_serving_size(
        scrubbedData_stage_5_name, 
        scrubbedData_serving_size, 
        scrubbedData_stage_6_name)
    convert_to_sql(scrubbedData_stage_6_name, ada_gi_sql_file_name)
    get_group_ranges(scrubbedData_stage_0_name, groupData_name)
    convert_to_sql_GroupData("ADA_GI_group_data_final.txt", ada_food_group_file_name)

def convert_to_sql_GroupData(in_file_name, out_file_name):
    target_table_name = "GI_Data";
    in_data = open(in_file_name, 'r')
    out_data = open(out_file_name,'w')

    in_data.close()
    out_data.close()

def convert_to_sql(in_file_name, out_file_name):
    target_table_name = "GI_Data";
    in_data = open(in_file_name, 'r')
    out_data = open(out_file_name,'w')
    row = []
    out_data.write("DROP TABLE IF EXISTS "+target_table_name+";\n")
    out_data.write("CREATE TABLE GI_Data(food_id VARCHAR(225), food_name VARCHAR(225), glucose_gi INT, bread_gi INT, serving_size_mL INT, serving_size_g INT);\n")
    for line in in_data:
        row = line.split(DELIMITER)
        food_id = "\""+row[0]+"\""
        food_name = "\""+row[1]+"\""
        glucose_gi = row[2]
        bread_gi = row[3]
        serving_size_mL = row[4].strip()
        if len(serving_size_mL) == 0:
            serving_size_mL = "NULL"
        serving_size_g = row[5].strip()
        if len(serving_size_g) == 0:
            serving_size_g = "NULL"
        out_data.write("INSERT INTO "+target_table_name+" (food_id, food_name, glucose_gi, bread_gi, serving_size_mL, serving_size_g) VALUES (" + food_id + ", " + food_name + ", " + glucose_gi  + ", " + bread_gi + ", " + serving_size_mL + ", " + serving_size_g+");\n")
    in_data.close()
    out_data.close()

def extractUniqueIDs(in_file_name, out_file_name):
    # This will only consider food items that 
    in_data = open(in_file_name, 'r')
    out_data = open(out_file_name,'w')
    uniqueIDs = {}
    for line in in_data:
        if re.match('^\d{1,4}\s', line):
            currFoodID = re.match('^\d{1,4}', line).group(0)
            if currFoodID not in uniqueIDs: # Only add unique food ids
                uniqueIDs[currFoodID] = 1
                out_data.write(line)
    in_data.close()
    out_data.close()

def extract_serving_size(in_file_name, out_file_name):
    # Split on Subjects (type & number)
    # This will only consider food items that are type NORMAL**
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    remove_last_two_units_regex = '\s[\d]+\s[\d]+$'
    find_ml_regex = '[\d]+[\s]*mL$'
    find_g_regex = '[\d]+$'
    id_regex = '^\d{1,4}\s'

    for line in in_data:
        last_two_match = re.findall(remove_last_two_units_regex, line)
        if last_two_match:
            line = line.replace(last_two_match[0], '')

        
        is_ml = re.findall(find_ml_regex, line)
        is_g = re.findall(find_g_regex, line)
        id_match = re.findall(id_regex, line)

        if id_match:
            food_id = id_match[0]
            if is_ml:
                line = food_id.strip() + DELIMITER + is_ml[0].strip() + DELIMITER + '' + "\n"
                out_data.write(line)
            elif is_g:
                line = food_id.strip() + DELIMITER + '' + DELIMITER + is_g[0].strip() +" g" + "\n"
                out_data.write(line)
        
        id_match = re.findall(id_regex, line)
        if id_match:
            food_id = id_match[0]
        
    in_data.close()
    out_data.close()

def combine_serving_size(in_file_name_1, serving_size_data, out_file_name):
    in_data = open(in_file_name_1,'r')
    in_data_ss = open(serving_size_data,'r')
    out_data = open(out_file_name,'w')
    ss_dict = {}
    currSplit = []
    for line in in_data_ss:
        currSplit = line.split(DELIMITER)
        food_id = currSplit[0].strip()
        food_ml = currSplit[1].replace("mL", '').strip()
        food_g = currSplit[2].replace("g", '').strip()
        if food_id not in ss_dict:
            ss_dict[food_id] = [food_ml, food_g]
    
    for line in in_data:
        food_id = line.split(DELIMITER)[0]
        if food_id in ss_dict:
            out_data.write(line.rstrip() + DELIMITER + DELIMITER.join(ss_dict[food_id]) + "\n")

    in_data.close()
    in_data_ss.close()
    out_data.close()

def extract_name_GI(in_file_name, out_file_name):
    # Split on Subjects (type & number)
    # This will only consider food items that are type NORMAL**
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    for line in in_data:
        out = line.split("Normal,")
        if len(out) == 2: # If there is actually a split
            out = out[0]+"\n"
            out_data.write(out)
    in_data.close()
    out_data.close()

def concat_name_GI(in_file_name, out_file_name):
    # Split on Subjects (type & number)
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    GI_regex = '\s[0-9\+\-]*$'
    for line in in_data:
        line = line.rstrip()
        GI_subs_match = re.findall(GI_regex, line)[0] # This is the bread GI
        if GI_subs_match:
            if '+-' in GI_subs_match:
                GI_bread = GI_subs_match.split('+-')[0]
            else:
                GI_bread = GI_subs_match
        out = line.split(GI_subs_match)[0]
        if out:
            GI_subs_match = re.findall(GI_regex, out)[0] # This is the glucose GI, TODO: Add this in
            if GI_subs_match:
                if '+-' in GI_subs_match:
                    GI_glucose = GI_subs_match.split('+-')[0]
                else:
                    GI_glucose = GI_subs_match
                name = line.split(GI_subs_match)[0]
                if name:
                    out = name + DELIMITER + GI_glucose.strip() + DELIMITER + GI_bread.strip() + "\n"
                    out_data.write(out)
    in_data.close()
    out_data.close()

def seperateIDs(in_file_name, out_file_name):
    # Split on Subjects (type & number)
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    for line in in_data:
        currFoodID_match = re.match('^\d{1,4}\s', line)
        if currFoodID_match:
            currFoodID = currFoodID_match.group(0)
            newCurrFoodID = currFoodID.strip()+DELIMITER
            line = line.replace(currFoodID, newCurrFoodID)
        out = line
        out_data.write(out)
    in_data.close()
    out_data.close()

def clean_names(in_file_name, out_file_name):
    # Split on Subjects (type & number)
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    name_regex = '(?<=;)(.*)(?=;[\d]+;)'
    for line in in_data:
        
        name_match = re.findall(name_regex, line)
        if name_match:
            name = name_match[0]
            new_name = name.strip()
            line = line.replace(name, new_name)

        # Trim trailing commas
        name_match = re.findall(name_regex, line)
        if name_match:
            name = name_match[0]
            if name[-1] == ",":
                new_name = name[0:-1]
                line = line.replace(name, new_name)

        out = line
        out_data.write(out)
    in_data.close()
    out_data.close()

def get_group_ranges(in_file_name, out_file_name):
    group_dict = {}
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    group_match_regex = '^[\(\),\/\-a-zA-Z0-9\&\s]+$'
    for line in in_data:
        # print line
        group_name_match = re.findall(group_match_regex, line)
        # A group name is one that is all letters, and begins with a capital letter
        if group_name_match and len(group_name_match[0]) > 1 and group_name_match[0][0].isupper():
            group_name = group_name_match[0]
            group_name = group_name.lower().rstrip()
            if group_name not in group_dict:
                group_dict[group_name] = []

    in_data.close()
    in_data = open(in_file_name,'r')

    #Build ranges of food ids per group
    uniqueIDs = {}
    curr_group = ""
    for line in in_data:
        if re.match('^\d{1,4}\s', line) or re.findall(group_match_regex, line):
            if re.findall(group_match_regex, line):
                curr_group_name_match = re.findall(group_match_regex, line)
                if curr_group_name_match and len(curr_group_name_match[0]) > 1 and curr_group_name_match[0][0].isupper():
                    curr_group = curr_group_name_match[0]
                    curr_group = curr_group.lower().rstrip()
            if re.match('^\d{1,4}\s', line):
                # It is a food
                currFoodID = re.match('^\d{1,4}', line).group(0)
                if currFoodID not in uniqueIDs: # Only add unique food ids
                    uniqueIDs[currFoodID] = 1
                    group_dict[curr_group].append(int(currFoodID))

    # We are only interested in the max and min of each food group
    for key in group_dict:
        if len(group_dict[key]) > 0: # Ignore empty lists
            group_dict[key] = [min(group_dict[key]),max(group_dict[key])]
    
    # Create a list of tuples for easier manipulation
    out_dict = []
    for key in group_dict:
        if len(group_dict[key]) > 0 and len(group_dict[key]) == 2:
            min_idx = group_dict[key][0]
            max_idx = group_dict[key][1]
            out_dict.append((key,min_idx,max_idx))
    
    #Sort the tuples
    out_dict = sorted(out_dict,key=lambda x:x[1])
    for item in out_dict:
        key = item[0]
        min_idx = str(item[1])
        max_idx = str(item[2])
        out_data.write(key + DELIMITER + min_idx + DELIMITER + max_idx + "\n")

    in_data.close()
    out_data.close()
if __name__ == "__main__":
    scrubMe("ADA_GI_raw.txt")