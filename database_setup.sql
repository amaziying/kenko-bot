DROP TABLE if Exists users CASCADE;

CREATE TABLE users (
  user_id binary(16) PRIMARY KEY NOT NULL,
  user_name VARCHAR(30) NOT NULL,
  weight FLOAT NOT NULL,
  height FLOAT NOT NULL,
  BMI FLOAT NOT NULL,
  age INTEGER NOT NULL
);

DROP TABLE if EXISTS food_log CASCADE;

CREATE TABLE food_log(
  log_id binary(16) PRIMARY KEY NOT NULL,
  user_id binary(16) REFERENCES users(user_id),
  log_time DATE NOT NULL
);

DROP TABLE if EXISTS food_item CASCADE;

CREATE TABLE food_item(
  food_item_id binary(16) PRIMARY KEY NOT NULL,
  log_id binary(16) REFERENCES food_log(log_id),
  food_name VARCHAR(200) NOT NUll,
  catgegory VARCHAR(200) NOT NULL,
  GI INTEGER NOT NULL,
  serving_size_g FLOAT,
  serving_size_ml FLOAT
);

DROP TABLE if EXISTS frequency CASCADE;

CREATE TABLE frequency(
  user_id binary(16) REFERENCES users(user_id),
  food_name VARCHAR(200) NOT NUll,
  catgegory VARCHAR(200) NOT NULL,
  frequency INTEGER NOT NUll
);



