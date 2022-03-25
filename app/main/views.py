from flask import render_template,current_app,request,redirect,flash,current_app,url_for
from flask_login import current_user,login_required
from . import main
from .. import db
from sqlalchemy.sql.expression import func
from ..models import User, Pictures,Follow
import os

#判断图片类型
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#存放search页面跳转前选择的选项
class Myclass(object):
    class struct(object):
        def __init__(self,gender,sexuality,age_type,height_type,size,income_type,education,occupation,constellation,love_state):
            self.gender = gender
            self.sexuality=sexuality
            self.age_type=age_type
            self.height_type=height_type
            self.size=size
            self.income_type=income_type
            self.education=education
            self.occupation=occupation
            self.constellation=constellation
            self.love_state=love_state
    def makeStruct(self,gender,sexuality,age_type,height_type,size,income_type,education,occupation,constellation,love_state):
            return self.struct(gender,sexuality,age_type,height_type,size,income_type,education,occupation,constellation,love_state)
myclass=Myclass()

#主页
@main.route('/')
def index():
    users=User.query.order_by(func.random()).all()
    length=len(users)
    return render_template('main/index.html',users=users,length=length)

#条件筛选
@main.route('/search',methods=['GET', 'POST'])
def search():
    searched=False
    selected_form=myclass.makeStruct('性别','取向','年龄','身高','体型','收入','教育经历','职业','星座','婚姻状况')
    if request.method == "POST":
        
        gender=request.form.get("gender")
        sexuality=request.form.get("sexuality")
        age_type=request.form.get("age_type")
        height_type=request.form.get("height_type")
        size=request.form.get("size")
        income_type=request.form.get("income_type")
        education=request.form.get("education")
        occupation=request.form.get("occupation")
        constellation=request.form.get("constellation")
        love_state=request.form.get("love_state")

        gender_filter=[]
        sexuality_filter=[]
        age_min=0
        age_max=10000
        height_min=0
        height_max=10000
        size_filter=[]
        income_min=0
        income_max=100000000
        education_filter=[]
        occupation_filter=[]
        constellation_filter=[]
        love_state_filter=[]
        

        if gender=='性别' or gender=='不限':
            gender_filter=['男','女','保密']
        else:
            gender_filter.append(gender)

        if sexuality =='取向' or sexuality =='不限':
            sexuality_filter=['男','女','双性恋','保密']
        else:
            sexuality_filter.append(sexuality)

        
        if age_type=='18岁以下':
            age_max=18
        elif age_type=='18-25岁':        
            age_min=18
            age_max=25
        elif age_type=='25-30岁':
            age_min=25
            age_max=30
        elif age_type=='30-40岁':
            age_min=30
            age_max=40
        elif age_type=='40-50岁':
            age_min=40
            age_max=50
        elif age_type=='50岁以上':
            age_min=50

        if height_type=='150及以下':
            height_max=150
        elif height_type=='150-160':
            height_min=150
            height_max=160  
        elif height_type=='160-170':
            height_min=160
            height_max=170  
        elif height_type=='170-180':
            height_min=170
            height_max=180  
        elif height_type=='180以上':
            height_min=180
        
        if size=='体型' or size=='体型不限':
            size_filter=['偏瘦','中等','微胖','保密']
        else:
            size_filter.append(size)

        if income_type=='5000以下':
            income_max=5000
        elif income_type=='5000-10000':
            income_min=5000
            income_max=10000
        elif income_type=='10000-20000':
            income_min=10000
            income_max=20000
        elif income_type=='20000-50000':
            income_min=20000
            income_max=50000
        elif income_type=='50000以上':
            income_min=50000
        elif income_type=='马云':
            income_min=100000000

        if education=='教育经历' or education=='不限':
            education_filter=['高中及以下','大学本科','硕士生','博士生及以上','保密']
        else:
            education_filter.append(education)
        
        if occupation=='职业' or occupation=='不限':
            occupation_filter=['程序猿（媛）','教育','医疗','金融','学生','自由职业','美少女','霸道总裁','视频博主','超级英雄','纸片人','冒险者','修仙者','演员','其他','保密']
        else:
            occupation_filter.append(occupation)

        if constellation=='星座' or constellation=='星座不限':
            constellation_filter=['水瓶座','双鱼座','白羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天秤座','天蝎座','射手座','魔羯座','保密']
        else:
            constellation_filter.append(constellation)

        if love_state=='婚姻状况' or love_state=='婚姻状况不限':
            love_state_filter=['离异','未婚','丧偶','保密']
        else:
            love_state_filter.append(love_state)

        users=User.query.filter(User.gender.in_(gender_filter))\
                        .filter(User.sexuality.in_(sexuality_filter))\
                        .filter(User.age>=age_min,User.age<=age_max)\
                        .filter(User.height>=height_min,User.height<=height_max)\
                        .filter(User.size.in_(size_filter))\
                        .filter(User.salary>=income_min,User.salary<=income_max)\
                        .filter(User.education.in_(education_filter))\
                        .filter(User.occupation.in_(occupation_filter))\
                        .filter(User.constellation.in_(constellation_filter))\
                        .filter(User.love_state.in_(love_state_filter)).all()
        searched=True
        selected_form=myclass.makeStruct(gender,sexuality,age_type,height_type,size,income_type,education,occupation,constellation,love_state)

    else:
        users=User.query.order_by(func.random()).all()
    count=len(users) 
    
    return render_template('main/search.html',users=users,searched=searched,count=count,selected_form=selected_form)

