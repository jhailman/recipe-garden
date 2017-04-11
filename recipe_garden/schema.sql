-- create the database
DROP DATABASE IF EXISTS recipe_schema;
CREATE DATABASE recipe_schema;

-- select the database
USE recipe_schema;

-- create the tables
DROP TABLE IF EXISTS user;
CREATE TABLE user
(
  id           INT(11)      NOT NULL,
  name	       VARCHAR(45) 	NOT NULL,
  password	   VARCHAR(93)	NOT NULL,
  email        VARCHAR(128) NOT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS ingredient;
CREATE TABLE ingredient
(
  name 	     VARCHAR(45)	NOT NULL,
  PRIMARY KEY (name)
);

DROP TABLE IF EXISTS recipe;
CREATE TABLE recipe
(
  id			    INT(11)		NOT NULL,
  rname		  	VARCHAR(45) NOT NULL,
  author_id		INT(11),
  created     TIMESTAMP DEFAULT now() ON UPDATE now(),
  PRIMARY KEY (id),
  FOREIGN KEY (author_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS direction;
CREATE TABLE direction
(
  id            INT(11)		NOT NULL,
  recipe_id		  INT(11)		NOT NULL,
  description   TEXT		  NOT NULL,
  ordernum      INT(11),
  PRIMARY KEY (id),
  FOREIGN KEY (recipe_id) REFERENCES recipe(id)
);

DROP TABLE IF EXISTS recipe_ingredient;
CREATE TABLE recipe_ingredient
(
  id            INT(11)		NOT NULL,
  recipe_id     INT(11)		NOT NULL,
  ingredient  	VARCHAR(45)	NOT NULL,
  amount        VARCHAR(45),
  PRIMARY KEY (id),
  FOREIGN KEY (recipe_id) REFERENCES recipe(id),
  FOREIGN KEY (ingredient) REFERENCES ingredient(name)
);

DROP TABLE IF EXISTS shopping_list;
CREATE TABLE shopping_list
(
  id              INT(11)   NOT NULL,
  user_id         INT(11)   NOT NULL,
  recipe_ingredient_id  INT(11) NOT NULL,
  FOREIGN KEY (recipe_ingredient_id) REFERENCES recipe_ingredient(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS favorites;
CREATE TABLE favorites
(
  user_id       INT(11)			NOT NULL,
  recipe_id   	INT(11)			NOT NULL,
  PRIMARY KEY (user_id, recipe_id),
  FOREIGN KEY (recipe_id) REFERENCES recipe(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Example data

INSERT INTO user (name, email, password) VALUES (
    "Mr. Foo Bar", "foo@foo.com",
    'pbkdf2:sha256:50000$jjb4u67b$6e3256db2e7d7f1e81aafa136e972934cb32a27014e53a2c17b0fd2d3f5a1f29'
);
