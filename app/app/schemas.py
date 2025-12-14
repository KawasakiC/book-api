# ======================
# schemas.py
# リクエスト / レスポンス用スキーマ定義ファイル
#
# Pydantic を使用して、APIで受け取るデータ形式や
# 返却するレスポンス形式を定義する。
# ======================

from pydantic import BaseModel, Field
from typing import Optional
import uuid


# ======================
# Author スキーマ
# ======================

"""
著者（Author）に関するリクエスト・レスポンス定義

・作成時に必要な項目
・レスポンスとして返却する項目
"""
class AuthorCreate(BaseModel):
    # 著者名（必須・最大50文字）
    name: str = Field(..., max_length=50)


class AuthorOut(BaseModel):
    # 著者ID
    id: uuid.UUID

    # 著者名
    name: str

    class Config:
        # ORMモデル（SQLAlchemy）からの変換を許可
        orm_mode = True


# ======================
# Book スキーマ
# ======================

"""
本（Book）に関するリクエスト・レスポンス定義

・作成時は著者IDを指定
・レスポンスでは著者情報をネストして返却
"""
class BookCreate(BaseModel):
    # 本のタイトル（必須・最大100文字）
    title: str = Field(..., max_length=100)

    # 著者ID（UUID）
    author_id: uuid.UUID


class BookOut(BaseModel):
    # 本ID
    id: uuid.UUID

    # 本のタイトル
    title: str

    # 著者情報（AuthorOut をネスト）
    author: AuthorOut

    class Config:
        # ORMモデル（SQLAlchemy）からの変換を許可
        orm_mode = True
