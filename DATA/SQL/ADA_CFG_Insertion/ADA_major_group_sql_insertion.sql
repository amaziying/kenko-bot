DROP TABLE IF EXISTS GI_major_group_ranges;
CREATE TABLE `GI_major_group_ranges` (
  GI_group_id INT,
  food_name VARCHAR(225),
  food_start_idx INT,
  food_end_idx INT
);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("BAKERY PRODUCTS",1,39);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("BEVERAGES",40,100);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("BREADS",101,296);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("BREAKFAST CEREALS",297,472);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("BREAKFAST CEREAL BARS",473,486);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("CEREAL GRAINS",487,613);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("COOKIES",614,715);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("CRACKERS",716,744);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("DAIRY PRODUCTS AND ALTERNATIVES",745,944);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("FRUIT AND FRUIT PRODUCTS",945,1036);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("FRUIT JUICES",1037,1059);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("INFANT FORMULA AND WEANING FOODS",1060,1075);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("LEGUMES AND NUTS",1076,1128);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("MANAGEMENT PRODUCTS",1129,1172);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("MIXED MEALS AND CONVENIENCE FOODS",1173,1274);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("NUTRITIONAL SUPPORT PRODUCTS",1275,1316);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("NUTS",1317,1324);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("PASTA AND NOODLES",1325,1388);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("SNACK FOODS AND CONFECTIONARY",1389,1537);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("SOUPS",1538,1560);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("SUGARS AND SYRUPS",1561,1609);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("VEGETABLES",1610,1712);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("AFRICAN",1713,1727);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("ARABIC AND TURKISH",1728,1732);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("ASIAN",1733,1773);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("ASIAN INDIAN",1774,1804);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("AUSTRALIAN ABORIGINAL",1805,1811);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("PACIFIC ISLANDERS",1812,1821);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("PIMA INDIAN",1822,1829);
INSERT INTO GI_major_group_ranges(food_name, food_start_idx, food_end_idx) VALUES("SOUTH AMERICAN",1830,1879);