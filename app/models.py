from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from flask_moment import datetime

#关注关联表模型   
class Follow(db.Model):
    __tablename__='follows'
    follower_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)

#用户存在数据库中的模型
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)#id 主键
    email = db.Column(db.String(64), unique=True, index=True)#注册邮箱
    username = db.Column(db.String(64), unique=True, index=True)#用户名
    password_hash = db.Column(db.String(128))#hash密码
    confirmed = db.Column(db.Boolean, default=False)#是否认证

    
    nickname=db.Column(db.String(64), unique=True, index=True)#昵称
    main_image_url = db.Column(db.String(80))#头像
    gender = db.Column(db.String(80))#性别
    height = db.Column(db.Integer)#身高
    age=db.Column(db.Integer)#年龄
    size=db.Column(db.String(80))#体型
    education=db.Column(db.String(80))#学历
    occupation= db.Column(db.String(80))#工作
    love_state = db.Column(db.String(80))#感情状态
    sexuality = db.Column(db.String(80))#性取向
    date_of_birth = db.Column(db.String(80))  #出身年月日
    age = db.Column(db.Integer)  #年龄
    salary = db.Column(db.Integer) #月薪
    location = db.Column(db.String(80))  #位置
    constellation=db.Column(db.String(80))  #星座
    contact_information = db.Column(db.String(80))  #联系方式
    about_me = db.Column(db.String(80))  #个性签名
    
    #个人相册
    picture_num = db.Column(db.Integer, default=0)
    pictures = db.relationship('Pictures', backref='owner', lazy='select')

    #关注
    followed=db.relationship('Follow',foreign_keys=[Follow.follower_id],backref=db.backref('follower',lazy='joined'),lazy='dynamic',cascade='all,delete-orphan')
    followers=db.relationship('Follow',foreign_keys=[Follow.followed_id],backref=db.backref('followed',lazy='joined'),lazy='dynamic',cascade='all,delete-orphan')

    #消息
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    
    #查询用户未读信息条数
    def new_messages(self):
        
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    #试图访问密码时报错
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    #生成密码散列
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #验证密码散列
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #生成认正令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    #认证令牌是否一致
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    #生成重置密码令牌
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    #重置密码
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

        
    def __repr__(self):
        return '<User %r>' % self.username

#图片模型
class Pictures(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)  #id 主键
    resource_url = db.Column(db.String(80))  #图片位置
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



#消息模型
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return '<Message {}>'.format(self.body)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
