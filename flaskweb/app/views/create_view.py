import os
from flask import Blueprint, render_template, request, url_for, redirect
from ..db import get_db_connection

bp = Blueprint('web_create', __name__, url_prefix='/create')

@bp.route('/<string:userid>', methods=('GET', 'POST'))
def create(userid):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        writer = request.form['writer']
        password = request.form['password']
        file = request.files['file']
        if title and content and writer:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                if file:
                    file_name = file.filename
                    Real_file_path = os.path.abspath(f".\\files\\{file_name}")
                    file.save(Real_file_path)

                    file_path = "LOAD_FILE('" + Real_file_path + "')"

                    sql = """INSERT INTO posts (title, content, writer, password, file_name, file_media) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (title,content,writer,password,file_name,file_path))

                else:
                    sql = """INSERT INTO posts (title, content, writer, password) 
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql, (title,content,writer,password))
                conn.commit()
                conn.close()
                return redirect(url_for('web_index.index'))
        else:
            return "<script>alert('빈칸이 존재합니다.');history.back(-1);</script>"
        
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE userid = %s"
        cursor.execute(sql, (userid))
        user = cursor.fetchone()
    return render_template('create.html',user=user)