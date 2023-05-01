from utils.config import Config
from flask_login import current_user
import sqlite3


DB = Config.DB

def get_participants_by_events(id_event=None):
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM `events_participants` WHERE (`id_event` = ?)", (id_event,))
   data = cursor.fetchall()

   title = cursor.execute("SELECT text FROM `events` WHERE (`id` = ?)", (id_event,)).fetchone()

   conn.close()  
   return data, title

def get_bimbingan_by_ep(id_ep=None):
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()

   cursor.execute("SELECT * FROM `bimbingan` WHERE (`id_event_participant` = ?)", (id_ep,))
   data = cursor.fetchall()

   event = cursor.execute("SELECT `nama_dosen`, `title_event`, `nama_mahasiswa`, `id_mahasiswa`, `id_dosen` FROM `events_participants` WHERE (`id` = ?)", (id_ep,)).fetchone()
   member = cursor.execute("SELECT `nama_dosen`, `title_event`, `nama_mahasiswa`, `id_mahasiswa` FROM `member` WHERE ((`id_ep` = ?) AND (`id_mahasiswa` = ?))", (id_ep, current_user.id,)).fetchone()

   if current_user.role == 'dosen' and current_user.id != event[4]:
      return None, None, False
   
   if current_user.role == 'mahasiswa':
      if not current_user.id == event[3] and not member:
         return None, None, False

   if member:
      event = member

   conn.close()  
   return data, event, True