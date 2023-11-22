from utils.config import Config
from flask_login import current_user
from flask import jsonify, request, render_template, redirect
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

def get_form_bimbingan_by_ep(id_ep, action_ep):
   if request.method == 'GET': 
        return render_template('participants/get_form_bimbingan_by_ep.html', id_ep=id_ep, action_ep=action_ep)
   else:
      data = (id_ep, 
              request.form['materi-diskusi'], 
              request.form['link-resource'] if request.form['link-resource'] else None,
              request.form['lama-durasi'] if request.form['lama-durasi'] else None, 
              request.form['tanggal-bimbingan'], )
      
      conn = sqlite3.connect(DB)
      cursor = conn.cursor()
      
      sql = "INSERT INTO `bimbingan` (`id_event_participant`, `materi_diskusi`, `link_resource`, `durasi`, `schedule`) VALUES (?,?,?,?,?)"
      cursor.execute(sql, data)

      conn.commit()
      conn.close()
      
      return redirect(f'/ep/{id_ep}/bimbingan')
   
def get_form_bimbingan_by_id(id_ep, action_ep, id_bimbingan):
   if request.method == 'GET':
      conn = sqlite3.connect(DB)
      cursor = conn.cursor()

      cursor.execute("SELECT * FROM `bimbingan` WHERE (`id` = ?)", (id_bimbingan,))
      data_ep = cursor.fetchone()
      return render_template('participants/get_form_bimbingan_by_id.html', id_ep=id_ep, action_ep=action_ep, id_bimbingan=id_bimbingan, data_ep=data_ep)
   else:
      data = (request.form['materi-diskusi'], 
              request.form['link-resource'] if request.form['link-resource'] else None,
              request.form['lama-durasi'] if request.form['lama-durasi'] else None, 
              request.form['tanggal-bimbingan'], 
              id_bimbingan, )
      
      conn = sqlite3.connect(DB)
      cursor = conn.cursor()
      
      sql = "UPDATE `bimbingan` SET `materi_diskusi`=?, `link_resource`=?, `durasi`=?, `schedule`=? WHERE `id`=?"
      cursor.execute(sql, data)

      conn.commit()
      conn.close()
      
      return redirect(f'/ep/{id_ep}/bimbingan')

def join():
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()
   
   users = cursor.execute("SELECT `id`, `fullname` FROM `users` WHERE (`username` = ?)", (request.json["username"],)).fetchone()
   id_mahasiswa = users[0]
   nama_mahasiswa = users[1]

   students = cursor.execute("SELECT `semester` FROM `students` WHERE (`id_student` = ?)", (id_mahasiswa,)).fetchone()
   semester = students[0]

   data = (request.json["id_event"], request.json["title_event"], id_mahasiswa,
           nama_mahasiswa, request.json["id_dosen"], request.json["nama_dosen"],
           request.json["id_subevent"], request.json["keterangan_subevent"], semester,)

   sql = "INSERT INTO `events_participants` (`id_event`, `title_event`, `id_mahasiswa`, `nama_mahasiswa`, `id_dosen`, `nama_dosen`, `id_subevent`, `keterangan_subevent`, `semester`) VALUES (?,?,?,?,?,?,?,?,?)"
   cursor.execute(sql, data)

   conn.commit()
   conn.close()

   return jsonify({"result": "OK"})