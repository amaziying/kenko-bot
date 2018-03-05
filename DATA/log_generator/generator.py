import os
from datetime import datetime
from datetime import timedelta
import pytz
import random


#We wanna generate data and put it into food_item table

#   `entry_id` binary(16) NOT NULL,
#   `user_id` varchar(200) REFERENCES users(user_id),
#   `food_name` varchar(200) NOT NULL,
#   `date_consumed` DATE NOT NULL,
#   `session_id` binary(16) REFERENCES food_logs(log_id),
#   `category` varchar(200) NOT NULL,
#   `cfg_vegfru_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_grain_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_milkalt_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_meatalt_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_port_sz_g` decimal(10,0),
#   `cfg_port_sz_mL` decimal(10,0),
#   `GI` int(11) NOT NULL,
#   `serving_size_g` float DEFAULT NULL,
#   `serving_size_ml` float DEFAULT NULL,

max_days = 30
num_users = 3

config = {
    "max_days":max_days,
    "session_count_lower":0,
    "session_count_upper":4,
    "lps_lower":1, # lps = logs per session
    "lps_upper":3,
    "food_words":{
        "veg" : [
            "Beets",
            "Cabbage",
            "Cauliflower",
            "Celery",
            "Cucumber",
            "Eggplant",
            "Mushrooms",
            "Peppers, bell",
            "Spinach",
            "Tomato",
            "Turnip",
            "Zucchini"
        ],
        "fru" : [
            "Nectarine",
            "Peach",
            "Mango ",
            "Banana",
            "Grapefruit",
            "Orange",
            "Plum",
            "Kiwi",
            "Apple",
            "Pear",
            "Berries",
            "Watermelon",
            "Grapes",
            "Cherries",
            "Dried fruit",
            "Corn, 1 ear"
        ],
        "grain" : [
            "Whole grain Bread",
            "Whole grain Cereal cold",
            "Barley",
            "Bulgur",
            "Wild rice",
            "Whole grain pasta/noodles",
            "Whole wheat couscous",
            "Potato",
            "Brown rice",
            "Sweet potato",
            "Whole wheat tortilla",
            "Whole grain Pita",
            "Whole grain Bagel",
            "Whole wheat waffle",
            "Whole grain Muffin",
            "Plain popcorn"
        ],
        "meatalt" : [
            "herring",
            "mackerel",
            "trout",
            "salmon",
            "sardines",
            "squid",
            "tuna",
            "Egg",
            "Beans, yellow",
            "Beans, cooked and canned",
            "Peas",
            "Snow peas",
            "tofu",
            "Peanut butter",
            "Hummus",
            "Lentils",
            "salmon",
            "tuna",
            "ptarmigan",
            "partridge",
            "turkey",
            "goose",
            "grouse",
            "lamb",
            "pork"
        ],
        "milkalt":[
            "Milk",
            "Fortified soy beverage",
            "Milk, powdered",
            "Yogurt",
            "Evaporated canned milk",
            "Cheese, block",
            "Cheese, cottage or quark"
        ]
    },
    "SS_fraction_lower_bound":9,
    "SS_fraction_upper_bound":12,
    "GI_lower_bound":6,
    "GI_upper_bound":118,
    "category":["veg", "fru", "grain","milkalt","meatalt"],
    "users":["user_"+str(uid) for uid in range(0,num_users)],
    "start_date":datetime.utcnow(),
    "end_date":datetime.utcnow(),
    "format_date":"%Y-%m-%d %H:%M:%S",
    "serving_size_g_lower":0,
    "serving_size_g_upper":30,
    "serving_size_ml_lower":0,
    "serving_size_ml_upper":100
}

out_name = "generated_data.sql"

