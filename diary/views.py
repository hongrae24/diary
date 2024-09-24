from datetime import datetime, date
from calendar import monthrange

from flask import Blueprint, render_template, redirect
from markdown import markdown

from diary import Diary, db


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
    dates = []
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
    diary = Diary.query.get(d)
    if diary is None:
        return render_template("content.html", day="/{0}/{1}/{2}".format(year, month, day), content="")
    else:
        return render_template("content.html", day="/{0}/{1}/{2}".format(year, month, day), content=markdown(diary.content))

@bp.route("/<int:year>/<int:month>/<int:day>/edit")
def edit(year, month, day):
    try:
        d = date(year, month, day)
    except ValueError:
        return redirect("/invalid_date")
    return ""

@bp.route("/<int:year>/<int:month>/<int:day>/del")
def delete(year, month, day):
    try:
        d = date(year, month, day)
    except ValueError:
        return redirect("/invalid_date")
    diary = Diary.query.get(d)
    if diary is None:
        res = False
    else:
        db.session.delete(diary)
        res = True
    return render_template("del.html", res=res)

@bp.route("/invalid_date")
def invalid_date():
    return "올바르지 않은 날짜입니다. <button onclick='location.href='/''>돌아가기</button>"