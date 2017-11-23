DROP TABLE IF EXISTS food_logs;

CREATE TABLE `food_logs` (
  `log_id` binary(16) NOT NULL,
  `user_id` binary(16) DEFAULT NULL,
  `log_time` date NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;