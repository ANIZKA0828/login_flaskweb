from flask import Blueprint, render_template, request, url_for, redirect
from ..db import get_db_connection

bp = Blueprint('web_modify', __name__, url_prefix='/modify')

@bp.route('/<int:post_id>', methods=('GET', 'POST'))
def modify(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        password = request.form['password']
        if title and content:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT password FROM posts WHERE id = {post_id}")
                auth_pass = cursor.fetchone()
            conn.close()
            if auth_pass['password'] == password: 
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute(f"UPDATE posts SET title = '{title}', content = '{content}' WHERE id = {post_id}")
                    conn.commit()
                conn.close()
                return redirect(url_for('web_index.index'))
            else:
                return "<script>alert('비밀번호를 잘못 입력하였습니다.');history.back(-1);</script>"
        else:
            return "<script>alert('빈칸이 존재합니다.');history.back(-1);</script>"
    if request.method == 'GET':
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM posts WHERE id = {post_id}")
            post = cursor.fetchone()
        conn.close()
        return render_template('modify.html', post=post)