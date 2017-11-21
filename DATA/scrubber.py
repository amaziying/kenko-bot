import os
import re

DELIMITER = ";"

def scrubMe(fname):
    scrubbedData_stage_0_name = fname
    scrubbedData_stage_1_name = 'output_stage_1.txt'
    scrubbedData_stage_2_name = 'output_stage_2.txt'
    scrubbedData_stage_3_name = 'output_stage_3.txt'
    scrubbedData_stage_4_name = 'output_stage_4.txt'
    scrubbedData_stage_5_name = 'output_stage_5.txt'

    extractUniqueIDs(scrubbedData_stage_0_name, scrubbedData_stage_1_name)
    extract_name_GI(scrubbedData_stage_1_name, scrubbedData_stage_2_name)
    concat_name_GI(scrubbedData_stage_2_name, scrubbedData_stage_3_name)
    seperateIDs(scrubbedData_stage_3_name, scrubbedData_stage_4_name)
    clean_names(scrubbedData_stage_4_name, scrubbedData_stage_5_name)

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
        GI_subs_match = re.findall('\s[0-9\+\-]*$', line)[0]
        if GI_subs_match:
            if '+-' in GI_subs_match:
                GI = GI_subs_match.split('+-')[0]
            else:
                GI = GI_subs_match
        out = line.split(GI_subs_match)[0]
        if out:
            GI_subs_match = re.findall('\s[0-9\+\-]*$', out)[0]
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

if __name__ == "__main__":
    scrubMe("ADA_scrub_me.txt")