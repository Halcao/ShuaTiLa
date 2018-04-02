from flask_login import UserMixin
from . import login_mamager
from . import config
import pymysql


class User(UserMixin):
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']


@login_mamager.user_loader
def load_user(user_id):
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    sql = 'SELECT Student_name FROM student where Student_id = %s'
    cur.execute(sql, (user_id))
    student = cur.fetchall()
    name = list(student[0])[0]
    return User(id=user_id, name=name)
