import os


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:010126@127.0.0.1:3306/flaskstudy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    UPLOAD_ICON_DIR = os.path.join(STATIC_DIR, r'upload\icon')
    UPLOAD_PHOTO_DIR = os.path.join(STATIC_DIR, r'upload\photo')
    UPLOAD_VIDEO_DIR = os.path.join(STATIC_DIR, r'upload\video')
    UPLOAD_NEW_VIDEO_DIR =os.path.join(STATIC_DIR, r'upload\video')
    UPLOAD_PICTURE_WOPAI_DIR = os.path.join(STATIC_DIR, r'picture\wopai')
    UPLOAD_PICTURE_JIQIU_DIR = os.path.join(STATIC_DIR, r'picture\jiqiu')


class DevelopmentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENv = 'production'
    DEBUG = False
