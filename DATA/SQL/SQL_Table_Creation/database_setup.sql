DROP TABLE IF EXISTS GI_major_group_ranges;
CREATE TABLE `GI_major_group_ranges` (
  GI_group_id INT AUTO_INCREMENT PRIMARY KEY,
  food_name VARCHAR(225),
  food_start_idx INT,
  food_end_idx INT
);

DROP TABLE IF EXISTS CNF_food_names;
CREATE TABLE `CNF_food_names` (
  `food_id` int(11) NOT NULL,
  `food_code` int(11) DEFAULT NULL,
  `food_group_id` int(11) DEFAULT NULL,
  `food_description` varchar(100) NOT NULL,
  `scientific_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`food_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS CNF_food_groups;
CREATE TABLE `CNF_food_groups` (
  `food_group_id` int(11) NOT NULL,
  `food_group_code` int(11) NOT NULL,
  `food_group_name` varchar(40) NOT NULL,
  PRIMARY KEY (`food_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS users;
CREATE TABLE `users` (
  `user_id` binary(16) NOT NULL,
  `user_name` varchar(225) NOT NULL,
  `sex` varchar(225) NOT NULL,
  `age` int(11) NOT NULL,
  `weight` float DEFAULT NULL,
  `height` float DEFAULT NULL,
  `BMI` float DEFAULT NULL,
  `ss_lower_grain` INTEGER NOT NULL,
  `ss_higher_grain` INTEGER NOT NULL,
  `ss_lower_meatalt` INTEGER NOT NULL,
  `ss_higher_meatalt` INTEGER NOT NULL,
  `ss_lower_milkalt` INTEGER NOT NULL,
  `ss_higher_milkalt` INTEGER NOT NULL,
  `ss_lower_vf` INTEGER NOT NULL,
  `ss_higher_vf` INTEGER NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS food_logs;
CREATE TABLE `food_logs` (
  `session_id` binary(16) NOT NULL,
  `user_id` binary(16) REFERENCES users(user_id),
  `session_time` DATETIME NOT NULL,
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE if EXISTS frequency CASCADE;
CREATE TABLE frequency(
  user_id binary(16) REFERENCES users(user_id),
  food_name VARCHAR(200) NOT NUll,
  catgegory VARCHAR(200) NOT NULL,
  frequency INTEGER NOT NUll
);

DROP TABLE if EXISTS food_item CASCADE;
CREATE TABLE `food_item` (
  `entry_id` binary(16) NOT NULL,
  `user_id` varchar(200) REFERENCES users(user_id),
  `food_name` varchar(200) NOT NULL,
  `date_consumed` DATETIME NOT NULL,
  `session_id` binary(16) REFERENCES food_logs(session_id),
  `catgegory` varchar(200) NOT NULL,
  `cfg_vegfru_ss_fraction` decimal(10,2) DEFAULT 0,
  `cfg_grain_ss_fraction` decimal(10,2) DEFAULT 0,
  `cfg_milkalt_ss_fraction` decimal(10,2) DEFAULT 0,
  `cfg_meatalt_ss_fraction` decimal(10,2) DEFAULT 0,
  `cfg_port_sz_g` decimal(10,2),
  `cfg_port_sz_mL` decimal(10,2),
  `GI` int(11) NOT NULL,
  `serving_size_g` float DEFAULT NULL,
  `serving_size_ml` float DEFAULT NULL,
  PRIMARY KEY (`entry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS GI_Data;
CREATE TABLE GI_Data(
  food_id VARCHAR(225), 
  food_name VARCHAR(225), 
  glucose_gi INT, 
  bread_gi INT, 
  serving_size_mL INT, 
  serving_size_g INT, 
  country_id VARCHAR(225),
  GI_group_id VARCHAR(225) REFERENCES GI_major_group_ranges(GI_group_id),
  PRIMARY KEY (`food_id`)
);

DROP TABLE IF EXISTS Preferences;
CREATE TABLE GI_Data(
  `user_id` varchar(200) REFERENCES users(user_id),
  food_name VARCHAR(225),
  chosen_times INT,
  rejected_times INT
);

-- Run these after ADA_GI_sql_insertion.sql
-- /////////////////////////////////////////////
-- This will add the major group ranges to the GI data
UPDATE GI_Data gd, GI_major_group_ranges gr
SET gd.`GI_group_id` = gr.`GI_group_id`
WHERE gd.`food_id` <= gr.`food_end_idx` AND gd.`food_id` >= gr.`food_start_idx`;
-- /////////////////////////////////////////////