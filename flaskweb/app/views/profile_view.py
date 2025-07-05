import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from ..db import get_db_connection

bp = Blueprint('web_profile', __name__, url_prefix='/profile')

@bp.route('/', methods=('GET','POST'))
def userprofile():
    if request.method == 'POST':
        search_user = request.form['search_user']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE userid = %s or userphone = %s"
            cursor.execute(sql,(search_user,search_user))
            user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('profile.html', user=user)
        else:
            return "<script>alert('해당하는 사용자가 없습니다.');history.back(-1);</script>"

@bp.route('/<string:user_id>')
def profile(user_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE userid = %s"
        cursor.execute(sql,(user_id))
        user = cursor.fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@bp.route('/modify/<int:user_index>', methods=('GET', 'POST'))
def profile_modify(user_index):
    if request.method == 'POST':
        userid = request.form['userid']
        userpw = request.form['userpw']
        username = request.form['username']
        userphone = request.form['userphone']
        userschool = request.form['userschool']
        userimage = request.files['userimage']
        if userid and userpw and username and userphone:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                if userimage:
                    userimgname = userimage.filename

                    allow_extenstion = ['jpg','png','jpeg']
                    userimgext = userimgname.rsplit('.',1)[1]
                    if userimgext not in allow_extenstion:
                        return "<script>alert('허용되지 않은 파일형식입니다.');history.back(-1);</script>"
                    
                    Real_file_path = os.path.abspath(f"app\\static\\image\\{userimgname}")
                    userimage.save(Real_file_path)
                    
                    file_path = "LOAD_FILE('" + Real_file_path + "')"

                    sql = "UPDATE users SET userid = %s, userpw = %s, username = %s, userschool = %s, userphone = %s, userimgname = %s, userimage = %s  WHERE id = %s"
                    cursor.execute(sql,(userid,userpw,username,userschool,userphone,userimgname, file_path, user_index))
                    
                else:
                    sql = "UPDATE users SET userid = %s, userpw = %s, username = %s, userschool = %s, userphone = %s WHERE id = %s"
                    cursor.execute(sql,(userid,userpw,username,userschool, userphone, user_index))
                
                conn.commit()

                sql = "SELECT * FROM users WHERE id = %s"
                cursor.execute(sql,(user_index))
                user = cursor.fetchone()
                
                session['user_id'] = user['userid']
                session['username'] = user['username']
                return redirect(url_for('web_index.index'))          
    
        else:
            return "<script>alert('빈칸이 존재합니다.');history.back(-1);</script>"
        
    if request.method == 'GET':
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql,(user_index))
            user = cursor.fetchone()
        conn.close()
        return render_template('profile.html',modify=True, user=user)