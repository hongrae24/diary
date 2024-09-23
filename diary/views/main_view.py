from flask import Blueprint, render_template
from diary import Diary

from datetime import datetime

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def home():
    diary_list = Diary.query.all()
    return render_template("main.html", diary_list=diary_list)

@bp.route("/<date>")
def content(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        pass
    diary = Diary.query.get_or_404(date)
    return render_template("diary.html", diary=diary)