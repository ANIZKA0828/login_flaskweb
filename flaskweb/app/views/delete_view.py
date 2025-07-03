from flask import Blueprint, url_for, redirect
from ..db import get_db_connection

bp = Blueprint('web_delete', __name__, url_prefix='/delete')

@bp.route('/<int:post_id>')
def delete(post_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM posts WHERE id = %s"
        cursor.execute(sql,(post_id))
        conn.commit()
    conn.close()
    return redirect(url_for('web_index.index'))