from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from ..exts import db
from ..utils import BaseModel


class User(BaseModel):
    __tablename__ = 'tb_user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(32), unique=True)
    avatar = db.Column(db.String(128))
    rgs_time = db.Column(db.DateTime, default=datetime.now)
    is_del = db.Column(db.Boolean, default=False)

    # 定义和用户关联的文章列表（一对多）
    articles = db.relationship('Article', backref='author', lazy=True)
    '''
    # 假设你已经有了一个用户实例 user  
    articles_by_user = user.articles
    articles是User模型的属性
    '''
    comments = db.relationship('Comment', backref='user')

    @property
    def password(self):
        # return self._password
        raise Exception('Access Not Allowed')

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self._password, pwd)


class Photo(BaseModel):
    __tablename__ = 'tb_photo'
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(128), nullable=False)
    photo_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.user_id'), nullable=False)


class AboutMe(BaseModel):
    __tablename__ = 'tb_about_me'
    me_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    me_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.user_id'))
    user = db.relationship('User', backref='about')


class MessageBoard(BaseModel):
    __tablename__ = 'tb_msg_board'
    bd_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    bd_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.user_id'), nullable=True)
    user = db.relationship('User', backref='messages')