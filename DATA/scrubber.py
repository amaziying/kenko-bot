from pprint import pprint
import os
import re
from collections import OrderedDict

DELIMITER = ";"

# Notes: There 

def scrubMe(fname):
    scrubbedData_stage_0_name = fname
    scrubbedData_stage_1_name = 'output_stage_1.txt'
    scrubbedData_stage_2_name = 'output_stage_2.txt'
    scrubbedData_stage_3_name = 'output_stage_3.txt'
    scrubbedData_stage_4_name = 'output_stage_4.txt'
    scrubbedData_stage_5_name = 'output_stage_5.txt'
    groupData_name = 'group_data.txt'

    extractUniqueIDs(scrubbedData_stage_0_name, scrubbedData_stage_1_name)
    extract_name_GI(scrubbedData_stage_1_name, scrubbedData_stage_2_name)
    concat_name_GI(scrubbedData_stage_2_name, scrubbedData_stage_3_name)
    seperateIDs(scrubbedData_stage_3_name, scrubbedData_stage_4_name)
    clean_names(scrubbedData_stage_4_name, scrubbedData_stage_5_name)
    get_group_ranges(scrubbedData_stage_0_name, groupData_name)

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
    for line in in_data:
        line = line.rstrip()
        GI_subs_match = re.findall('\s[0-9\+\-]*$', line)[0] # This is the bread GI, TODO: Add this in
        if GI_subs_match:
            if '+-' in GI_subs_match:
                GI = GI_subs_match.split('+-')[0]
            else:
                GI = GI_subs_match
        out = line.split(GI_subs_match)[0]
        if out:
            GI_subs_match = re.findall('\s[0-9\+\-]*$', out)[0] # This is the glucose GI, TODO: Add this in
            if GI_subs_match:
                name = line.split(GI_subs_match)[0]
                if name:
                    out = name + DELIMITER + GI.strip() + "\n"
                    out_data.write(out)
    in_data.close()
    out_data.close()

def seperateIDs(in_file_name, out_file_name):
    # Split on Subjects (type & number)
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    for line in in_data:
        currFoodID_match = re.match('^\d{1,4}', line)
        if currFoodID_match:
            currFoodID = currFoodID_match.group(0)
            newCurrFoodID = currFoodID+DELIMITER
            line = line.replace(currFoodID, newCurrFoodID)
        out = line
        out_data.write(out)
    in_data.close()
    out_data.close()

def clean_names(in_file_name, out_file_name):
    # Split on Subjects (type & number)
    in_data = open(in_file_name,'r')
    out_data = open(out_file_name,'w')
    for line in in_data:
        
        name_match = re.findall('(?<=;)(.*)(?=;)', line)
        if name_match:
            name = name_match[0]
            new_name = name.strip()
            line = line.replace(name, new_name)

        # Trim trailing commas
        name_match = re.findall('(?<=;)(.*)(?=;)', line)
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
    scrubMe("ADA_scrub_me.txt")