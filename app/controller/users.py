from utils.config import Config
from flask_login import current_user, login_required
import requests
import sqlite3
import random


DB = Config.DB

def get_profile():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM `events` WHERE (`id` = ?)", (1,))
    user = cursor.fetchone()
    
    cat = random.choice(['education', 'failure', 'inspirational', 'success'])
    url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(cat)
    
    response = requests.get(url, headers={'X-Api-Key': '/2ngwp4luVWlea+ksewYXA==R0XrwKWPbcfJ37Yh'})
    
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

    conn.close()