from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
import json
from config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50), default="user") # admin, user
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    profile_picture = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    wp_accounts = relationship("WPAccount", back_populates="user")
    generated_articles = relationship("GeneratedArticle", back_populates="user")


class WPAccount(Base):
    __tablename__ = "wp_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    site_name = Column(String(100), nullable=False)
    wp_url = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    app_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="wp_accounts")
    articles = relationship("GeneratedArticle", back_populates="wp_account")
    analytics = relationship("ArticleAnalytics", back_populates="wp_account")


class GeneratedArticle(Base):
    __tablename__ = "generated_articles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    wp_account_id = Column(Integer, ForeignKey("wp_accounts.id"), nullable=True)
    category = Column(String(50), nullable=False)
    topic_input = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    content_body = Column(Text, nullable=False)
    seo_title = Column(Text, nullable=False)
    slug = Column(String(200), nullable=False)
    meta_description = Column(Text, nullable=False)
    keyphrase = Column(String(100), nullable=False)
    
    # Store JSON array as Text
    keywords_list = Column(Text, nullable=False) # JSON encoded list
    featured_image_url = Column(Text, nullable=True)
    wikipedia_outlinks = Column(Text, nullable=True) # JSON encoded list
    
    wp_post_id = Column(Integer, nullable=True)
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="generated_articles")
    wp_account = relationship("WPAccount", back_populates="articles")

    @property
    def get_keywords(self):
        return json.loads(self.keywords_list) if self.keywords_list else []

    @property
    def get_outlinks(self):
        return json.loads(self.wikipedia_outlinks) if self.wikipedia_outlinks else []


class ArticleAnalytics(Base):
    __tablename__ = "article_analytics"

    id = Column(Integer, primary_key=True, index=True)
    wp_account_id = Column(Integer, ForeignKey("wp_accounts.id"))
    post_id = Column(Integer, nullable=False) # ID of post in WP 
    pageviews = Column(Integer, default=0)
    seo_score = Column(Integer, default=0)
    readability_score = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    wp_account = relationship("WPAccount", back_populates="analytics")
