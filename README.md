# 世济嘉缘相亲网

世济嘉缘是一个面向同济大学嘉定校区同学的相亲网站，为帮助广大单身男女脱单而开发的交友平台。

--- 

## 目录

- 项目简介
- 使用说明
  - 功能说明
- 安装部署
    - 依赖安装
    - 运行
- 开发与维护
    - 注意事项与说明
    - 项目目录结构
- 维护者
- Github地址
- 更新日志

---

## 项目简介

本项目是面向同济大学嘉定校区广大单身男女开发的相亲交友网站。该网站具有一般社交媒体的主要功能，相较于市面上其他网站，我们不仅加入了同性模块，还将用户群体从三次元扩展至了各个领域。本网站后端采用flask框架+SQ Lite数据库搭建，前端主要使用Bootstrap扩展。
该项目目前主要具有的一些功能有：
1. 用户可以注册、登录、认证、填写与修改个人信息
   
2. 用户可以查看、按条件筛选其他用户
   
3. 用户可以上传照片并编辑自己的个人主页
   
4. 用户之间可以互相关注与发送私信

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

## 维护者

世济嘉缘项目组成员
mjy、cgz、zwy、hjx、tsy、lgf
联系方式：majiayu5@163.com
---

## Github地址

- https://github.com/Group-3-in-CS10070901/web-development

---

## 更新日志