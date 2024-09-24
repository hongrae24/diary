from flask import Blueprint, render_template, redirect
from diary import Diary

from datetime import datetime, date
from calendar import monthrange

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def home():
    t = datetime.today()
    return redirect("/{0}/{1}".format(t.year, t.month))

@bp.route("/<int:year>/<int:month>")
def calendar(year, month):
    if month < 1 or 12 < month:
        month -= 1
        year += month // 12
        month %= 12
        month += 1
        return redirect("/{0}/{1}".format(year, month))
    dates = [] # 0 is invalid, 1 is valid but has no data, 2 has data 
    first, last = monthrange(year, month)
    for i in range(first):
        dates.append((0, False))
    for i in range(1, last + 1):
        d = date(year, month, i)
        if Diary.query.get(d) is None:
            dates.append((i, False))
        else:
            dates.append((i, True))
    while len(dates) % 7:
        dates.append((0, False))
    return render_template("cal.html", year=year, month=month, dates=dates)

@bp.route("/<int:year>/<int:month>/<int:day>")
def content(year, month, day):
    try:
        d = date(year, month, day)
    except ValueError:
        return redirect("/invalid_date")
    diary = Diary.query.get_or_404(d)
    return render_template("diary.html", diary=diary)

# TODO: make button to go today
@bp.route("/invalid_date")
def invalid_date():
    return "Invalid date"