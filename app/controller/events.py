from utils.config import Config
import sqlite3


DB = Config.DB

def get_event(id_event):
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM `events` WHERE (`id` = ?)", (id_event,))
   event = cursor.fetchone()
   
   data = {}
   if not event:
      return data
   
   data['id'] = event[0]
   data['sd'], data['ed'] = event[1], event[2]
   data['tit'], data['cat'] = event[3], []
   
   cursor.execute("SELECT `id_category` FROM `events_categories` WHERE (`id_event` = ?)", (id_event,))
   category = cursor.fetchall()
   
   for cat in category:
     data['cat'].append(cat[0])
   
   conn.close()  
   return data