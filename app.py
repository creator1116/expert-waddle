from flask import Flask, render_template, request, redirect, url_for, abort, jsonify, session, flash
from models import db, Collection, Link, CollectionLink
from slugify import slugify
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wiki.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# simple admin password (optional)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

db.init_app(app)

@app.route('/')
def index():
    cols = Collection.query.order_by(Collection.created_at.desc()).all()
    return render_template('index.html', collections=cols)

@app.route('/collections/new', methods=['GET','POST'])
def new_collection():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        visibility = request.form.get('visibility', 'public')
        slug = slugify(title) if title else None
        if not slug:
            flash('Title required', 'danger')
            return redirect(url_for('new_collection'))
        # ensure unique
        base = slug
        i = 1
        while Collection.query.filter_by(slug=slug).first():
            slug = f"{base}-{i}"
            i += 1
        col = Collection(title=title, description=description, visibility=visibility, slug=slug)
        db.session.add(col)
        db.session.commit()
        return redirect(url_for('view_collection', slug=col.slug))
    return render_template('new_collection.html')

@app.route('/collections/<slug>')
def view_collection(slug):
    col = Collection.query.filter_by(slug=slug).first_or_404()
    return render_template('collection.html', collection=col)

@app.route('/collections/<slug>/add_link', methods=['POST'])
def add_link(slug):
    col = Collection.query.filter_by(slug=slug).first_or_404()
    title = request.form.get('title')
    url = request.form.get('url')
    description = request.form.get('description')
    tags = request.form.get('tags')
    if not title or not url:
        flash('Title and URL required', 'danger')
        return redirect(url_for('view_collection', slug=slug))
    link = Link(title=title, url=url, description=description, tags=tags)
    db.session.add(link)
    db.session.commit()
    pos = len(col.links)
    cl = CollectionLink(collection_id=col.id, link_id=link.id, position=pos)
    db.session.add(cl)
    db.session.commit()
    return redirect(url_for('view_collection', slug=slug))

@app.route('/collections/<slug>/delete_link/<int:link_id>', methods=['POST'])
def delete_link(slug, link_id):
    col = Collection.query.filter_by(slug=slug).first_or_404()
    cl = CollectionLink.query.filter_by(collection_id=col.id, link_id=link_id).first_or_404()
    db.session.delete(cl)
    db.session.commit()
    return redirect(url_for('view_collection', slug=slug))

@app.route('/collections/<slug>/reorder', methods=['POST'])
def reorder(slug):
    col = Collection.query.filter_by(slug=slug).first_or_404()
    data = request.get_json() or {}
    order = data.get('order', [])
    # order is list of collection_link ids in desired order
    for idx, clid in enumerate(order):
        cl = CollectionLink.query.get(clid)
        if cl and cl.collection_id == col.id:
            cl.position = idx
    db.session.commit()
    return jsonify({'status': 'ok'})

@app.route('/api/collections')
def api_collections():
    cols = Collection.query.all()
    return jsonify([c.to_dict() for c in cols])

@app.route('/api/collections/<slug>')
def api_collection(slug):
    col = Collection.query.filter_by(slug=slug).first_or_404()
    return jsonify(col.to_dict())

# simple admin login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pw = request.form.get('password')
        if ADMIN_PASSWORD and pw != ADMIN_PASSWORD:
            flash('Bad password', 'danger')
            return redirect(url_for('login'))
        session['admin'] = True
        return redirect(url_for('index'))
    return render_template('login.html')

@app.context_processor
def inject_admin():
    return {'is_admin': session.get('admin', False)}

if __name__ == '__main__':
    app.run(debug=True)
