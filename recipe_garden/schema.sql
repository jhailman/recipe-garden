CREATE TABLE IF NOT EXISTS users (
  `id` INTEGER NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users (name, email) VALUES (
    "footastic95", "foo@foo.com"
);
