from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Article, Author, Category, Tag, User

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
