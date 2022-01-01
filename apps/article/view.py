from flask import Blueprint, request, render_template, g
from apps.user.model import User
from apps.article.models import Article
from exts import db

article_bp = Blueprint('article', __name__)
###################################
required_login_list = ['/article/upload', '/article/publish', '/article/all']
#################################
#################################
@article_bp.before_app_request
def before_request():
    if request.path in required_login_list:
        id = request.cookies.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)
            g.user = user
##############################
##############################
@article_bp.route('/upload', methods=['GET', 'POST'])
def article_upload():
    return render_template('article/add_article.html', user=123)
##############################

@article_bp.route('/publish', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        uid = request.form.get('uid')
        article = Article()
        article.title = title
        article.content = content
        article.user_id = uid
        db.session.add(article)
        db.session.commit()
        return '添加成功！'
    else:
        users = User.query.filter(User.isdelete == False).all()
    return render_template('article/add_article.html', users=users)


@article_bp.route('/all', methods=['GET', 'POST'])
def all_article():
    return render_template('article/all.html')

# articles=Article.query.all()
