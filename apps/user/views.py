import os.path
from flask import Blueprint, render_template
from flask import url_for, g, current_app
from flask import jsonify, request
from flask import redirect, session
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ..exts import mail
from ..cfg import Config
from random import randint
from .models import User, Photo, AboutMe, MessageBoard
from ..article.models import Tag, Article

user_bp = Blueprint('user', __name__, url_prefix='/user')

allowed_path = [
    '/user/center.html', '/user/update', '/article/publish',
    '/article/photo', '/user/photos.html', '/article/photo_del',
    '/article/pub_cmt', '/user/aboutme', '/user/showme',
]

@user_bp.app_template_filter('jm')
def content_decode(content):
    return content.decode('utf-8')

@user_bp.before_app_request
def before_you_request():
    if request.path in allowed_path:
        uid = session.get('uid')
        if not uid:
            return render_template('user/login.html')
        else:
            user = User.query.get(uid)
            g.user = user


@user_bp.after_app_request
def after_you_request(response):
    return response


@user_bp.route('/', endpoint='index')
def index():
    uid = session.get('uid')
    page = request.args.get('page', 1, type=int)
    tags = Tag.query.all()
    pagination = Article.query.order_by(-Article.pub_time).paginate(page=page, per_page=3)
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, pagination=pagination, tags=tags)
    else:
        return render_template('user/index.html', pagination=pagination, tags=tags)


@user_bp.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            pwd = request.form.get('pwd')
            phone = request.form.get('phone')
            email = request.form.get('email')
            if password == pwd:
                user = User()
                user.username = username
                user.password = password
                user.phone = phone
                user.email = email
                user.yes()
                return redirect('/')
    return render_template('user/register.html')


@user_bp.route('/protocol')
def must_protocol():
    return render_template('user/bwtk.html')


@user_bp.route('/verify_phone')
def check_phone():
    phone_num = request.args.get('phoneNum')
    user = User.query.filter(User.phone == phone_num).all()
    if user:
        return jsonify({
            'status': 400,
            'msg': '此号码已被注册',
            'url': f'{request.url}',
        })
    else:
        return jsonify({
            'status': 200,
            'msg': '此号码可用',
            'url': f'{request.url}',
        })


@user_bp.route('/verify_email')
def check_email():
    email = request.args.get('email')
    user = User.query.filter(User.email == email).all()
    if user:
        return jsonify({
            'code': 400,
            'msg': '该邮箱已被注册',
            'url': f'{request.url}',
        })
    else:
        return jsonify({
            'code': 200,
            'msg': '该邮箱可用',
            'url': f'{request.url}',
        })


def save_captcha_to_session(email, captcha):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(captcha, salt='email-captcha')
    session[f'captcha_{email}'] = token


def verify_captcha_from_session(email, captcha):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = session.get(f'captcha_{email}')
    try:
        data = s.loads(token, salt='email-captcha', max_age=300)  # 假设验证码5分钟内有效
        return data == captcha
    except SignatureExpired:
        return False
    except BadSignature:
        return False


@user_bp.route('/email_capcha')
def send_email_capcha():
    email = request.args.get('email')
    random_num = randint(100000, 999999)
    save_captcha_to_session(email, random_num)

    try:
        msg = Message(
            subject="邮箱验证码",
            recipients=[email, ],
            html=f"""<table><tbody><tr height="40">
        <td style="padding-left:25px;padding-right:25px;font-size:18px;font-family:'微软雅黑','黑体',arial;">
            尊敬的 <a href="mailto:{email}" rel="noopener" target="_blank">{email}</a> ：
        </td></tr><tr height="15"><td></td></tr><tr height="30">
        <td style="padding-left:55px;padding-right:55px;font-family:'微软雅黑','黑体',arial;font-size:14px;line-height:20px;">
            您的账户<a href="{email}" rel="noopener" target="_blank">{email}</a> 
            正在获取身份验证, 验证码 {random_num} , 5 分钟内有效。
            </td></tr><tr height="20"><td></td></tr>
            <tr><td style="padding-left:55px;padding-right:55px;font-family:'微软雅黑','黑体',arial;font-size:14px;">
            此致<br>本站作者</td></tr><tr height="50"><td></td></tr></tbody></table>"""
        )
        mail.send(message=msg)
        return jsonify({
            'status': 200,
            'msg': '验证码发送成功'
        })
    except Exception as e:
        return jsonify({
            'status': 400,
            'msg': '验证码发送失败'
        })


