from config import Config
from sqlite3 import Error
import sqlite3, os


DB = Config.DB
SQL = Config.SQL

def init():
  if os.path.exists(DB):
    os.remove(DB)

  conn = sqlite3.connect(DB)

  with open(SQL) as f:
    conn.executescript(f.read())
  
  conn.commit()
  conn.close() 

  print("database created")
  
init()