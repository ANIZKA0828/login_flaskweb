import os
from flask import Blueprint, render_template, request, url_for, redirect
from ..db import get_db_connection

bp = Blueprint('web_register', __name__, url_prefix='/register')

@bp.route('/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        userpw = request.form['userpw']
        username = request.form['username']
        userschool = request.form['userschool']
        userphone = request.form['userphone']
        if userid and userpw and username and userschool and userphone:
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("SELECT userid, userphone FROM users")
                    users = cursor.fetchall()

                    for user in users:
                        if userid == user['userid']:
                            return "<script>alert('사용 중인 ID입니다.');history.back(-1);</script>"
                        if userphone == user['userphone']:
                            return "<script>alert('가입 된 전화번호입니다.');history.back(-1);</script>"
                    
                    sql = """INSERT INTO users (userid, userpw, username, userschool, userphone) 
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (userid,userpw,username,userschool,userphone))
                    conn.commit()
                conn.close()
                return redirect(url_for('web_index.index'))
        else:
            return "<script>alert('빈칸이 존재합니다.');history.back(-1);</script>"
    else:
        return render_template('register.html')