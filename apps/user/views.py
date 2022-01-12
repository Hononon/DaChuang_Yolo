from flask import Blueprint, request, render_template, redirect, url_for, g
from apps.user.model import User
from exts import db
import os
from werkzeug.utils import secure_filename
from setting import Config
from detect_copy import myfunc
from detector import actions
from detector import imgaction
import tkinter

user_bp = Blueprint('user', __name__, url_prefix='/user')
required_login_list = ['/user/center', '/user/change', '/user/vupload', '/user/pupload', '/user/article',
                       '/user/messages',
                       '/user/wopaisc', '/user/jiqiusc', '/user/wopaicl', '/user/jiqiucl']

@user_bp.before_app_request
def before_request():
    if request.path in required_login_list:
        id = request.cookies.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)
            g.user = user


@user_bp.route('/')
def index():
    uid = request.cookies.get('uid', None)
    if uid:
        user = User.query.get(uid)
        return render_template('article/base.html', user=user)
    else:
        return render_template('article/base.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if password == repassword:
            # 与模型结合
            user = User()
            user.username = username
            user.password = password
            user.phone = phone
            user.email = email
            # 添加
            db.session.add(user)
            db.session.commit()
            return '用户注册成功'
        else:
            return '两次密码不一致'

    return render_template('user/register.html')


@user_bp.route('/messages', methods=['GET', 'POST'])
def messages():
    msg='?'
    if request.method == 'POST':
        file_path = os.path.join(Config.UPLOAD_VIDEO_DIR, '1.mp4')
        #t_copeimg=Thread(target=actions,args=(file_path,))
        actions(file_path)

    return render_template('user/messages.html', user=g.user, msg=msg)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = User.query.filter(User.username == username).all()
        for user in users:
            if user.password == password:
                response = redirect(url_for('user.index'))
                response.set_cookie('uid', str(user.id), max_age=1800)
                return response
        else:
            return render_template('user/login.html', msg='用户名或者密码错误')
    return render_template('user/login.html')


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    response = redirect(url_for('user.index'))
    response.delete_cookie('uid')
    return response


@user_bp.route('/center', methods=['GET', 'POST'])
def user_center():
    return render_template('user/user_center.html', user=g.user)


ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif']
ALLOWED_EXTENSIONS_VIDEO = ['mp4']


@user_bp.route('/change', methods=['GET', 'POST'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        icon = request.files.get('icon')
        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)
            file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
            icon.save(file_path)

        else:
            return render_template('user/user_center.html', user=g.user, msg='必须扩展名是jpg，png，gif')

        users = User.query.all()
        for user in users:
            if user.phone == phone:
                return render_template('user/user_center.html', user=g.user, msg='此手机已被注册')
            else:
                user = g.user
                user.username = username
                user.phone = phone
                user.email = email
                path = 'upload/icon/'
                user.icon = os.path.join(path, icon_name)

            db.session.commit()
            return redirect(url_for('user.user_center'))
    return render_template('user/user_center.html', user=g.user)

@user_bp.route('/pupload', methods=['GET', 'POST'])
def picture_upload():
    return render_template('user/uppicture.html', user=g.user)

@user_bp.route('/wopaisc', methods=['GET', 'POST'])
def wopaisc():
    if request.method == 'POST':
        picture_wopai = request.files.get('picture_wopai')
        picture_wopai_name = picture_wopai.filename
        print(picture_wopai_name)
        suffix = picture_wopai_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            picture_wopai_name = secure_filename(picture_wopai_name)
            file_path = os.path.join(Config.UPLOAD_PICTURE_WOPAI_DIR, picture_wopai_name)
            picture_wopai.save(file_path)
        else:
            return render_template('user/wopaisc.html', user=g.user, msg='必须扩展名是jpg，png，gif')
        user = g.user
        path = 'picture/wopai/'
        user.picture_wopai = os.path.join(path, picture_wopai_name)
        db.session.commit()
        return redirect(url_for('user.wopaisc'))
    return render_template('user/wopaisc.html', user=g.user)


@user_bp.route('/wopaicl', methods=['GET', 'POST'])
def wopaicl():
    if request.method == 'POST':
        user = g.user
        wopai_picture_name = 'static/'+user.picture_wopai
        imgaction(wopai_picture_name,'wopai')
        wopai_picture_name=wopai_picture_name.split('/')[-1]

        wopai_p_name = 'static/dealwith/wopaiing.jpg'
        A,B=myfunc(wopai_p_name)
        path = 'picture/new/'
        user.picture_wopai_new = os.path.join(path, 'wopaiing.jpg')
        db.session.commit()
        '''
        #弹窗处理
        window = tkinter.Tk()
        window.title('意见')
        window.geometry('300x200')
        label = tkinter.Label(window, text="你的意见")
        label.pack()
        window.mainloop()
        '''
        msg='动作为握拍,'
        if B > 0.8:
            msg1='动作较为标准，请继续练习'
        else:
            msg1='动作不标准，请纠正'
        msg1 = msg+msg1

        return render_template('user/wopaisc.html', user=g.user, msg1=msg1)
    return render_template('user/wopaisc.html', user=g.user, msg1=msg1) 


@user_bp.route('/jiqiusc', methods=['GET', 'POST'])
def jiqiusc():
    if request.method == 'POST':
        picture_jiqiu = request.files.get('picture_jiqiu')
        picture_jiqiu_name = picture_jiqiu.filename
        print(picture_jiqiu_name)
        suffix = picture_jiqiu_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            picture_jiqiu_name = secure_filename(picture_jiqiu_name)
            file_path = os.path.join(Config.UPLOAD_PICTURE_JIQIU_DIR, picture_jiqiu_name)
            picture_jiqiu.save(file_path)
        else:
            return render_template('user/jiqiusc.html', user=g.user, msg='必须扩展名是jpg，png，gif')
        user = g.user
        path = 'picture/jiqiu/'
        user.picture_jiqiu = os.path.join(path, picture_jiqiu_name)
        db.session.commit()
        return redirect(url_for('user.jiqiusc'))
    return render_template('user/jiqiusc.html', user=g.user)


@user_bp.route('/jiqiucl', methods=['GET', 'POST'])
def jiqiucl():
    if request.method == 'POST':
        user = g.user
        jiqiu_picture_name = 'static/'+user.picture_jiqiu
        imgaction(jiqiu_picture_name,'jiqiu')
        jiqiu_picture_name=jiqiu_picture_name.split('/')[-1]

        jiqiu_p_name = 'static/dealwith/jiqiuing.jpg'
        A,B=myfunc(jiqiu_p_name)
        path = 'picture/new/'
        user.picture_jiqiu_new = os.path.join(path, 'jiqiuing.jpg')
        db.session.commit()
        '''
        #弹窗处理
        window = tkinter.Tk()
        window.title('意见')
        window.geometry('300x200')
        label = tkinter.Label(window, text="你的意见")
        label.pack()
        window.mainloop()
        '''
        msg='动作为击球,'
        if B > 0.8:
            msg1='动作较为标准，请继续练习'
        else:
            msg1='动作不标准，请纠正'
        msg1 = msg+msg1
        return render_template('user/jiqiusc.html', user=g.user, msg1=msg1)
    return render_template('user/jiqiusc.html', user=g.user, msg1=msg1)  

@user_bp.route('/vupload', methods=['GET', 'POST'])
def video_upload():
    if request.method == 'POST':
        video = request.files.get('video')
        video_name = video.filename
        suffix = video_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS_VIDEO:
            video_name = secure_filename(video_name)
            file_path = os.path.join(Config.UPLOAD_VIDEO_DIR, video_name)
            video.save(file_path)
            # action(file_path)

        else:
            return render_template('user/upvideo.html', user=g.user, msg='必须扩展名是mp4')

        user = g.user
        path = 'upload/video/'
        user.video = os.path.join(path, video_name)
        print('1=' + user.video)
        db.session.commit()
        return redirect(url_for('user.video_upload'))
    return render_template('user/upvideo.html', user=g.user)