import os
from flask import Blueprint, render_template, send_file ,request
from ..db import get_db_connection

bp = Blueprint('web_detail', __name__, url_prefix='/view')

@bp.route('/<int:post_id>',methods=('GET','POST'))
def view(post_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM posts WHERE id = %s"
            cursor.execute(sql,(post_id))
            post = cursor.fetchone()
            conn.close()
        if request.method == 'POST':
            password = request.form['password']
            
            if password == post['password']:
                  return render_template('view.html', post=post)
            else:
                  return "<script>alert('비밀번호가 일치하지 않습니다.'); history.back(-1);</script>"
        return render_template('view.html', post=post)

@bp.route('/download/<int:post_id>')
def file(post_id):  
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM posts WHERE id=%s"
            cursor.execute(sql,(post_id))
            post = cursor.fetchone()
        conn.close()

        file_path = os.path.abspath(f".\\files\\{post['file_name']}")

        return send_file(file_path)