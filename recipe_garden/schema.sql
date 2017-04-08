CREATE TABLE IF NOT EXISTS users (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(256) NOT NULL,
  `email` VARCHAR(128) NOT NULL
);

INSERT INTO users (name, email) VALUES (
    "footastic95", "foo@foo.com"
);
