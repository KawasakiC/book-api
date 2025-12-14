# ======================
# models.py
# ORMモデル定義ファイル
#
# SQLAlchemy を用いてデータベースのテーブル構造を
# Pythonクラスとして定義する。
# 本ファイルはレイヤードアーキテクチャにおける
# 「ドメイン層 / モデル層」に該当する。
# ======================

import uuid
from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base


# ======================
# Author モデル
# ======================

"""
著者（Author）テーブルに対応する ORM モデル

・著者ID（UUID）
・著者名
・著者が持つ本（Book）とのリレーションを定義
"""
class Author(Base):
    # テーブル名を明示的に指定
    __tablename__ = "authors"

    # 著者ID（UUIDを主キーとして使用）
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 著者名（検索を想定して index を付与）
    name = Column(String(50), nullable=False, index=True)

    # 著者が持つ本一覧（1対多のリレーション）
    # cascade により著者削除時に紐づく本も削除される
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


# ======================
# Book モデル
# ======================

"""
本（Book）テーブルに対応する ORM モデル

・本ID（UUID）
・タイトル
・著者ID（外部キー）
・Author モデルとのリレーションを定義
"""
class Book(Base):
    __tablename__ = "books"  # テーブル名を明示的に指定

    # 本ID（UUIDを主キーとして使用）
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 本のタイトル（検索を想定して index を付与）
    title = Column(String(100), nullable=False, index=True)

    # 著者ID（authors テーブルの id を参照する外部キー）
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.id"), nullable=False, index=True)

    # 著者情報（多対1のリレーション）
    author = relationship("Author", back_populates="books")


# ======================
# インデックス定義
# ======================

"""
検索性能向上のための追加インデックス定義

author_id を使った検索（著者ごとの本一覧）を高速化する
"""
# Book.author_id に対して明示的にインデックスを作成
Index("ix_books_author_id", Book.author_id)
