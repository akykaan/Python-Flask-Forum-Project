from ast import Break
from asyncio.windows_events import NULL
from datetime import datetime
from re import U
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy import null
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('profile',__name__)

# profil sayfası açılın kısmı
@bp.route('/index')
def profile():
    return render_template('profile/profile.html') 


### Kişiye özel profil sayfası editleme işlemi
@bp.route('/<int:id>/edit',methods=('GET','POST'))
def edit(id):
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
        error = None

        
        if not nickname and password:
            error = 'nickname and password is required.'
        if nickname=="" and password=="":
            return redirect(url_for('profile.profile')) # 2 alan birden boş ile bizi tekrar aynı sayfaya atar

        if error is not None:
            flash(error)
        else:
            try:
                db = get_db()
                db.execute(
                    'UPDATE user SET nickname = ?, password = ?'
                    ' WHERE id = ?',
                    (nickname, generate_password_hash(password), g.user['id'])
                )
                db.commit()
            except:
                flash("Already user exist")
                return redirect(url_for('profile.edit',id=g.user['id']))
    db = get_db()
    users = db.execute(
        'SELECT id,nickname,password'
        ' FROM user u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchall()
    return render_template('profile/edit.html',users=users)
