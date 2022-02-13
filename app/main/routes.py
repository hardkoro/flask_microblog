from datetime import datetime

from flask import (current_app, flash, g, jsonify, redirect, render_template,
                   request, url_for)
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from langdetect import LangDetectException, detect

from app import db
from app.main import bp
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm
from app.models import Post, User
from app.translate import translate


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''
        post = Post(
            body=form.post.data,
            author=current_user,
            language=language
        )
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    next_url, prev_url = None, None
    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)
    if posts.has_prev:
        prev_url = url_for('main.index', page=posts.prev_num)
    return render_template(
        'index.html', title=_('Home Page'), form=form, posts=posts.items,
        next_url=next_url, prev_url=prev_url
    )


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    next_url, prev_url = None, None
    if posts.has_next:
        next_url = url_for(
            'main.user', username=user.username, page=posts.next_num
        )
    if posts.has_prev:
        prev_url = url_for(
            'main.user', username=user.username, page=posts.prev_num
        )
    form = EmptyForm()
    return render_template(
        'user.html', user=user, posts=posts.items, form=form,
        next_url=next_url, prev_url=prev_url
    )


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved!'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        'edit_profile.html', title='Edit Profile', form=form
    )


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(_('User %(username)s not found!', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You are following %(username)s!', username=username))
        return redirect(url_for('main.user', username=username))
    return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(_('User %(username)s not found!', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself!', username=username))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You are not following %(username)s!'))
        return redirect(url_for('main.user', username=username))
    return redirect(url_for('main.index'))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    next_url, prev_url = None, None
    if posts.has_next:
        next_url = url_for('main.explore', page=posts.next_num)
    if posts.has_prev:
        prev_url = url_for('main.explore', page=posts.prev_num)
    return render_template(
        'index.html', title=_('Explore'), posts=posts.items,
        next_url=next_url, prev_url=prev_url
    )


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({
        'text': translate(
            request.form['text'],
            request.form['source_lang'],
            request.form['dest_lang']
        )
    })


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POSTS_PER_PAGE']
    posts, total = Post.search(
        g.search_form.q.data, page, per_page
    )
    next_url, prev_url = None, None
    if total > page * per_page:
        next_url = url_for(
            'main.search', q=g.search_form.q.data, page=page + 1
        )
    if page > 1:
        prev_url = url_for(
            'main.search', q=g.search_form.q.data, page=page - 1
        )
    return render_template(
        'search.html', title=_('Search'), posts=posts,
        next_url=next_url, prev_url=prev_url
    )
