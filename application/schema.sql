DROP TABLE IF EXISTS person;

CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  middle_name TEXT,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  age INTEGER NOT NULL,
  metadata TEXT NOT NULL
);
