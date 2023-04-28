from utils.config import Config
from flask_login import current_user
import sqlite3


DB = Config.DB

def get_event(id_event=None):
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM `events` WHERE (`id` = ?)", (id_event,))
   event = cursor.fetchone()
   
   data = {}
   if not event:
      return data
   
   data['id'] = event[0]
   data['sd'], data['ed'] = event[1], event[2]
   data['tit'], data['det'] = event[3], event[6]
   data['cat'], data['subs'] = [], []
   data['ep'] = None
   
   cursor.execute("SELECT `id_category` FROM `events_categories` WHERE (`id_event` = ?)", (id_event,))
   category = cursor.fetchall()
   
   for cat in category:
     data['cat'].append(cat[0])
   
   cursor.execute("SELECT `id`, `keterangan` FROM `subevents` WHERE ((`id_event` = ?) AND (`deleted` = 0))", (id_event,))
   subevents = cursor.fetchall()

   for sub in subevents:
     data['subs'].append([sub[0], sub[1]])
   
   if current_user.is_authenticated and current_user.role == 'mahasiswa':
      cursor.execute("SELECT `id_dosen`, `id_subevent`, `id` FROM `events_participants` WHERE ((`id_event` = ?) AND (`id_mahasiswa` = ?))", (id_event, current_user.id,))
      ep = cursor.fetchone()
      if not ep:
         ep = cursor.execute("SELECT `id_dosen`, `id_subevent`, `id_ep` FROM `member` WHERE ((`id_event` = ?) AND (`id_mahasiswa` = ?))", (id_event, current_user.id,)).fetchone()
      data['ep'] = ep

   conn.close()  
   return data

def get_events():
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM `events`")
   data = cursor.fetchall()

   print(data)

   conn.close()  
   return data