CREATE TABLE IF NOT EXISTS events (
  id INTEGER,
  start DATETIME,
  end DATETIME,
  text TEXT NOT NULL,
  color TEXT NOT NULL,
  bg TEXT NOT NULL,
  PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE INDEX IF NOT EXISTS idx_start ON events (start);
CREATE INDEX IF NOT EXISTS idx_end ON events (end);


CREATE TABLE IF NOT EXISTS users (
  id INTEGER,
  fullname TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  PRIMARY KEY("id")
);


CREATE TABLE IF NOT EXISTS categories (
  id INTEGER,
  category TEXT NOT NULL,
  PRIMARY KEY("id")
);
INSERT INTO categories ('id', 'category') 
VALUES
        (1, 'data sains'),
        (2, 'kewirausahaan'),
        (3, 'infografis'),
        (4, 'karya ilmiah');


CREATE TABLE IF NOT EXISTS events_categories (
  id INTEGER,
  id_event INTEGER,
  id_category INTEGER,
  PRIMARY KEY("id" AUTOINCREMENT)
);