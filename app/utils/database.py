from .config import Config
import sqlite3
import os


DB = Config.DB
SQL = Config.SQL

def init(app=None):
  if os.path.exists(DB):
    os.remove(DB)

  conn = sqlite3.connect(DB)

  with open(SQL) as f:
    conn.executescript(f.read())
  
  conn.commit()
  conn.close() 

  print("database created")