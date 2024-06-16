from datetime import datetime
from ..utils import BaseModel
from ..exts import db


class Tag(BaseModel):
    __tablename__ = 'tb_tag'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    articles = db.relationship('Article', backref='tag')


class Article(BaseModel):
    __tablename__ = 'tb_article'
    art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_time = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.user_id'), nullable=False)
    comments = db.relationship('Comment', backref='article')
    tag_id = db.Column(db.Integer, db.ForeignKey('tb_tag.tag_id'), nullable=False)


class Comment(BaseModel):
    __tablename__ = 'tb_comment'
    cmt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.user_id'))
    art_id = db.Column(db.Integer, db.ForeignKey('tb_article.art_id'))
    cmt_time = db.Column(db.DateTime, default=datetime.now)