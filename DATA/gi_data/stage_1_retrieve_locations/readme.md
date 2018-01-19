location.txt

For every row of input data from ADA_GI_sql_insertion.sql, the last bracket is parsed out and its contents are put into location.txt. Most of the time there will be a country name in it, denoting where the food item was sampled from. By inspection, you can take the country names of interest and put them into the list variable ```available_countries``` in the file ```normalize_food_names.py``` so that food items with associated countries in ```available_countries``` will have its country information extracted into a new ```country_id``` column. 

normalize_food_names.py

This is a data cleansing script. It will remove the last bracket from each row in input data ```ADA_GI_sql_insertion.sql``` and put its content into locaiton.txt. Each row may be updated with a location based on what was found in the last bracket.