def getRandomDate(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def getRandDec(lower, upper):
    return round(random.uniform(lower, upper),2)

def getRandInt(lower, upper):
    return random.randint(lower, upper)

def getRandChoice(input_list):
    return random.choice(input_list)


def insertQuote(w):
    return "\""+str(w)+"\""

def generate_data():
    out_data = open(out_name,'w')

#     refresh = '''
# DROP TABLE if EXISTS food_item CASCADE;
# CREATE TABLE `food_item` (
# `entry_id` binary(16) NOT NULL,
# `user_id` varchar(200) REFERENCES users(user_id),
# `food_name` varchar(200) NOT NULL,
# `date_consumed` DATETIME NOT NULL,
# `session_id` binary(16) REFERENCES food_logs(session_id),
# `category` varchar(200) NOT NULL,
# `cfg_veg_ss_fraction` decimal(10,2) DEFAULT 0,
# `cfg_fru_ss_fraction` decimal(10,2) DEFAULT 0,
# `cfg_grain_ss_fraction` decimal(10,2) DEFAULT 0,
# `cfg_milkalt_ss_fraction` decimal(10,2) DEFAULT 0,
# `cfg_meatalt_ss_fraction` decimal(10,2) DEFAULT 0,
# `cfg_port_sz_g` decimal(10,2),
# `cfg_port_sz_mL` decimal(10,2),
# `GI` int(11) NOT NULL,
# `serving_size_g` float DEFAULT NULL,
# `serving_size_ml` float DEFAULT NULL,
# PRIMARY KEY (`entry_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
#     '''
#     out_data.write(refresh)
    prefix = "INSERT INTO food_item(entry_id,user_id,food_name,date_consumed,session_id,category,cfg_veg_ss_fraction,cfg_fru_ss_fraction,cfg_grain_ss_fraction,cfg_milkalt_ss_fraction,cfg_meatalt_ss_fraction,GI,serving_size_g,serving_size_ml) VALUES ("
    entry_count = 0
    currDay = config["start_date"]
    for i in range(0, config["max_days"]):
        for user in config["users"]:
            prevDay = currDay-timedelta(days=1)
            # Each user gets random dates
            for session_id in range(0,getRandInt(config["session_count_lower"],config["session_count_upper"])):
                for log in range(0,getRandInt(config["lps_lower"],config["lps_upper"])):
                    entry_id = str(entry_count)
                    user_id = insertQuote(user)
                    category = getRandChoice(config["category"])
                    food_name = insertQuote(getRandChoice(config["food_words"][category]))
                    category = insertQuote(category)
                    date_consumed = insertQuote(datetime.strftime(getRandomDate(prevDay,currDay), config["format_date"]))
                    cfg_veg_ss_fraction = str(getRandDec(config["SS_fraction_lower_bound"],config["SS_fraction_upper_bound"]))
                    cfg_fru_ss_fraction = str(getRandDec(config["SS_fraction_lower_bound"],config["SS_fraction_upper_bound"]))
                    cfg_grain_ss_fraction = str(getRandDec(config["SS_fraction_lower_bound"],config["SS_fraction_upper_bound"]))
                    cfg_milkalt_ss_fraction = str(getRandDec(config["SS_fraction_lower_bound"],config["SS_fraction_upper_bound"]))
                    cfg_meatalt_ss_fraction = str(getRandDec(config["SS_fraction_lower_bound"],config["SS_fraction_upper_bound"]))
                    GI = str(getRandInt(config["GI_lower_bound"],config["GI_upper_bound"]))
                    cfg_port_sz_g = str(getRandInt(config["serving_size_g_lower"],config["serving_size_g_upper"]))
                    cfg_port_sz_mL = str(getRandInt(config["serving_size_ml_lower"],config["serving_size_ml_upper"]))

                    line = (str(prefix) +
                        str(entry_id) + "," +
                        str(user_id) + "," +
                        str(food_name) + "," +
                        str(date_consumed) + "," +
                        str(session_id) + "," +
                        str(category) + "," +
                        str(cfg_veg_ss_fraction) + "," +
                        str(cfg_fru_ss_fraction) + "," +
                        str(cfg_grain_ss_fraction) + "," +
                        str(cfg_milkalt_ss_fraction) + "," +
                        str(cfg_meatalt_ss_fraction) + "," +
                        str(GI) + "," +
                        str(cfg_port_sz_g) + "," +
                        str(cfg_port_sz_mL) + ");\n")
                    out_data.write(line)
                    entry_count = entry_count + 1
            currDay = prevDay
    out_data.close()



if __name__=="__main__":
    generate_data()