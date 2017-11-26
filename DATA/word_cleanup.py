import re
import json

stopWords = "a,able,about,above,abst,accordance,according,accordingly,across,act,actually,added,adj,affected,affecting,affects,after,afterwards,again,against,ah,all,almost,alone,along,already,also,although,always,am,among,amongst,an,and,announce,another,any,anybody,anyhow,anymore,anyone,anything,anyway,anyways,anywhere,apparently,approximately,are,aren,arent,arise,around,as,aside,ask,asking,at,auth,available,away,awfully,b,back,be,became,because,become,becomes,becoming,been,before,beforehand,begin,beginning,beginnings,begins,behind,being,believe,below,beside,besides,between,beyond,biol,both,brief,briefly,but,by,c,ca,came,can,cannot,can't,cause,causes,certain,certainly,co,com,come,comes,contain,containing,contains,could,couldnt,d,date,did,didn't,different,do,does,doesn't,doing,done,don't,down,downwards,due,during,e,each,ed,edu,effect,eg,eight,eighty,either,else,elsewhere,end,ending,enough,especially,et,et-al,etc,even,ever,every,everybody,everyone,everything,everywhere,ex,except,f,far,few,ff,fifth,first,five,fix,followed,following,follows,for,former,formerly,forth,found,four,from,further,furthermore,g,gave,get,gets,getting,give,given,gives,giving,go,goes,gone,got,gotten,h,had,happens,hardly,has,hasn't,have,haven't,having,he,hed,hence,her,here,hereafter,hereby,herein,heres,hereupon,hers,herself,hes,hi,hid,him,himself,his,hither,home,how,howbeit,however,hundred,i,id,ie,if,i'll,im,immediate,immediately,importance,important,in,inc,indeed,index,information,instead,into,invention,inward,is,isn't,it,itd,it'll,its,itself,i've,j,just,k,keep	keeps,kept,kg,km,know,known,knows,l,largely,last,lately,later,latter,latterly,least,less,lest,let,lets,like,liked,likely,line,little,'ll,look,looking,looks,ltd,m,made,mainly,make,makes,many,may,maybe,me,mean,means,meantime,meanwhile,merely,mg,might,million,miss,ml,more,moreover,most,mostly,mr,mrs,much,mug,must,my,myself,n,na,name,namely,nay,nd,near,nearly,necessarily,necessary,need,needs,neither,never,nevertheless,new,next,nine,ninety,no,nobody,non,none,nonetheless,noone,nor,normally,nos,not,noted,nothing,now,nowhere,o,obtain,obtained,obviously,of,off,often,oh,ok,okay,old,omitted,on,once,one,ones,only,onto,or,ord,other,others,otherwise,ought,our,ours,ourselves,out,outside,over,overall,owing,own,p,page,pages,part,particular,particularly,past,per,perhaps,placed,please,plus,poorly,possible,possibly,potentially,pp,predominantly,present,previously,primarily,probably,promptly,proud,provides,put,q,que,quickly,quite,qv,r,ran,rather,rd,re,readily,really,recent,recently,ref,refs,regarding,regardless,regards,related,relatively,research,respectively,resulted,resulting,results,right,run,s,said,same,saw,say,saying,says,sec,section,see,seeing,seem,seemed,seeming,seems,seen,self,selves,sent,seven,several,shall,she,shed,she'll,shes,should,shouldn't,show,showed,shown,showns,shows,significant,significantly,similar,similarly,since,six,slightly,so,some,somebody,somehow,someone,somethan,something,sometime,sometimes,somewhat,somewhere,soon,sorry,specifically,specified,specify,specifying,still,stop,strongly,sub,substantially,successfully,such,sufficiently,suggest,sup,sure	t,take,taken,taking,tell,tends,th,than,thank,thanks,thanx,that,that'll,thats,that've,the,their,theirs,them,themselves,then,thence,there,thereafter,thereby,thered,therefore,therein,there'll,thereof,therere,theres,thereto,thereupon,there've,these,they,theyd,they'll,theyre,they've,think,this,those,thou,though,thoughh,thousand,throug,through,throughout,thru,thus,til,tip,to,together,too,took,toward,towards,tried,tries,truly,try,trying,ts,twice,two,u,un,under,unfortunately,unless,unlike,unlikely,until,unto,up,upon,ups,us,use,used,useful,usefully,usefulness,uses,using,usually,v,value,various,'ve,very,via,viz,vol,vols,vs,w,want,wants,was,wasnt,way,we,wed,welcome,we'll,went,were,werent,we've,what,whatever,what'll,whats,when,whence,whenever,where,whereafter,whereas,whereby,wherein,wheres,whereupon,wherever,whether,which,while,whim,whither,who,whod,whoever,whole,who'll,whom,whomever,whos,whose,why,widely,willing,wish,with,within,without,wont,words,world,would,wouldnt,www,x,y,yes,yet,you,youd,you'll,your,youre,yours,yourself,yourselves,you've,z,zero"
existingFoodWords = set(["yam yeast", "currants", "olive", "guava", "milk", "preserves", "grape", "peanut", "cayenne pepper", "curds", "dressing", "melon", "cress", "icing", "dessert", "brownie", "fat", "lunchmeat", "minerals", "chick peas", "nectar", "asparagus", "dip", "seaweed", "pork", "tea", "almond", "bacon", "millet", "dried", "spaghetti", "brussels sprouts", "sausage", "fava bean", "sauerkraut", "tarragon", "syrup", "crust", "fillet", "salsify", "scallops", "mints", "crunch", "hash", "mussels", "dandelion greens", "punch", "black tea", "citron", "pumpernickel", "pate", "pancake", "frosting", "mozzarella", "vinegar", "lychee", "strudel", "milkshake", "cinnamon", "buckwheat", "popcorn", "spices", "guacamole", "kebab", "turkey", "soybeans", "radish", "sherbet", "soybean", "lime", "rutabaga", "brown rice", "split peas", "crab", "dairy", "blueberry", "sushi", "tangerine", "flax", "chocolate", "pecan", "loquat", "flan", "crackers", "casserole", "edible", "salad", "soup", "sour", "oleo", "meatball", "toffee", "pickle", "ribs", "honey", "alfalfa sprouts", "carrot", "cornflakes", "durian", "lamb", "suet", "rhubarb", "rye", "sundae", "hot", "chinese cabbage", "pizza", "entree", "kohlrabi", "gelatin", "rations", "taco", "salsa", "tomato", "cod", "crepe", "knife kohlrabi", "seaweed seeds", "mango", "chopsticks", "halibut", "danish pastry", "egg", "order", "turmeric", "popsicle", "muffin", "iced tea", "dough", "artichoke", "lima bean", "comestibles", "avocado", "buns", "relish", "submarine sandwich", "fig", "orange", "sauce", "coffee", "citrus", "flour", "wasabi", "cupcake", "lunch", "ketchup", "bread", "meat", "thyme", "bamboo shoots", "roast", "mung bean", "torte", "rosemary", "glasses", "popovers", "fish", "waffle", "mincemeat", "sandwich", "turnip", "ugli fruit", "ice cream", "caramel apple", "summer squash", "granola", "barley", "mashed potatoes", "nutmeg", "pomegranate", "cloves", "salami", "cookie", "lollipop", "tapioca taro", "steak", "raisin", "pudding", "pepperoni", "soda", "garlic", "fritter", "cheese", "lettuce", "lunch box", "bland", "spork", "calorie", "cassava", "spinach", "brisket", "licorice", "scallion", "bitter", "banana", "boil", "kiwi", "nutrition", "stomach", "shallot", "legumes", "cereal", "hazelnut", "micronutrient", "soysauce", "soda bread", "prune", "oats", "stir-fry", "french fries", "spareribs", "sweet potato", "olive omelet", "coconut", "coleslaw", "slaw", "ginger", "cranberry cream", "juice", "nourish", "pastry", "mint", "sprinkles", "bagel", "zucchini", "jimmies", "gravy", "cheesecake", "salmon", "mutton", "shallots", "romaine", "watercress", "chard", "oyster", "beets", "hot dog", "gyro", "napkin", "hungry", "scrambled", "macaroon", "pineapple", "radicchio", "beancurd", "tuber", "bell pepper", "green tea", "fennel", "jellybeans", "kidney beans", "chicken", "spuds", "toast", "snack", "gouda cheese", "nectarine", "gourd", "menu", "sugar", "celery", "jam", "kettle corn", "rice", "pumpkin", "plate", "appetizer", "swiss chard", "molasses", "watermelon", "julienne", "spicy", "jicama", "chutney", "string bean", "greens", "spatula", "pretzel", "caramel", "stringy", "collard greens", "sour cream", "picnic", "ice cream cone", "nut", "lemonade", "nibble", "sage", "ham hamburger", "quiche", "noodles", "honeydew", "elderberry", "mug", "wok", "yogurt", "nutritious", "cantaloupe", "cauliflower", "sole", "vitamin", "broil", "aspic", "kitchen", "water", "dates", "restaurant", "jelly", "succotash", "hummus", "grain", "berry", "eggplant", "fava bans", "bran", "peanut butter", "patty", "sweet", "pot", "pop", "arugula", "oregano", "walnut", "candy apple", "beef", "parsley", "main course", "yam", "beet", "basil", "tofu", "fry", "ravioli", "mushroom", "cream cheese", "squash", "lima beans", "savory", "black beans", "brunch", "teapot", "feed fennel", "teriyaki", "vanilla", "sorghum", "hot sauce", "squid", "pita bread", "acorn squash", "sustenance", "protein", "pot roast", "toaster", "greenbean", "macaroni", "vegetable", "lasagna", "pan", "water chestnut", "oil", "papaya", "dragonfruit", "drink", "munch", "fruit", "cucumber", "supper", "taro", "tuna", "broccoli", "butter", "blood orange", "burrito", "pork chops", "veal", "gingerale", "smoked", "alfalfa", "kale", "rocket", "cheddar", "mole sauce", "margarine", "apple", "omnivore", "cilantro", "sunflower", "cherry", "straw", "horseradish", "sub sandwich", "kumquat", "plum poached", "persimmon", "cottage cheese", "chives", "anchovy", "endive", "provisions", "black-eyed peas", "doughnut", "boysenberry", "jackfruit", "maple syrup", "clam", "crisp", "onion", "candy", "roll", "blackberry", "meringue", "nosh", "tomatillo", "grub", "sorbet", "yolk", "marmalade", "lobster", "meatloaf", "lentils", "slice", "okra", "jalapeno", "kettle", "ice", "lard", "pea", "mandarin orange", "pepper", "wheat", "corn", "sesame seed", "pomelo", "tortilla", "stew", "pasta", "raspberry", "iceberg lettuce", "quinoa", "biscuit", "oatmeal", "shrimp", "beans", "gingerbread", "curry", "marshmallow", "mochi", "jordan almonds", "gastronomy", "celeriac", "soy", "custard", "maize", "breadfruit", "anise", "caviar", "parsnip", "peapod", "refrigerator", "hot chile peppers", "marionberry", "lox", "sorrel", "jug", "pitcher", "peppers", "chili chips", "unleavened", "butter bean", "liver loaf", "basil batter", "shish kebab", "take-out", "apricot", "strawberry", "grapefruit grated", "cornmeal", "cake", "fried", "dill", "pie", "carbohydrate", "cobbler", "sprouts", "lemon", "peach", "cashew", "saffron", "venison", "pattypan squash", "mayonnaise", "whey", "leek", "whipped cream", "tart", "tamale", "mustard", "pear", "refreshments", "herbs", "capers", "wafer", "potato", "mustard greens", "salt", "daikon", "prime rib", "nutrient", "pilaf"])
stopWords = set(stopWords.split(','))

def containsNumber(x):
	for char in x:
		if char.isdigit():
			return True
	return False

with open('raw_food_names.txt', 'r') as myfile:
    data = myfile.read()
    phrases = data.split('|')

    result = []
    for phrase in data.split('|'):
    	words = filter(lambda x: len(x) and not (x in stopWords), phrase.split(' '))
    	words = map(lambda x: re.sub(r'\W+', '', x).lower(), words)
    	words = filter(lambda x: len(x) and (not containsNumber(x)), words)
    	result += words

    result = list(set(result).union(existingFoodWords))

    with open('food_words.json', 'w') as outfile:
    	json.dump({ "words": result }, outfile)




