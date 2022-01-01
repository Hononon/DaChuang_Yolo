from exts import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(30))
    video = db.Column(db.String(100), default=False)
    new_video = db.Column(db.String(100), default=False)
    picture_wopai = db.Column(db.String(100), default=False)
    picture_wopai_new = db.Column(db.String(100), default=False)
    picture_jiqiu = db.Column(db.String(100), default=False)
    picture_jiqiu_new = db.Column(db.String(100), default=False)
    icon = db.Column(db.String(100), default=False)
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    articles = db.relationship('Article', backref='user')

    def __str__(self):
        return self.username
