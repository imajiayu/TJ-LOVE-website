import os
import cv2
from flask import render_template, redirect, request, url_for, flash,current_app,flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email


#判断上传图片的类型
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#替换图片
def delete_pic(dirpath,userid):
    for item in os.listdir(dirpath):
        for ext in ALLOWED_EXTENSIONS:
            if str(userid)+'.'+ext in item:
                os.remove(dirpath+str(userid)+'.'+ext)
    return


#裁剪并缩放图片
def edit_pic(filename):
    image=cv2.imread(filename)
    width=image.shape[1]
    height=image.shape[0]
    r=min(width,height)
    dst1=image[int((height-r)/2):int((height+r)/2),int((width-r)/2):int((width+r)/2)]
    dst2=cv2.resize(dst1,(500,500))
    cv2.imwrite(filename,dst2)
    return 

#若未认证
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

#跳转至需要验证
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/email_confirm.html')

#登录路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user)
            if (not user.confirmed):
                return redirect(url_for('auth.toConfirm'))
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        else:
            flash('错误的邮箱或密码。')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')

#登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功退出！')
    return redirect(url_for('auth.login'))

#注册路由
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        user = User(email=request.form['email'],
                    username=request.form['username'],
                    password=request.form['password'],
                    main_image_url="main_image/0.jpg")
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认您的邮箱',
                   'auth/email/confirm', user=user, token=token)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/toConfirm')
def toConfirm():
    return render_template('auth/email_confirm.html')

#认证时电子邮件中的链接
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('您已成功认证！')
        return redirect(url_for('auth.detailed_information'))
    else:
        flash('验证链接是无效或过期的！')
    return redirect(url_for('main.index'))

#认证
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认您的邮箱',
               'auth/email/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已发送至您的邮箱！')
    return redirect(url_for('auth.toConfirm'))

#注册时填写详细信息
@auth.route('/detailed_information', methods=['GET', 'POST'])
@login_required
def detailed_information():
    if request.method=='POST':
        app = current_app._get_current_object()
        main_image = request.files['main_image']
        user = current_user._get_current_object()


        user.nickname = request.form['nickname']
        user.gender = request.form['gender']
        user.height = request.form['height']
        user.size = request.form['size']
        user.education = request.form['education']
        user.occupation = request.form['occupation']
        user.love_state = request.form['love_state']
        user.sexuality = request.form['sexuality']
        user.date_of_birth = request.form['date_of_birth']
        user.salary = request.form['salary']
        user.location = str(request.form['province'] + ' ' + request.form['city'])
        user.contact_information = request.form['contact_information']
        user.about_me = request.form['about_me']
        user.occupation=request.form['occupation']
        user.constellation = request.form['constellation']
        user.age = int(2020 - int(user.date_of_birth[0:4]))
        
        if allowed_file(main_image.filename):
            user.main_image_url = 'main_image/' + str(current_user.id) + '.' + str(main_image.filename.rsplit('.', 1)[1])
            delete_pic(app.config['UPLODE_FOLDER']+'main_image/',current_user.id)
            main_image.save(app.config['UPLODE_FOLDER'] + user.main_image_url)
            edit_pic(app.config['UPLODE_FOLDER']+user.main_image_url)
            flash('上传成功！')
        else:
            flash('上传图片不符合类型！')
            return redirect(url_for('auth.detailed_information'))

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('auth/detailed_information.html')

#修改个人信息
@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user._get_current_object()
    if request.method=='POST':
        app = current_app._get_current_object()
        main_image = request.files['main_image']
        user = current_user._get_current_object()


        user.nickname = request.form['nickname']
        user.gender = request.form['gender']
        user.height = request.form['height']
        user.size = request.form['size']
        user.education = request.form['education']
        user.occupation = request.form['occupation']
        user.love_state = request.form['love_state']
        user.sexuality = request.form['sexuality']
        user.date_of_birth = request.form['date_of_birth']
        user.salary = request.form['salary']
        user.location = str(request.form['province'] + ' ' + request.form['city'])
        user.contact_information = request.form['contact_information']
        user.about_me = request.form['about_me']
        user.occupation=request.form['occupation']
        user.constellation = request.form['constellation']
        user.age = int(2020 - int(user.date_of_birth[0:4]))
        
        if allowed_file(main_image.filename):
            user.main_image_url = 'main_image/' + str(current_user.id) + '.' + str(main_image.filename.rsplit('.', 1)[1])
            delete_pic(app.config['UPLODE_FOLDER']+'main_image/',current_user.id)
            main_image.save(app.config['UPLODE_FOLDER'] + user.main_image_url)
            edit_pic(app.config['UPLODE_FOLDER']+user.main_image_url)
            flash('上传成功！')
        else:
            flash('上传图片不符合类型！')
            return redirect(url_for('auth.edit_profile'))

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.homepage_information', user_id=current_user.id))
    return render_template('auth/edit_profile.html',user=user)
 




#更改密码
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method=='POST':
        if current_user.verify_password(request.form['old_password']):
            current_user.password = request.form['new_password']
            db.session.add(current_user)
            db.session.commit()
            flash('密码修改成功!')
            return redirect(url_for('main.index'))
        else:
            flash('旧密码不正确！')
    return render_template("auth/change_password.html")

#重置密码
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    if request.method=='POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置您的密码',
                       'auth/email/reset_password',
                       user=user, token=token)
            flash('一封重置密码的电子邮件已发送至您的邮箱！')
            return redirect(url_for('auth.login'))
        flash('该邮箱未注册！')
    return render_template('auth/forget_password.html')


#重置密码时电子邮件中的路由
@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if request.method == "POST":
        if User.reset_password(token, request.form['new_password']):
            db.session.commit()
            flash('您的密码已重置')
            return redirect(url_for('auth.login'))
        else:
            flash('无效或过期的连接！')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',token=token)




