CREATE TABLE IF NOT EXISTS events (
  id INTEGER,
  start DATETIME,
  end DATETIME,
  text TEXT NOT NULL,
  color TEXT NOT NULL,
  bg TEXT NOT NULL,
  detail TEXT NOT NULL,
  PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE INDEX IF NOT EXISTS idx_start ON events (start);
CREATE INDEX IF NOT EXISTS idx_end ON events (end);


CREATE TABLE IF NOT EXISTS users (
  id INTEGER,
  fullname TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role TEXT DEFAULT "mahasiswa",
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


CREATE TABLE IF NOT EXISTS lecturers (
  id INTEGER,
  id_lecturer INTEGER UNIQUE,
  research_interest TEXT,
  PRIMARY KEY("id" AUTOINCREMENT)
  FOREIGN KEY(id_lecturer) REFERENCES users (id)
);


CREATE TABLE IF NOT EXISTS students (
  id INTEGER,
  id_student INTEGER UNIQUE,
  semester TEXT,
  PRIMARY KEY("id" AUTOINCREMENT)
  FOREIGN KEY(id_student) REFERENCES users (id)
);


CREATE TABLE IF NOT EXISTS hima (
  id INTEGER,
  id_hima INTEGER UNIQUE,
  divisi TEXT,
  PRIMARY KEY("id" AUTOINCREMENT)
  FOREIGN KEY(id_hima) REFERENCES users (id)
);


CREATE TABLE IF NOT EXISTS tendik (
  id INTEGER,
  id_tendik INTEGER UNIQUE,
  bagian TEXT,
  PRIMARY KEY("id" AUTOINCREMENT)
  FOREIGN KEY(id_tendik) REFERENCES users (id)
);


CREATE TABLE IF NOT EXISTS events_categories (
  id INTEGER,
  id_event INTEGER,
  id_category INTEGER,
  PRIMARY KEY("id" AUTOINCREMENT)
  FOREIGN KEY(id_event) REFERENCES events (id)
  FOREIGN KEY(id_category) REFERENCES categories (id) 
);