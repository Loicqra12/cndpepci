from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import ForumTopic, ForumPost, ForumCategory
from extensions import db

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/')
def index():
    categories = ForumCategory.query.all()
    return render_template('forum/index.html', categories=categories)

@forum_bp.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = ForumTopic.query.get_or_404(topic_id)
    return render_template('forum/topic.html', topic=topic)