@user_bp.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        if f == '1':
            username = request.form.get("username")
            password = request.form.get("password")
            users = User.query.filter(User.username == username).all()
            for user in users:
                if user.check_pwd(password):
                    session['uid'] = user.user_id
                    return redirect('/')
            else:
                return render_template('user/login.html', msg='用户名或密码有误')

        elif f == '2':
            email = request.form.get('email')
            random_num = request.form.get('yzm', type=int)
            user = User.query.filter(User.email == email).first()
            if user and verify_captcha_from_session(email, random_num):
                session['uid'] = user.user_id
                return redirect(url_for('user.index'))
            else:
                return render_template('user/login.html', msg='邮箱或验证码有误')
    return render_template('user/login.html')


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user_bp.route('/center.html')
def user_center():
    tags = Tag.query.all()
    photos = Photo.query.filter(Photo.user_id == g.user.user_id).all()
    return render_template('user/center.html', user=g.user, tags=tags, photos=photos)


image_suffix = ['jpg', 'gif', 'png', 'webp']


@user_bp.route('/update', methods=['GET', 'POST'])
def user_update():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        icon = request.files.get('icon')  # type:FileStorage
        avatar_path = None
        if icon:
            icon_name = icon.filename
            suffix = icon_name.split('.')[1]
            if suffix.lower() in icon_name:
                icon_name = secure_filename(icon_name)
                file_path = os.path.join(Config.ICON_DIR, icon_name)
                icon.save(file_path)
                avatar_path = os.path.join('uploads/icon/', icon_name)
            else:
                return render_template('user/center.html', user=g.user, msg='图片格式不对')
        else:
            avatar_path = g.user.avatar if g.user.avatar else None
        user = g.user
        user.username = username
        user.phone = phone
        user.email = email
        user.avatar = avatar_path
        user.yes()
        return redirect(url_for('user.user_center'))
    else:
        return render_template('user/center.html')


@user_bp.route('/photos.html')
def my_photo():
    page = request.args.get('page', 1, type=int)
    photos = Photo.query.paginate(page=page, per_page=1)
    return render_template('user/photos.html', photos=photos, user=g.user)


@user_bp.route('/aboutme', methods=['GET', 'POST'])
def about_me():
    content = request.form.get('about')
    print(content)
    # try:

    has_me = AboutMe.query.filter_by(user_id=g.user.user_id).first()
    if has_me.content:
        has_me.content = content
        has_me.yes()
    else:
        me = AboutMe()
        me.content = content
        me.user_id = g.user.user_id
        me.yes()
    # except Exception as e:
    #     return redirect(url_for('user.user_center'))
    # else:
    return render_template('user/aboutme.html', user=g.user)


@user_bp.route('/showme')
def show_about_me():
    return render_template('user/aboutme.html', user=g.user)


@user_bp.route('/board', methods=['GET', 'POST'])
def show_board():
    uid = session.get('uid', None)
    user = None
    if uid:
        user = User.query.get(uid)
    page = request.args.get('page', 1, type=int)
    boards = MessageBoard.query.order_by(-MessageBoard.bd_time).paginate(page=page, per_page=5)
    if request.method == 'POST':
        content = request.form.get('board')
        mb = MessageBoard()
        mb.content = content
        if uid:
            mb.user_id = uid
        mb.yes()
        return redirect(url_for('user.show_board'))
    return render_template('user/board.html', user=user, boards=boards)


@user_bp.route('/del_bd')
def delete_board():
    bid = request.args.get('bid', type=int)
    if bid:
        mb = MessageBoard.query.get(bid)
        mb.ono()
        return redirect(url_for('user.user_center'))
