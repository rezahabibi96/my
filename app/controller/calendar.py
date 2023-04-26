from utils.config import Config
from calendar import monthrange
import sqlite3


DB = Config.DB

def get(month, year):
  conn = sqlite3.connect(DB)
  cursor = conn.cursor()

  # DATE RANGE CALCULATION FORMULA
  daysInMonth = str(monthrange(year, month)[1])
  month = month if month>10 else "0" + str(month)
  dateYM = str(year) + "-" + str(month) + "-"
  start = dateYM + "01 00:00:00"
  end = dateYM + daysInMonth + " 23:59:59"

  cursor.execute(
    "SELECT * FROM `events` WHERE ((`start` BETWEEN ? AND ?) OR (`end` BETWEEN ? AND ?) OR (`start` <= ? AND `end` >= ?))",
    (start, end, start, end, start, end)
  )
  rows = cursor.fetchall()
  
  if len(rows)==0:
    return None

  data = {}
  for r in rows:

    # NEED OPTIMIZED WITH AJAX
    
    cursor.execute(
      "SELECT `id_category` FROM `events_categories` WHERE (`id_event` = ?)", (str(r[0]),)
    )
    cat = []
    for c in cursor.fetchall():
      cat.append(c[0])

    data[r[0]] = {
      "s" : r[1], "e" : r[2],
      "c" : r[4], "b" : r[5],
      "t" : r[3], 
      "det" : r[6],
      "cat" : cat
    }
  conn.close()  
  return data

def save (start, end, txt, color, bg, det, cat, id=None):
  conn = sqlite3.connect(DB)
  cursor = conn.cursor()

  data = (start, end, txt, color, bg, det,)
  
  if id is None:
    sql = "INSERT INTO `events` (`start`, `end`, `text`, `color`, `bg`, `detail`) VALUES (?,?,?,?,?,?)"
    cursor.execute(sql, data)
   
    data = []
    id_event = cursor.lastrowid

    if not cat=='':
      for val in cat.split(','):
        data.append((id_event, val,))

      sql = "INSERT INTO `events_categories` (`id_event`, `id_category`) VALUES (?,?)"
      cursor.executemany(sql, data)
  else:
    sql = "UPDATE `events` SET `start`=?, `end`=?, `text`=?, `color`=?, `bg`=?, `detail`=? WHERE `id`=?"
    data = data + (id,)
    cursor.execute(sql, data)
    cursor.execute("DELETE FROM `events_categories` WHERE `id_event`=?", (id,))

    data = []
    id_event = id
    
    for val in cat.split(','):
      data.append((id_event, val,))

    sql = "INSERT INTO `events_categories` (`id_event`, `id_category`) VALUES (?,?)"
    cursor.executemany(sql, data)

  conn.commit()
  conn.close()
  return True

def cut(id):
  conn = sqlite3.connect(DB)
  cursor = conn.cursor()

  cursor.execute("DELETE FROM `events` WHERE `id`=?", (id,))
  cursor.execute("DELETE FROM `events_categories` WHERE `id_event`=?", (id,))

  conn.commit()
  conn.close()
  return True