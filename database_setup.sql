DROP TABLE IF EXISTS users;

CREATE TABLE `users` (
  `user_id` binary(16) NOT NULL,
  `user_name` varchar(225) NOT NULL,
  `sex` varchar(225) NOT NULL,
  `age` int(11) NOT NULL,
  `weight` float NOT NULL,
  `height` float NOT NULL,
  `BMI` float NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS food_logs;

CREATE TABLE `food_logs` (
  `log_id` binary(16) NOT NULL,
  `user_id` binary(16) DEFAULT NULL,
  `log_time` date NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS consumed_food;

CREATE TABLE `consumed_food`(
    `food_item_id` int NOT NULL AUTO_INCREMENT,
    `food_item_name` varchar(225) NOT NULL,
    `date_consumed` DATE NOT NULL,
    `cfg_vegfru_ss_fraction` decimal(10,0) DEFAULT 0,
    `cfg_grain_ss_fraction` decimal(10,0) DEFAULT 0,
    `cfg_milkalt_ss_fraction` decimal(10,0) DEFAULT 0,
    `cfg_meatalt_ss_fraction` decimal(10,0) DEFAULT 0,
    `cfg_port_sz_g` decimal(10,0),
    `cfg_port_sz_mL` decimal(10,0),
    `log_id` binary(16) NOT NULL,
    PRIMARY KEY (`food_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE if EXISTS frequency CASCADE;

CREATE TABLE frequency(
  user_id binary(16) REFERENCES users(user_id),
  food_name VARCHAR(200) NOT NUll,
  catgegory VARCHAR(200) NOT NULL,
  frequency INTEGER NOT NUll
);



