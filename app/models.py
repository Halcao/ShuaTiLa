from flask_login import UserMixin
from . import login_mamager
from . import config
import pymysql


class User(UserMixin):
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.email = kwargs['email']
        self.if_admin = kwargs['if_admin']


@login_mamager.user_loader
def load_user(user_id):
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    sql = 'SELECT Student_name, Email, If_admin FROM student where Student_id = %s'
    cur.execute(sql, (user_id))
    student = cur.fetchall()
    info = list(student[0])
    name = info[0]
    email = info[1]
    if_admin = info[2]
    return User(id=user_id, name=name, email=email, if_admin=if_admin)
