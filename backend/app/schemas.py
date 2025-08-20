from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Article, Author, Category, Tag, User, Quiz, Question, Answer, Page, MenuItem, StockQuote, SiteSettings

class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True
    
    id = fields.Str()

class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
    
    id = fields.Str()

class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True
    
    id = fields.Str()

class ArticleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        load_instance = True
    
    id = fields.Str()
    author = fields.Nested(AuthorSchema, dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)
    tags = fields.Nested(TagSchema, many=True, dump_only=True)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ['password_hash']
    
    id = fields.Str()

class AnswerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        load_instance = True
    
    id = fields.Str()
    question_id = fields.Str()

class QuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        load_instance = True
    
    id = fields.Str()
    quiz_id = fields.Str()
    answers = fields.Nested(AnswerSchema, many=True, dump_only=True)

class QuizSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Quiz
        load_instance = True
    
    id = fields.Str()
    questions = fields.Nested(QuestionSchema, many=True, dump_only=True)

class PageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Page
        load_instance = True
    
    id = fields.Str()

class MenuItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MenuItem
        load_instance = True
    
    id = fields.Str()

class StockQuoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StockQuote
        load_instance = True
    
    id = fields.Str()

class SiteSettingsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SiteSettings
        load_instance = True
    
    id = fields.Str()

# Schemas for different use cases
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
quiz_schema = QuizSchema()
quizzes_schema = QuizSchema(many=True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)
answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)
page_schema = PageSchema()
pages_schema = PageSchema(many=True)
menu_item_schema = MenuItemSchema()
menu_items_schema = MenuItemSchema(many=True)
stock_quote_schema = StockQuoteSchema()
stock_quotes_schema = StockQuoteSchema(many=True)
site_settings_schema = SiteSettingsSchema()
site_settings_list_schema = SiteSettingsSchema(many=True)
