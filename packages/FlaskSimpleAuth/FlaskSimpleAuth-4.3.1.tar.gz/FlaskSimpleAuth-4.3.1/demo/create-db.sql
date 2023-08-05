CREATE TABLE Stuff(
  sid INTEGER PRIMARY KEY AUTOINCREMENT,
  sname TEXT NOT NULL
);

CREATE TABLE Auth(
  login TEXT PRIMARY KEY,
  upass TEXT NOT NULL,
  admin BOOLEAN NOT NULL DEFAULT FALSE
);
