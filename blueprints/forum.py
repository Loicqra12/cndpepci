from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import ForumCategory, ForumTopic, ForumPost
from datetime import datetime

bp = Blueprint('forum', __name__)

@bp.route('/forum')
def index():
    categories = ForumCategory.query.order_by(ForumCategory.position).all()
    return render_template('forum/index.html', categories=categories)

@bp.route('/forum/category/<int:id>')
def category(id):
    category = ForumCategory.query.get_or_404(id)
    topics = category.topics.order_by(ForumTopic.is_pinned.desc(), ForumTopic.updated_at.desc()).all()
    return render_template('forum/category.html', category=category, topics=topics)

@bp.route('/forum/topic/<int:id>')
def topic(id):
    topic = ForumTopic.query.get_or_404(id)
    # Incrémenter le compteur de vues
    topic.views += 1
    db.session.commit()
    posts = topic.posts.order_by(ForumPost.created_at).all()
    return render_template('forum/topic.html', topic=topic, posts=posts)

@bp.route('/forum/topic/new/<int:category_id>', methods=['GET', 'POST'])
@login_required
def new_topic(category_id):
    category = ForumCategory.query.get_or_404(category_id)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if title and content:
            topic = ForumTopic(
                title=title,
                content=content,
                category=category,
                author=current_user
            )
            db.session.add(topic)
            db.session.commit()
            flash('Votre sujet a été créé avec succès.', 'success')
            return redirect(url_for('forum.topic', id=topic.id))
            
    return render_template('forum/new_topic.html', category=category)

@bp.route('/forum/post/new/<int:topic_id>', methods=['POST'])
@login_required
def new_post(topic_id):
    topic = ForumTopic.query.get_or_404(topic_id)
    
    if topic.is_locked and not current_user.is_admin:
        flash('Ce sujet est verrouillé.', 'error')
        return redirect(url_for('forum.topic', id=topic_id))
        
    content = request.form.get('content')
    
    if content:
        post = ForumPost(
            content=content,
            topic=topic,
            author=current_user
        )
        db.session.add(post)
        topic.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Votre réponse a été publiée.', 'success')
        
    return redirect(url_for('forum.topic', id=topic_id))

@bp.route('/forum/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = ForumPost.query.get_or_404(id)
    
    if post.author != current_user and not current_user.is_admin:
        flash('Vous n\'êtes pas autorisé à modifier ce message.', 'error')
        return redirect(url_for('forum.topic', id=post.topic_id))
        
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            post.content = content
            post.is_edited = True
            post.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Votre message a été modifié.', 'success')
            return redirect(url_for('forum.topic', id=post.topic_id))
            
    return render_template('forum/edit_post.html', post=post)

@bp.route('/forum/topic/lock/<int:id>')
@login_required
def lock_topic(id):
    topic = ForumTopic.query.get_or_404(id)
    if current_user.is_admin:
        topic.is_locked = not topic.is_locked
        db.session.commit()
        status = 'verrouillé' if topic.is_locked else 'déverrouillé'
        flash(f'Le sujet a été {status}.', 'success')
    return redirect(url_for('forum.topic', id=id))

@bp.route('/forum/topic/pin/<int:id>')
@login_required
def pin_topic(id):
    topic = ForumTopic.query.get_or_404(id)
    if current_user.is_admin:
        topic.is_pinned = not topic.is_pinned
        db.session.commit()
        status = 'épinglé' if topic.is_pinned else 'désépinglé'
        flash(f'Le sujet a été {status}.', 'success')
    return redirect(url_for('forum.topic', id=id))

@bp.route('/forum/admin/categories')
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('Accès refusé.', 'error')
        return redirect(url_for('forum.index'))
        
    categories = ForumCategory.query.order_by(ForumCategory.position).all()
    return render_template('forum/admin_categories.html', categories=categories)
