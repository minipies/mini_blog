from flask import Blueprint, render_template
from flask import url_for, g, current_app
from flask import jsonify, request
from flask import redirect, session
from ..utils import upload_to_qiniu, delete_to_qiniu
from .models import Article, Tag, Comment
from ..user.models import Photo, User

article_bp = Blueprint('article', __name__, url_prefix='/article')


@article_bp.route('/publish', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        tag_id = request.form.get('tag')
        content = request.form.get('content')
        article = Article()
        article.title = title
        article.tag_id = tag_id
        article.content = content
        article.user_id = g.user.user_id
        article.yes()
        return redirect(url_for('user.index'))
    return redirect(url_for('user.user_center'))


@article_bp.route('/detail')
def article_detail():
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    user = None
    tags = Tag.query.all()
    uid = session.get('uid', None)
    if uid:
        user = User.query.get(uid)
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter(Comment.art_id == article_id).order_by(-Comment.cmt_time).paginate(page=page, per_page=5)

    return render_template('article/detail.html', article=article, tags=tags, user=user, comments=comments)


@article_bp.route('/love')
def article_love():  # 点赞
    aid = request.args.get('aid', type=int)
    t = request.args.get('t', type=int)
    article = Article.query.get(aid)  # type: Article

    if t == 1:
        article.love_num -= 1
    else:
        article.love_num += 1
    article.yes()
    return jsonify({
        'num': article.love_num
    })


@article_bp.route('/photo', methods=['GET', 'POST'])
def photo_album():
    if request.method == 'POST':
        pic = request.form.get('file')
        pic2 = request.files.get('photo')
        print(pic, type(pic))
        print(pic2, type(pic2))
        # ret, info = upload_to_qiniu(pic)
        # if info.status_code == 200:
        #     photo = Photo()
        #     photo.photo_name = ret['key']
        #     photo.user_id = g.user.user_id
        #     photo.yes()
        #     return redirect(url_for('user.user_center'))
        return 'post'
    # return 'get'


@article_bp.route('/photo_del')
def delete_photo():
    pid = request.args.get('pid', type=int)
    photo = Photo.query.get(pid)  # type:Photo
    info = delete_to_qiniu(photo.photo_name)
    if info.status_code == 200:
        photo.ono()
        return redirect(url_for('user.user_center'))
    else:
        return '失败了'


@article_bp.route('/pub_cmt', methods=['GET', 'POST'])
def publish_comment():
    if request.method == 'POST':
        aid = request.form.get('aid')
        cmt_ctt = request.form.get('comment')
        user_id = g.user.user_id
        cmt = Comment()
        cmt.comment = cmt_ctt
        cmt.user_id = user_id
        cmt.art_id = aid
        cmt.yes()
        return redirect(url_for('article.article_detail') + '?aid=' + aid)
    return redirect('/')


@article_bp.route('/tag')
def tag_search():
    tags = Tag.query.all()
    user = None
    uid = session.get('uid', None)
    if uid:
        user = User.query.get(uid)
    tid = request.args.get('tid', type=int)
    page = request.args.get('page', 1, type=int)

    articles = Article.query.filter(Article.tag_id == tid).paginate(page=page, per_page=3)

    return render_template('article/tag.html', **locals())


@article_bp.route('delete_cmt')
def delete_comment():
    cmt_id = request.args.get('cmt_id')
    if cmt_id:
        cmt = Comment.query.get(cmt_id)
        cmt.ono()
        return redirect(url_for('user.user_center'))
