# ============================================
# main.py
# FastAPI アプリケーションのエントリーポイント
#
# 本ファイルはレイヤードアーキテクチャにおける
# 「プレゼンテーション層（API層）」を担当する。
#
# DBの直接操作は行わず、責務を分離している。
# ============================================

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, schemas
from .database import SessionLocal, engine, Base
import os
import uuid

"""
 FastAPI アプリケーションの生成
"""
app = FastAPI(title="Book API")

"""
 DBセッションを取得する Dependency

 各リクエストごとに DB セッションを生成し、
 処理終了後に必ず close する
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
# 著者（Author）API
# ======================

"""
 著者を新規作成する
"""
@app.post("/authors", response_model=schemas.AuthorOut, status_code=201)
def create_author(author_in: schemas.AuthorCreate, db: Session = Depends(get_db)):
    # CRUD層に処理を委譲
    return crud.create_author(db, author_in)


"""
 著者一覧を取得する
"""
@app.get("/authors", response_model=list[schemas.AuthorOut])
def read_authors(db: Session = Depends(get_db)):
    # ORMオブジェクトをそのまま返却（Pydanticで変換）
    return db.query(models.Author).all()


"""
 著者を削除する
"""
@app.delete("/authors/{author_id}", status_code=204)
def delete_author(author_id: str, db: Session = Depends(get_db)):
    # UUID形式チェック
    try:
        aid = uuid.UUID(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid author id")

    # CRUD層で削除処理
    deleted = crud.delete_author(db, aid)
    if not deleted:
        raise HTTPException(status_code=404, detail="author not found")

    # 204 No Content のため戻り値なし
    return None


# ======================
# 書籍（Book）API
# ======================

"""
 書籍を新規作成する
"""
@app.post("/books", response_model=schemas.BookOut, status_code=201)
def create_book(book_in: schemas.BookCreate, db: Session = Depends(get_db)):
    # 本を作成
    book = crud.create_book(db, book_in)

    # author 情報を含めた状態で返却するため再取得
    return db.query(models.Book).filter(models.Book.id == book.id).first()


"""
 書籍一覧を取得する
"""
@app.get("/books", response_model=list[schemas.BookOut])
def read_books(db: Session = Depends(get_db)):
    # CRUD層で一覧取得
    return crud.list_books(db)


"""
 書籍をID指定で取得する
"""
@app.get("/books/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: str, db: Session = Depends(get_db)):
    # UUID形式チェック
    try:
        bid = uuid.UUID(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid book id")

    # 書籍の取得
    book = crud.get_book(db, bid)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")

    return book


"""
 書籍を削除する
"""
@app.delete("/books/{book_id}", status_code=204)
def remove_book(book_id: str, db: Session = Depends(get_db)):
    # UUID形式チェック
    try:
        bid = uuid.UUID(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid book id")

    # CRUD層で削除
    deleted = crud.delete_book(db, bid)
    if not deleted:
        raise HTTPException(status_code=404, detail="book not found")

    return None
