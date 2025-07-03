from flask import Blueprint, render_template, request, session, redirect, url_for
from ..db import get_db_connection

bp = Blueprint('web_index', __name__, url_prefix='/')

@bp.route('/', methods=('GET','POST'))
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        search_type = request.form['search_type']
        search_name = request.form['search_name']
        with conn.cursor() as cursor:
            if search_type == 'all':
                cursor.execute(f"SELECT * FROM posts WHERE title LIKE '%{search_name}%' OR content LIKE '%{search_name}%' OR writer LIKE '%{search_name}%'")
            else:
                cursor.execute(f"SELECT * FROM posts WHERE {search_type} LIKE '%{search_name}%'")
                    
            posts = cursor.fetchall()
    else:     
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts ORDER BY id DESC")
            posts = cursor.fetchall()
    conn.close()

    user_id = session.get('user_id')
    username = session.get('username')
    return render_template('index.html', posts=posts, user_id=user_id, username=username)


@bp.route('/login/', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        user_id = request.form['userid']
        user_pw = request.form['userpw']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            if user_id and user_pw:
                sql = "SELECT userpw FROM users WHERE userid=%s"
                cursor.execute(sql, (user_id))
                real_pw = cursor.fetchone()
            else:
                return "<script>alert('빈칸이 존재합니다.');history.back(-1);</script>"
            
            if real_pw and real_pw['userpw'] == user_pw:
                sql = "SELECT * FROM users WHERE userid=%s"
                cursor.execute(sql,(user_id))
                user = cursor.fetchone()
                session.clear()
                session['user_id'] = user_id
                session['username'] = user['username']
                return redirect(url_for('web_index.index'))
            else:
                return "<script>alert('아이디 혹은 비밀번호가 일치하지 않습니다.');history.back(-1);</script>"

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('web_index.index'))