# ============================================
# database.py
# データベース接続およびセッション管理を担当するモジュール
#
# 本ファイルはレイヤードアーキテクチャにおける
# 「インフラストラクチャ層（Database）」に該当し、
# SQLAlchemy を用いて以下を提供する。
#  - DB接続エンジンの生成
#  - DBセッションのファクトリ
#  - ORMモデル用のBaseクラス
# ============================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

"""
 データベース接続URLの定義
 環境変数 DATABASE_URL が存在する場合はそれを使用し、
 未設定の場合は Docker Compose 用のデフォルトURLを使用する

 例:
 postgresql://ユーザー名:パスワード@ホスト:ポート/DB名
"""
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/appdb")

"""
 SQLAlchemy エンジンの生成
 エンジンは DB との接続情報を保持し、
 実際のコネクション管理を内部で行う
"""
engine = create_engine(DATABASE_URL)

"""
 セッションファクトリの作成

 autocommit=False:
   明示的に commit() を呼ばない限り DB に反映されない

 autoflush=False:
   クエリ実行時に自動で flush しない（意図しない更新を防ぐ）

 bind=engine:
   上で作成したエンジンを使用する
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
 ORMモデルの基底クラス

 models.py で定義するすべての ORM モデルは
 この Base を継承することで、
 SQLAlchemy によるテーブル管理の対象となる
"""
Base = declarative_base()
