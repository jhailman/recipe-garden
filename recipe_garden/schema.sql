-- create the database
DROP DATABASE IF EXISTS recipe_schema;
CREATE DATABASE recipe_schema;

-- select the database
USE recipe_schema;

-- create the tables
DROP TABLE IF EXISTS user;
CREATE TABLE user
(
  id           INTEGER AUTO_INCREMENT,
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
  id			    INTEGER AUTO_INCREMENT,
  name		  	VARCHAR(45) NOT NULL,
  author_id		INT(11) NOT NULL,
  created     TIMESTAMP DEFAULT now() ON UPDATE now(),
  PRIMARY KEY (id),
  FOREIGN KEY (author_id) REFERENCES user(id)
);

DROP TABLE IF EXISTS direction;
CREATE TABLE direction
(
  id            INTEGER AUTO_INCREMENT,
  recipe_id		  INT(11)		NOT NULL,
  description   TEXT		  NOT NULL,
  ordernum      INT(11),
  PRIMARY KEY (id),
  FOREIGN KEY (recipe_id) REFERENCES recipe(id)
);

DROP TABLE IF EXISTS recipe_ingredient;
CREATE TABLE recipe_ingredient
(
  id            INTEGER AUTO_INCREMENT,
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
  id              INTEGER AUTO_INCREMENT,
  user_id         INT(11)   NOT NULL,
  recipe_ingredient_id  INT(11) NOT NULL,
  PRIMARY KEY (id),
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

<<<<<<< HEAD
INSERT INTO user (name, password, email) VALUES (
    "footastic95", "footastic95", "foo@foo.com"
=======
-- Example data

INSERT INTO user (name, email, password) VALUES (
    "Mr. Foo Bar", "foo@foo.com",
    'pbkdf2:sha256:50000$jjb4u67b$6e3256db2e7d7f1e81aafa136e972934cb32a27014e53a2c17b0fd2d3f5a1f29'
>>>>>>> a882bb2486145265581e20d995621ec559393dac
);

INSERT INTO ingredient VALUES
("onion(s)"), ("potato(s)"), ("carrot(s)"), ("mushroom(s)"),
("olive oil"), ("vegetable broth"), ("chard"), ("canned corn"),
("garlic"), ("salt"), ("pepper"), ("dried parsley"),
("dried oregano"), ("bay leaf");

INSERT INTO recipe (name, author_id) VALUES
("Potato Soup", 1);

INSERT INTO recipe_ingredient (recipe_id, ingredient, amount) VALUES
(1, "onion(s)", "1"), (1, "potato(s)", "5"), (1, "carrot(s)", "1"),
(1, "mushroom(s)", "6 oz"), (1, "olive oil", "1/4 cup"),
(1, "vegetable broth", "6 cups"), (1, "chard", "1 bunch"),
(1, "garlic", "4 cloves"), (1, "salt", "1 tbsp"),
(1, "pepper", "1 tsp"), (1, "dried parsley", "1 tbsp"),
(1, "dried oregano", "1 tbsp"), (1, "bay leaf", "1");

INSERT INTO recipe_ingredient (recipe_id, ingredient) VALUES
(1, "canned corn");

INSERT INTO direction (recipe_id, description, ordernum) VALUES
(1, "Cut all veggies and mince the garlic", 1),
(1, "Add the olive oil to a large pot on medium heat", 2),
(1, "Sautee the onion until caramelized", 3),
(1, "Add garlic and sautee for 1 minute more", 4),
(1, "Add the rest of the ingredients to the pot except for chard and corn", 5),
(1, "Bring the liquid to a boil and then turn heat down to simmer for 45 minutes", 6),
(1, "Turn heat off and use an immersion blender to make the soup a smooth-thick consistency", 7),
(1, "Heat some olive oil in a pan on medium heat", 8),
(1, "Add chard to pan and sautee until wilted", 9),
(1, "Assemble by adding soup to a bowl and topping with the canned corn and sauteed chard", 10);
