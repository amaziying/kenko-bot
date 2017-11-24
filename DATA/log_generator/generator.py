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
#   `catgegory` varchar(200) NOT NULL,
#   `cfg_vegfru_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_grain_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_milkalt_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_meatalt_ss_fraction` decimal(10,0) DEFAULT 0,
#   `cfg_port_sz_g` decimal(10,0),
#   `cfg_port_sz_mL` decimal(10,0),
#   `GI` int(11) NOT NULL,
#   `serving_size_g` float DEFAULT NULL,
#   `serving_size_ml` float DEFAULT NULL,

max_days = 100

config = {
    "max_days":max_days,
    "session_count_lower":0,
    "session_count_upper":5,
    "lps_lower":1, # lps = logs per session
    "lps_upper":3,
    "food_words":["yam yeast", "currants", "olive", "guava", "milk", "preserves", "grape", "peanut", "cayenne pepper", "curds", "dressing", "melon", "cress", "icing", "dessert", "brownie", "fat", "lunchmeat", "minerals", "chick peas", "nectar", "asparagus", "dip", "seaweed", "pork", "tea", "almond", "bacon", "millet", "dried", "spaghetti", "brussels sprouts", "sausage", "fava bean", "sauerkraut", "tarragon", "syrup", "crust", "fillet", "salsify", "scallops", "mints", "crunch", "hash", "mussels", "dandelion greens", "punch", "black tea", "citron", "pumpernickel", "pate", "pancake", "frosting", "mozzarella", "vinegar", "lychee", "strudel", "milkshake", "cinnamon", "buckwheat", "popcorn", "spices", "guacamole", "kebab", "turkey", "soybeans", "radish", "sherbet", "soybean", "lime", "rutabaga", "brown rice", "split peas", "crab", "dairy", "blueberry", "sushi", "tangerine", "flax", "chocolate", "pecan", "loquat", "flan", "crackers", "casserole", "edible", "salad", "soup", "sour", "oleo", "meatball", "toffee", "pickle", "ribs", "honey", "alfalfa sprouts", "carrot", "cornflakes", "durian", "lamb", "suet", "rhubarb", "rye", "sundae", "hot", "chinese cabbage", "pizza", "entree", "kohlrabi", "gelatin", "rations", "taco", "salsa", "tomato", "cod", "crepe", "knife kohlrabi", "seaweed seeds", "mango", "chopsticks", "halibut", "danish pastry", "egg", "order", "turmeric", "popsicle", "muffin", "iced tea", "dough", "artichoke", "lima bean", "comestibles", "avocado", "buns", "relish", "submarine sandwich", "fig", "orange", "sauce", "coffee", "citrus", "flour", "wasabi", "cupcake", "lunch", "ketchup", "bread", "meat", "thyme", "bamboo shoots", "roast", "mung bean", "torte", "rosemary", "glasses", "popovers", "fish", "waffle", "mincemeat", "sandwich", "turnip", "ugli fruit", "ice cream", "caramel apple", "summer squash", "granola", "barley", "mashed potatoes", "nutmeg", "pomegranate", "cloves", "salami", "cookie", "lollipop", "tapioca taro", "steak", "raisin", "pudding", "pepperoni", "soda", "garlic", "fritter", "cheese", "lettuce", "lunch box", "bland", "spork", "calorie", "cassava", "spinach", "brisket", "licorice", "scallion", "bitter", "banana", "boil", "kiwi", "nutrition", "stomach", "shallot", "legumes", "cereal", "hazelnut", "micronutrient", "soysauce", "soda bread", "prune", "oats", "stir-fry", "french fries", "spareribs", "sweet potato", "olive omelet", "coconut", "coleslaw", "slaw", "ginger", "cranberry cream", "juice", "nourish", "pastry", "mint", "sprinkles", "bagel", "zucchini", "jimmies", "gravy", "cheesecake", "salmon", "mutton", "shallots", "romaine", "watercress", "chard", "oyster", "beets", "hot dog", "gyro", "napkin", "hungry", "scrambled", "macaroon", "pineapple", "radicchio", "beancurd", "tuber", "bell pepper", "green tea", "fennel", "jellybeans", "kidney beans", "chicken", "spuds", "toast", "snack", "gouda cheese", "nectarine", "gourd", "menu", "sugar", "celery", "jam", "kettle corn", "rice", "pumpkin", "plate", "appetizer", "swiss chard", "molasses", "watermelon", "julienne", "spicy", "jicama", "chutney", "string bean", "greens", "spatula", "pretzel", "caramel", "stringy", "collard greens", "sour cream", "picnic", "ice cream cone", "nut", "lemonade", "nibble", "sage", "ham hamburger", "quiche", "noodles", "honeydew", "elderberry", "mug", "wok", "yogurt", "nutritious", "cantaloupe", "cauliflower", "sole", "vitamin", "broil", "aspic", "kitchen", "water", "dates", "restaurant", "jelly", "succotash", "hummus", "grain", "berry", "eggplant", "fava bans", "bran", "peanut butter", "patty", "sweet", "pot", "pop", "arugula", "oregano", "walnut", "candy apple", "beef", "parsley", "main course", "yam", "beet", "basil", "tofu", "fry", "ravioli", "mushroom", "cream cheese", "squash", "lima beans", "savory", "black beans", "brunch", "teapot", "feed fennel", "teriyaki", "vanilla", "sorghum", "hot sauce", "squid", "pita bread", "acorn squash", "sustenance", "protein", "pot roast", "toaster", "greenbean", "macaroni", "vegetable", "lasagna", "pan", "water chestnut", "oil", "papaya", "dragonfruit", "drink", "munch", "fruit", "cucumber", "supper", "taro", "tuna", "broccoli", "butter", "blood orange", "burrito", "pork chops", "veal", "gingerale", "smoked", "alfalfa", "kale", "rocket", "cheddar", "mole sauce", "margarine", "apple", "omnivore", "cilantro", "sunflower", "cherry", "straw", "horseradish", "sub sandwich", "kumquat", "plum poached", "persimmon", "cottage cheese", "chives", "anchovy", "endive", "provisions", "black-eyed peas", "doughnut", "boysenberry", "jackfruit", "maple syrup", "clam", "crisp", "onion", "candy", "roll", "blackberry", "meringue", "nosh", "tomatillo", "grub", "sorbet", "yolk", "marmalade", "lobster", "meatloaf", "lentils", "slice", "okra", "jalapeno", "kettle", "ice", "lard", "pea", "mandarin orange", "pepper", "wheat", "corn", "sesame seed", "pomelo", "tortilla", "stew", "pasta", "raspberry", "iceberg lettuce", "quinoa", "biscuit", "oatmeal", "shrimp", "beans", "gingerbread", "curry", "marshmallow", "mochi", "jordan almonds", "gastronomy", "celeriac", "soy", "custard", "maize", "breadfruit", "anise", "caviar", "parsnip", "peapod", "refrigerator", "hot chile peppers", "marionberry", "lox", "sorrel", "jug", "pitcher", "peppers", "chili chips", "unleavened", "butter bean", "liver loaf", "basil batter", "shish kebab", "take-out", "apricot", "strawberry", "grapefruit grated", "cornmeal", "cake", "fried", "dill", "pie", "carbohydrate", "cobbler", "sprouts", "lemon", "peach", "cashew", "saffron", "venison", "pattypan squash", "mayonnaise", "whey", "leek", "whipped cream", "tart", "tamale", "mustard", "pear", "refreshments", "herbs", "capers", "wafer", "potato", "mustard greens", "salt", "daikon", "prime rib", "nutrient", "pilaf"],
    "SS_fraction_lower_bound":0,
    "SS_fraction_upper_bound":1.5,
    "GI_lower_bound":6,
    "GI_upper_bound":118,
    "category":["vf", "grain","milkalt","meatalt"],
    "users":["zi","felix","brian","susan"],
    "start_date":datetime.utcnow()-timedelta(days=max_days),
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
    prefix = "INSERT INTO food_item(entry_id,user_id,food_name,date_consumed,session_id,catgegory,cfg_vegfru_ss_fraction,cfg_grain_ss_fraction,cfg_milkalt_ss_fraction,cfg_meatalt_ss_fraction,GI,serving_size_g,serving_size_ml) VALUES ("
    entry_count = 0
    for user in config["users"]:
        for i in xrange(0, config["max_days"]):
            currDay = config["start_date"]
            prevDay = config["start_date"]-timedelta(days=1)
            # Each user gets random dates
            for session_id in xrange(0,getRandInt(config["session_count_lower"],config["session_count_upper"])):
                for log in xrange(0,getRandInt(config["lps_lower"],config["lps_upper"])):
                    entry_id = str(entry_count)
                    user_id = insertQuote(user)
                    food_name = insertQuote(getRandChoice(config["food_words"]))
                    date_consumed = insertQuote(datetime.strftime(getRandomDate(prevDay,currDay), config["format_date"]))
                    category = insertQuote(getRandChoice(config["category"]))
                    cfg_vegfru_ss_fraction = str(getRandDec(config["SS_fraction_lower_bound"],config["SS_fraction_upper_bound"]))
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
                        str(cfg_vegfru_ss_fraction) + "," +
                        str(cfg_grain_ss_fraction) + "," +
                        str(cfg_milkalt_ss_fraction) + "," +
                        str(cfg_meatalt_ss_fraction) + "," +
                        str(GI) + "," +
                        str(cfg_port_sz_g) + "," +
                        str(cfg_port_sz_mL) + ");\n")
                    out_data.write(line)
                    entry_count = entry_count + 1
    
    out_data.close()



if __name__=="__main__":
    generate_data()