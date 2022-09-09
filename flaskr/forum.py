from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('forum',__name__)


@bp.route('/user_profile',methods=['GET','POST'])
def profile():
    db = get_db()
    users = db.execute(
        'SELECT id,nickname,password'
        ' FROM user u'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchall()

    forums = db.execute(
        'SELECT f.title,f.body'
        ' FROM forum f JOIN user u ON f.user_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchall()
    return render_template('profile/index.html',users=users,forums=forums)


# Tüm girilen forum başlıklarını sql sorgusu ile listelemiş olduk.
@bp.route('/index')
def index():
    db = get_db()
    forums = db.execute(
        'SELECT f.id,f.user_id,u.nickname,created,title,body,is_active'
        ' FROM forum f JOIN user u ON f.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('forum/index.html',forums=forums)


# Forumda yeni bir başlık açmak için
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST': # İlk Sayfa açıldığında post işlemi olmayacak ve render_template çalışacak
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
            return redirect(url_for('forum.index')) # Post işleminden sonra bizi index fonksiyonuna gönderir ve açılan başlığı görmüş oluruz.
    return render_template('forum/create.html')


def check_comment(id,check_author=True):
    comment = get_db().execute(
        'SELECT user_id'
        ' FROM comment c JOIN user u ON c.user_id=u.id'
        ' WHERE c.id=?',
        (id,)
    ).fetchone()

    if check_author and comment['user_id']!=g.user['id']:
        print("yetki yok")
        abort(403)
    return comment

def get_forum(id, check_author=True):   # Verilen id ile ilgini forumun bilgilerini almak için 
    forum = get_db().execute(
        'SELECT f.id,user_id,created,title,body'
        ' FROM forum f JOIN user u ON f.user_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchone()

    if forum is None:
        abort(404, f"Forum id {id} doesn't exist.")
    if g.user['authority']==1:  # Database kısmında yetkisi 1 ile işaretlenen kişiler tüm yetkilere sahiptir.
        return forum
    if check_author and forum['user_id'] != g.user['id']:
        abort(403)
    
    return forum

@bp.route('/<int:id>/get_comment',methods=('GET','POST')) # Forumun sahip olduğu yorumları getirmek için 
def get_comment(id): # id ile hangi forumun yorumlarına gidildi onu öğrendik.
    db=get_db()      
    comments=db.execute(
        'SELECT c.body,c.forum_id,c.id,c.user_id,u.nickname'
        ' FROM comment c'
        ' INNER JOIN user u ON u.id = f.user_id'
        ' INNER JOIN forum f ON u.id = c.user_id'
        ' WHERE c.forum_id = ?'
        ' ORDER BY c.id DESC',
        (id,) # id'yi burada kullanıp sql sorgusu ile çektik.
    ).fetchall()
    
    return render_template('forum/get_comment.html',comments=comments)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    forum = get_forum(id)  # Önce hangi forum başlığı ve içeriği güncellenmeli onu get_forum ile belirledik.

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
                (title, body, id) # Belirlenen id'yi sql update ile kullanarak içeriğin değişmesini sağladık
            )
            db.commit()
            return redirect(url_for('forum.index'))

    return render_template('forum/update.html', forum=forum)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):  # Silinmesini istediğimiz forum'un id'sini buraya yollayıp onu sql komutu ile sildik
    get_forum(id) # bir ara bakılacak
    db = get_db()
    db.execute('DELETE FROM forum WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('forum.index'))


@bp.route('/<int:id>/comment',methods=['GET','POST'])
@login_required
def comment(id):
    if request.method == 'POST': #yorum ekleme işlemleri 
        body = request.form['body'] # eğer post değilse comment.html sayfasını açar 
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
            return redirect(url_for('forum.index'))  # yorum yaptıktan sonra ise forumun index sayfasına yönlendirir.
    return render_template('forum/comment.html')


@bp.route('/<int:id>/close_comment',methods=['GET'])
@login_required
def close_comment(id): # Gelen forum'un id'si buraya gönderdik ve sql komutu ile aktiflik durumunu değiştirdik.
    db = get_db()
    db.execute(
        'UPDATE forum set is_active = 0'
        ' WHERE forum.id=? AND user_id=? IN (SELECT authority FROM user WHERE authority=1)',
        (id,g.user['id'])
    ).fetchone()
    db.commit()
    return redirect(url_for('forum.index'))

@bp.route('/<int:id>/comment_edit',methods=['GET','POST'])
@login_required
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
                ' WHERE id=? AND (user_id=? OR (SELECT authority FROM user WHERE authority=1))',
                (body,created,id,g.user['id'])
            ).fetchone()
            db.commit()
            return redirect(url_for('forum.index'))
    return render_template('forum/comment.html')

@bp.route('/<int:id>/comment_delete',methods=['GET'])
@login_required
def comment_delete(id):
    check_comment(id)
    db = get_db()
    db.execute(
        'DELETE FROM comment ' 
        'WHERE id=?',
        (id,)
    ).fetchone()
    db.commit()

    return redirect(url_for('forum.index'))

