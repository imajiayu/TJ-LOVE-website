import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    #邮件配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'tj_findlove@163.com'
    MAIL_PASSWORD = 'PBEPIXUTHMWHMGGP'
    FLASKY_MAIL_SUBJECT_PREFIX = '[世济嘉缘]'
    FLASKY_MAIL_SENDER = '世济嘉缘<tj_findlove@163.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #上传文件路径
    UPLODE_FOLDER = basedir+"/app/static/"

    @staticmethod
    def init_app(app):
        pass

#数据库路径
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database.sqlite')

config = {
    'default': DevelopmentConfig
}
