# 世济嘉缘相亲网

世济嘉缘是一个面向同济大学嘉定校区同学的相亲网站，为帮助广大单身男女脱单而开发的交友平台。

--- 

## 目录

- 项目简介
- 使用说明
  - 功能说明
  - 使用技术
- 安装部署
    - 依赖安装
    - 运行
- 开发与维护
    - 注意事项与说明
    - 项目目录结构
- 开发成员贡献
- Github地址
- 更新日志

---

## 项目简介

本项目是面向同济大学嘉定校区广大单身男女开发的相亲交友网站。该网站具有一般社交媒体的主要功能。
该项目目前主要具有的一些功能有：
1. 用户功能：
    - 注册、登陆、邮件令牌认证、修改与重置密码
    - 上传头像与修改个人信息

2. 基本功能：
    - 推送展示其他用户信息
    - 条件筛选展示用户信息

3. 互动功能：
    - 关注功能，并在个人主页显示粉丝与关注的人
    - 收发私信功能
    - 上传照片填充私人照片墙

---

## 使用说明

### 功能说明

1. 注册、登录、认证、填写与修改个人信息
   - 注册后系统向注册邮箱发送认证邮件，点击邮件中的链接完成用户认证
   - 第一次登录后自动跳转到填写信息页面，包括上传头像
   - 可以从左上角的导航栏个人头像下拉页中进入个人空间并修改信息
2. 用户可以查看、按条件筛选其他用户
   - 首页为随机推荐的其他用户
   - 点击导航栏中的搜索跳转到筛选页面，选择条件并搜索即可找到符合条件的用户
3. 用户可以上传照片并编辑自己的个人主页
   - 从右上角导航栏中进入个人主页
   - 可以在照片一栏中选择上传图片
   - 个人主页会显示其粉丝与关注的人
4. 用户之间可以互相关注与发送私信
   - 点击进入其他用户的个人主页后即可关注
   - 点击私信一栏即可对该用户发送消息
   - 导航栏中的私信列表可以查看收到的私信

---

### 使用技术

1. 后端采用flask框架，主要分为下列模块
   - auth用户模块，主要包括用户模型及其相关操作
   - main模块，包括推送及索引功能与个人主页
   - message私信模块，收发信息功能实现
2. 数据库为SQ Lite，数据库中的模型如下
   - user
   ```
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
   ```
   - 图片
   ```
   class Pictures(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)  #id 主键
    resource_url = db.Column(db.String(80))  #图片位置
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
   ```
   - 消息
   ```
   class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return '<Message {}>'.format(self.body)
   ```
   - 关注与被关注（自引用关系）
   ```
   class Follow(db.Model):
    __tablename__='follows'
    follower_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
   ```
3. 前端没有使用现成框架，为小组成员从base.html开始搭建，主要为html、css、JavaScript和bootstrap扩展。

## 安装部署

### 依赖安装

运行命令
```bash
pip install -r requirements.txt
```
直接快速安装依赖包。

### 运行

点击flasky.py
来运行此项目。项目正常启动后，可以通过访问本地 http://127.0.0.1:5000/ 进行查看。

### 项目目录结构
项目的目录结构如下（部分）：
```bash
.
├─venv    //虚拟环境配置
├─config.py   //默认配置文件，包括数据库路径与邮箱配置
├─database.sqlite    //数据库
├─flasky.py //框架运行入口
├─README //markdown文档
├─app    //后端框架
│  ├─auth      //用户等功能
│  ├─main      //主页等功能
│  ├─message   //私信功能后端
│  ├─static    //静态文件
│  ├─templates    //网页模板
│  ├─ 
│  └─models.py     //数据库模型
├─requirements.txt  //依赖包信息
└─
```
---

## 开发成员贡献

世济嘉缘项目组成员
### 马家昱：
后端框架，数据库模型设计，注册、登录、令牌认证、邮件、重置密码等用户基础功能，用户资料上传与修改，个人主页填充与编辑等。  


### 陈冠忠：
首页推送与筛选搜索功能，用户收发私信和粉丝关注功能，上传文件处理和图片显示功能。数据库关系与数据库测试, 前后端连接等。


### 周婉莹：
完成网站首页、条件筛选页、登录页、消息列表页、发送消息页、上传图片页、认证邮箱提示页、错误提示页、成功注册提示页，以及前后端连接工作。
### 罗格峰：
个人主页，包括显示个人信息的页面，照片集的页面，粉丝和关注的页面，制作导航栏将各页面关联，以及前后端交接的工作。
### 陶思月：
完成基础格式、更改密码页面、重置密码页面、注册发邮件页面，最终所有页面格式统一，模板继承的工作以及前后端连接工作。
### 黄继宣：
详细信息填写页、修改页，应用多种选择器，负责各种js部分完成特殊需求。其他工作有debug、辅助组员、参与前后端连接等。

---

## Github地址

- https://github.com/Group-3-in-CS10070901/web-development

---

## 更新日志