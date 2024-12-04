from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import ForumCategory, ForumTopic, ForumPost
from forms import ForumTopicForm, ForumPostForm, ForumCategoryForm

bp = Blueprint('forum', __name__)

@bp.route('/forum')
def index():
    categories = ForumCategory.query.order_by(ForumCategory.order).all()
    return render_template('forum/index.html', categories=categories)

@bp.route('/forum/category/<int:id>')
def category(id):
    category = ForumCategory.query.get_or_404(id)
    topics = category.topics.order_by(ForumTopic.is_pinned.desc(), ForumTopic.updated_at.desc()).all()
    return render_template('forum/category.html', category=category, topics=topics)

@bp.route('/forum/topic/new/<int:category_id>', methods=['GET', 'POST'])
@login_required
def new_topic(category_id):
    category = ForumCategory.query.get_or_404(category_id)
    form = ForumTopicForm()
    if form.validate_on_submit():
        topic = ForumTopic(title=form.title.data, 
                          content=form.content.data,
                          category=category,
                          author=current_user)
        db.session.add(topic)
        db.session.commit()
        flash('Votre sujet a été créé.', 'success')
        return redirect(url_for('forum.topic', id=topic.id))
    return render_template('forum/new_topic.html', form=form, category=category)

@bp.route('/forum/topic/<int:id>', methods=['GET', 'POST'])
def topic(id):
    topic = ForumTopic.query.get_or_404(id)
    form = ForumPostForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour répondre.', 'error')
            return redirect(url_for('auth.login'))
        post = ForumPost(content=form.content.data,
                        topic=topic,
                        author=current_user)
        db.session.add(post)
        topic.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Votre réponse a été publiée.', 'success')
        return redirect(url_for('forum.topic', id=topic.id))
    topic.views += 1
    db.session.commit()
    posts = topic.posts.order_by(ForumPost.created_at).all()
    return render_template('forum/topic.html', topic=topic, posts=posts, form=form)

@bp.route('/forum/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = ForumPost.query.get_or_404(id)
    if post.author != current_user and not current_user.is_admin:
        flash('Vous n\'avez pas la permission de modifier ce message.', 'error')
        return redirect(url_for('forum.topic', id=post.topic_id))
    form = ForumPostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        post.is_edited = True
        db.session.commit()
        flash('Votre message a été modifié.', 'success')
        return redirect(url_for('forum.topic', id=post.topic_id))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('forum/edit_post.html', form=form, post=post)

# Routes d'administration du forum
@bp.route('/forum/admin/categories', methods=['GET', 'POST'])
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('Accès refusé.', 'error')
        return redirect(url_for('forum.index'))
    form = ForumCategoryForm()
    if form.validate_on_submit():
        category = ForumCategory(name=form.name.data,
                               description=form.description.data,
                               order=form.order.data)
        db.session.add(category)
        db.session.commit()
        flash('La catégorie a été créée.', 'success')
        return redirect(url_for('forum.admin_categories'))
    categories = ForumCategory.query.order_by(ForumCategory.order).all()
    return render_template('forum/admin_categories.html', categories=categories, form=form)
