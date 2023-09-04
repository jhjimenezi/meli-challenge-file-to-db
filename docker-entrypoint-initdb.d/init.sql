-- Use the newly created database
USE itemsdb;

-- Create a new table
CREATE TABLE item (
  site VARCHAR(3),
  id VARCHAR(50),
  price DECIMAL(10,2),
  start_time DATETIME,
  category_name VARCHAR(50),
  currency_description VARCHAR(100),
  seller_nickname VARCHAR(50),
  PRIMARY KEY (site, id)
);