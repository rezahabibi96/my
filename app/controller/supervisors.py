from utils.config import Config
import sqlite3
import random


DB = Config.DB

def get_supervisor(id_supervisor=None):
   pass

def get_supervisors():
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM `users` WHERE (`role` = 'dosen')")
   lecturers = cursor.fetchall()

   data = []
   for dt in lecturers:
      id_lecturer = dt[0]

      cursor.execute("SELECT `research_interest`, `research_group` FROM `lecturers` WHERE (`id_lecturer` = ?)", (id_lecturer,))
      research = cursor.fetchone()
      data.append({
         'id': id_lecturer,
         'nama': dt[1],
         'ri': research[0],
         'rg': research[-1],
         'imgs': random.choice(['person_01', 'person_02', 'person_03', 'person_04'])
      })
   
   conn.close()
   return data