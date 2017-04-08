DROP TABLE IF EXISTS users;
CREATE TABLE users (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(256) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  `password` VARCHAR(93) NOT NULL
);

-- Example data
INSERT INTO users (name, email, password) VALUES (
    'Example User', 'user@example.com',
    -- valid hash of 'password'
    'pbkdf2:sha256:50000$jjb4u67b$6e3256db2e7d7f1e81aafa136e972934cb32a27014e53a2c17b0fd2d3f5a1f29'
)
