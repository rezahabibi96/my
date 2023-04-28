controllers calender.py cut cursor.execute("UPDATE `subevents` SET `deleted`=1 WHERE `id`=?", (request.json["id"],))
controllers events.py get_event id_notfound 