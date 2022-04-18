from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('forum', __name__)

@bp.route('/index')
def index():
    db = get_db()
    forums = db.execute(
        'SELECT f.id,user_id,created,title,body'
        ' FROM forum f JOIN user u ON f.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('forum/index.html',forums=forums)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO forum (title, body, user_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('forum.index'))

    return render_template('forum/create.html')

def get_forum(id, check_author=True):
    forum = get_db().execute(
        'SELECT f.id,user_id,created,title,body'
        ' FROM forum f JOIN user u ON f.user_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchone()

    if forum is None:
        abort(404, f"Forum id {id} doesn't exist.")

    if check_author and forum['user_id'] != g.user['id']:
        abort(403)

    return forum

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    forum = get_forum(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE forum SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('forum.index'))

    return render_template('forum/update.html', forum=forum)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_forum(id)
    db = get_db()
    db.execute('DELETE FROM forum WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('forum.index'))