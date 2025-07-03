from flask import Blueprint, render_template, request
from ..db import get_db_connection

bp = Blueprint('web_find', __name__, url_prefix='/find')

@bp.route('/<string:type>',methods=('GET','POST'))
def find(type):
    if type == "find_id":
        if request.method == 'POST':
            username = request.form['username']
            userphone = request.form['userphone']

            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT userid FROM users WHERE username=%s and userphone=%s"
                cursor.execute(sql,(username,userphone))
                result = cursor.fetchone()
            conn.close()
            
            if result:
                userid = result['userid']
                return render_template('find.html',find_id=True, userid=userid)
            else:
                return "<script>alert('찾으시는 ID가 없습니다.');history.back(-1);</script>"
        return render_template('find.html',find_id=True)
    
    elif type == "find_pw":
        if request.method == 'POST':
            userid = request.form['userid']
            username = request.form['username']
            userphone = request.form['userphone']

            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT userpw FROM users WHERE userid=%s and username=%s and userphone=%s"
                cursor.execute(sql,(userid,username,userphone))
                result = cursor.fetchone()
            conn.close()
            
            if result:
                userpw = result['userpw']
                return render_template('find.html',find_pw=True, userpw=userpw)
            else:
                return "<script>alert('찾으시는 PW가 없습니다.');history.back(-1);</script>"
        return render_template('find.html',find_pw=True)
    
    else:
        return "잘못된 접근입니다."