#个人主页
#个人信息
@main.route('/homepage_information/<user_id>', methods=['GET', 'POST'])
@login_required
def homepage_information(user_id):
    follow_relation = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    have_followed=(follow_relation is not None)        
    if request.method=='POST':
        if have_followed:
            db.session.delete(follow_relation)
            db.session.commit()
        else:
            follow_relation=Follow(follower_id=current_user.id, followed_id=user_id)
            db.session.add(follow_relation)
            db.session.commit()
        have_followed=not have_followed
    user = User.query.filter_by(id=user_id).first()
    return render_template('main/homepage_information.html',user_id=user_id,user=user,have_followed=have_followed)

#照片
@main.route('/homepage_photo/<user_id>')
def homepage_photo(user_id):
    user = User.query.filter_by(id=user_id).first()
    pictures=Pictures.query.filter_by(user_id=user_id).all()
    image_list=[]
    for picture in pictures:
        image_list.append('../static/' + picture.resource_url)
    image_num = len(image_list)
    return render_template('main/homepage_photo.html', user_id=user_id, user=user,image_list=image_list,image_num=image_num)

#粉丝
@main.route('/homepage_fans/<user_id>')
def homepage_fans(user_id):
    user = User.query.filter_by(id=user_id).first()
    fans = Follow.query.filter_by(followed_id=user_id).order_by(func.random()).all()
    fans_num = len(fans)
    prod_list = []
    prod = []
    is_odd=True
    for i in range(fans_num):
        if not i % 2:
            prod = [fans[i].follower]
        else:
            prod.append(fans[i].follower)
            prod_list.append(prod)

    if len(prod) % 2:
        prod_list.append(prod)
        is_odd = False

    return render_template('main/homepage_fans.html', user_id=user_id, user=user, is_odd=is_odd,prod_num=fans_num//2,prod_list=prod_list)

#关注者
@main.route('/homepage_notice/<user_id>')
def homepage_notice(user_id):
    user = User.query.filter_by(id=user_id).first()
    followed = Follow.query.filter_by(follower_id=user_id).order_by(func.random()).all()
    notice_num = len(followed)
    prod_list = []
    prod = []
    is_odd=True
    for i in range(notice_num):
        if not i % 2:
            prod = [followed[i].followed]
        else:
            prod.append(followed[i].followed)
            prod_list.append(prod)

    if len(prod) % 2:
        prod_list.append(prod)
        is_odd = False
    return render_template('main/homepage_notice.html', user_id=user_id, user=user,is_odd=is_odd,prod_num=notice_num//2,prod_list=prod_list)

#上传照片
@main.route('/upload_picture', methods=['GET', 'POST'])
@login_required
def upload_picture():
    if request.method == "POST":
        app = current_app._get_current_object()
        upload_files = request.files.getlist("upload_pictures")
        for file in upload_files:
            if file and allowed_file(file.filename):
                resource_url = 'user_pictures/' + str(file.filename)
                picture = Pictures(resource_url=resource_url, user_id=current_user.id)
                db.session.add(picture)
                db.session.commit()
                file.save(os.path.join(app.config['UPLODE_FOLDER'] + resource_url))
            else:
                flash('上传图片不符合类型！')
                return redirect(url_for('main.upload_picture'))
        flash('上传成功！')
        return redirect(url_for('main.homepage_photo', user_id=current_user.id))
    return render_template('main/upload_pictures.html')
        
