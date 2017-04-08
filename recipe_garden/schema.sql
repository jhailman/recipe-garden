CREATE TABLE IF NOT EXISTS users (
  `id` INT NOT NULL, -- AUTO_INCREMENT doesn't work here for some reason
  `name` VARCHAR(256) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users (id, name, email) VALUES (
    1, "footastic95", "foo@foo.com"
);
