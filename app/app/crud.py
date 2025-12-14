# ============================================
# crud.py
# データベース操作（CRUD）を担当するモジュール
#
# 本ファイルはレイヤードアーキテクチャにおける
# 「データアクセス層（Repository / CRUD 層）」に該当し、
# FastAPI のエンドポイントから直接 ORM 操作を行わず、
# DB操作をこの層に集約することを目的としている。
# ============================================

from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
import uuid

# =========================
# Author（著者）関連の CRUD
# =========================

"""
 著者を新規作成する処理

 :param db: DBセッション
 :param author_in: リクエストで受け取った著者作成用データ
 :return: 作成された著者モデル
"""
def create_author(db: Session, author_in: schemas.AuthorCreate):
    # Authorモデルを作成
    author = models.Author(name=author_in.name)

    # DBに追加
    db.add(author)
    db.commit()

    # DBに保存された最新状態を取得（idなど）
    db.refresh(author)
    return author


"""
 著者IDをもとに著者を1件取得する

 :param db: DBセッション
 :param author_id: 著者のUUID
 :return: Authorモデル or None
"""
def get_author(db: Session, author_id: uuid.UUID):
    # 著者IDで著者を取得
    return db.query(models.Author).filter(models.Author.id == author_id).first()


"""
 著者を削除する処理

 :param db: DBセッション
 :param author_id: 削除対象の著者UUID
 :return: 削除したAuthor or None
"""
def delete_author(db: Session, author_id: uuid.UUID):
    # 著者IDをもとに、対象の著者を取得
    author = get_author(db, author_id)

    # 著者が存在しない場合は削除できないため None を返す
    if not author:
        return None

    # DBから削除
    db.delete(author)
    db.commit()
    return author


# =========================
# Book（書籍）関連の CRUD
# =========================

"""
 書籍を新規作成する処理
 著者が存在しない場合はエラーとする

 :param db: DBセッション
 :param book_in: 書籍作成用リクエストデータ
 :return: 作成されたBookモデル
"""
def create_book(db: Session, book_in: schemas.BookCreate):
    # 著者の存在チェック
    author = get_author(db, book_in.author_id)
    if not author:
        # 著者が存在しない場合は400エラー
        raise HTTPException(status_code=400, detail="author not found")

    # Bookモデルを作成
    book = models.Book(title=book_in.title, author_id=book_in.author_id)

    # DBに追加
    db.add(book)
    db.commit()

    # DBに保存された最新状態を取得（idなど）
    db.refresh(book)
    return book


"""
 書籍一覧を取得する処理

 :param db: DBセッション
 :param skip: 取得開始位置（ページング用）
 :param limit: 取得件数
 :return: Bookモデルのリスト
"""
def list_books(db: Session, skip: int = 0, limit: int = 100):
    # 書籍を取得
    return db.query(models.Book).offset(skip).limit(limit).all()


"""
 書籍IDをもとに書籍を1件取得する

 :param db: DBセッション
 :param book_id: 書籍のUUID
 :return: Bookモデル or None
"""
def get_book(db: Session, book_id: uuid.UUID):
    # 書籍IDで書籍を取得
    return db.query(models.Book).filter(models.Book.id == book_id).first()


"""
 書籍を削除する処理

 :param db: DBセッション
 :param book_id: 削除対象の書籍UUID
 :return: 削除したBook or None
"""
def delete_book(db: Session, book_id: uuid.UUID):
    # 書籍IDをもとに、対象の書籍を取得
    book = get_book(db, book_id)

    # 書籍が存在しない場合は削除できないため None を返す
    if not book:
        return None

    # DBから削除
    db.delete(book)
    db.commit()
    return book
