from controller import searchs as searchs_ct 
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user


searchs_bp = Blueprint('searchs', __name__)

@searchs_bp.route("/search", methods=["GET"])
def get_search():
    data = searchs_ct.get_search()
    return render_template('searchs/get_searchs.html', data=data)