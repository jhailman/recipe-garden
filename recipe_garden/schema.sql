CREATE TABLE IF NOT EXISTS `users` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `name` VARCHAR(256) NOT NULL UNIQUE,
  `email` VARCHAR(128) NOT NULL UNIQUE
);
