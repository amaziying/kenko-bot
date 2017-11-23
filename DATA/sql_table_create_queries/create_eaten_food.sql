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