import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
        db = get_db()
        error = None
        if not nickname:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        authority=0 # default 0 all user value
        if nickname=="moderator": # yes its bad
            authority=1
        # üye olurken verilen nickname va password'ü alır ve password'ü hashler     
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (nickname, password,authority) VALUES (?, ?, ?)",
                    (nickname, generate_password_hash(password),authority),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {nickname} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
        
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE nickname = ?', (nickname,)
        ).fetchone()

        if user is None:
            error = 'Incorrect nickname.'
        elif not check_password_hash(user['password'], password): 
            error = 'Incorrect password.'

        # giriş yaparken db'de kayıtlı olan hashlı şifre ile girilen şifre aynı mı diye bakar 
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('forum.index'))

        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id') # session bilgisi olan kullanıcı dbden çeker 

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()   

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login')) # siteden çıkış işlemleri session bilgisi kesilir 

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view