from pprint import pprint
import os
import re
from collections import OrderedDict
import math

DELIMITER = ";"
target_table_name = "User_preference"

in_data = open('pref_data.txt', 'r')
out_data = open('pref_insertion.sql','w')

out_data.write('''
DROP TABLE if EXISTS User_preference;
CREATE TABLE `User_preference` (
  `user_id` varchar(200) REFERENCES users(user_id),
  `food_name` varchar(200) NOT NULL,
  `pref_val` int(11),
  PRIMARY KEY (`food_name`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;''')

for line in in_data:
    counter = 0
    row = line.split(DELIMITER)
    food_name = "\'"+str(row[0])+"\'"
    max_users = len(row)
    for pref_val in row[1:max_users]:
        counter += 1
        user_id = "\'"+"user_"+str(counter)+"\'"
        pref_val = str(pref_val).rstrip()
        
        out_data.write("INSERT INTO "+target_table_name+" (user_id, food_name, pref_val) VALUES (" + user_id + ", " + food_name + ", " + pref_val +");\n")

in_data.close()
out_data.close()