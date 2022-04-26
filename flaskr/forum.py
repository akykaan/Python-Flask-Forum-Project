from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('forum',__name__)

@bp.route('/<int:id>/user_profile',methods=('GET','POST'))
def profile(id):
    db = get_db()
    users = db.execute(
        'SELECT id,nickname,password'
        ' FROM user u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchall()

    forums = db.execute(
        'SELECT f.title,f.body'
        ' FROM forum f JOIN user u ON f.user_id = u.id'
        ' WHERE u.id = ?',
        (id,)
    ).fetchall()
    return render_template('profile/index.html',users=users,forums=forums)

@bp.route('/index')
def index():
    db = get_db()
    forums = db.execute(
        'SELECT f.id,user_id,created,title,body,is_active'
        ' FROM forum f '
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
                'INSERT INTO forum (title, body, user_id,is_active)'
                ' VALUES (?, ?, ?,?)',
                (title, body, g.user['id'],True)
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
    if g.user['authority']==1:
        return forum
    if check_author and forum['user_id'] != g.user['id']:
        abort(403)
    
    return forum


@bp.route('/<int:id>/get_comment',methods=('GET','POST'))
def get_comment(id):
    db=get_db()      
    comments=db.execute(
        'SELECT c.body,c.forum_id,c.id'
        ' FROM comment c INNER JOIN user u ON u.id=f.user_id'
        ' INNER JOIN forum f ON f.id=c.forum_id'
        ' WHERE c.forum_id = ?'
        ' ORDER BY c.id DESC',
        (id,)
    ).fetchall()
    
    return render_template('forum/get_comment.html',comments=comments)

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

@bp.route('/<int:id>/comment',methods=['GET','POST'])
@login_required
def comment(id):
    if request.method == 'POST':
        body = request.form['body']
        created=datetime.now().strftime('%Y-%m-%d')
        error = None
        
        if not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db=get_db()
            db.execute(
                'INSERT INTO comment(user_id,forum_id,created,body)'
                ' VALUES(?,?,?,?)',
                (g.user['id'],id,created,body)
            )
            db.commit()
            return redirect(url_for('forum.index'))
    return render_template('forum/comment.html')

@bp.route('/<int:id>/close_comment',methods=['GET'])
def close_comment(id):
    db = get_db()
    db.execute(
        'UPDATE forum set is_active = 0'
        ' WHERE forum.id=?',
        (id,)
    ).fetchone()
    db.commit()
    return redirect(url_for('forum.index'))

@bp.route('/<int:id>/comment_edit',methods=['GET','POST'])
def comment_edit(id):
    if request.method == 'POST': 
        body = request.form['body']
        created=datetime.now().strftime('%Y-%m-%d')
        error = None
        
        if not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE comment set body = ?, created = ?'
                ' WHERE id=?',
                (body,created,id,)
            ).fetchone()
            db.commit()
            return redirect(url_for('forum.index'))
    return render_template('forum/comment.html')

@bp.route('/<int:id>/comment_delete',methods=['GET'])
def comment_delete(id):
    db = get_db()
    db.execute(
        'DELETE FROM comment'
        ' WHERE id=?',
        (id,)
    ).fetchone()
    db.commit()
    return redirect(url_for('forum.index'))

