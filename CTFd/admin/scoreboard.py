from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint
from CTFd.utils import admins_only, is_admin, cache
from CTFd.models import db, Teams, Solves, Awards, Challenges, WrongKeys, Keys, Tags, Files, Tracking, Pages, Config, DatabaseError
from CTFd.scoreboard import get_standings, sum_cat

from CTFd import utils

admin_scoreboard = Blueprint('admin_scoreboard', __name__)

@admin_scoreboard.route('/admin/scoreboard')
@admin_scoreboard.route('/admin/scoreboard/teams')
@admins_only
def admin_scoreboard_view_teams():
    standings = get_standings(admin=True)
    return render_template('admin/scoreboard_teams.html', teams=standings)

@admin_scoreboard.route('/admin/scoreboard/flights')
@admins_only
def admin_scoreboard_view_flights():
    standings = get_standings(admin=True)
    return render_template('admin/scoreboard_flights.html', flights=sum_cat(standings, 2, admin=True))

@admin_scoreboard.route('/admin/scoreboard/squadrons')
@admins_only
def admin_scoreboard_view_squadrons():
    standings = get_standings(admin=True)
    return render_template('admin/scoreboard_squadrons.html', squadrons=sum_cat(standings, 3, admin=True))

@admin_scoreboard.route('/admin/scores')
@admins_only
def admin_scores():
    score = db.func.sum(Challenges.value).label('score')
    quickest = db.func.max(Solves.date).label('quickest')
    teams = db.session.query(Solves.teamid, Teams.name, score)\
        .join(Teams).join(Challenges).filter(Teams.banned == False)\
        .group_by(Solves.teamid).order_by(score.desc(), quickest)
    db.session.close()
    json_data = {'teams': []}
    for i, x in enumerate(teams):
        json_data['teams'].append({'place': i + 1, 'id': x.teamid, 'name': x.name, 'score': int(x.score)})
    return jsonify(json_data)
