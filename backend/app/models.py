from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    image_alt = db.Column(db.String(255))
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    
    # Foreign Keys
    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('authors.id'), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'))
    
    # Relationships
    author = db.relationship('Author', backref='articles')
    category = db.relationship('Category', backref='articles')
    tags = db.relationship('Tag', secondary='article_tags', backref='articles')

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Association table for many-to-many relationship between articles and tags
article_tags = db.Table('article_tags',
    db.Column('article_id', UUID(as_uuid=True), db.ForeignKey('articles.id'), primary_key=True),
    db.Column('tag_id', UUID(as_uuid=True), db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    quiz = db.relationship('Quiz', backref='questions')

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = db.Column(UUID(as_uuid=True), db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    answer_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    question = db.relationship('Question', backref='answers')

class Page(db.Model):
    __tablename__ = 'pages'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text)
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500))
    menu_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    menu_type = db.Column(db.String(50), default='header')  # header, footer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StockQuote(db.Model):
    __tablename__ = 'stock_quotes'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(255))
    current_price = db.Column(db.Numeric(10, 2))
    price_change = db.Column(db.Numeric(10, 2))
    percent_change = db.Column(db.Numeric(5, 2))
    volume = db.Column(db.BigInteger)
    market_cap = db.Column(db.BigInteger)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(50), default='text')  # text, json, boolean, number
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
