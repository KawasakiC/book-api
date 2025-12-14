# Book API （FastAPI + PostgreSQL + Docker）


本プロジェクトは、FastAPI を使用した書籍管理 API です。  

著者（Author）および書籍（Book）の登録・取得・削除を行うことができます。  

データベースには PostgreSQL、マイグレーションには Alembic を使用しています。


---


## 使用技術


| 項目 | 内容 |

|------|------|

| 言語 | Python 3.12 |

| フレームワーク | FastAPI |

| データベース | PostgreSQL |

| ORM | SQLAlchemy |

| マイグレーション | Alembic |

| コンテナ | Docker / docker-compose |

| API ドキュメント | Swagger UI（/docs） |


---


## ディレクトリ構成



book-api/

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── alembic/

│ ├── versions/ # マイグレーションファイル

│ └── env.py

├── alembic.ini

└── app/

├── main.py # FastAPI エントリポイント

├── models.py # SQLAlchemy Models

├── schemas.py # Pydantic Schemas

├── crud.py # DB 操作用関数

└── database.py # DB セッション管理


---


## セットアップ手順

### 1. Docker コンテナの起動
docker compose up --build

起動後、FastAPI は以下の URL で確認できます
http://localhost:8000/docs

### 2. データベースマイグレーションの実行（初回のみ）
別ターミナルで API コンテナに入り、Alembic を実行します。
docker exec -it bookapi-api sh
alembic upgrade head

これにより、以下のテーブルが作成されます。
・authors
・books


---


## 注意点

### 1.
Windows PowerShell の curl は挙動が異なるため、cmd.exe または curl.exe の使用を推奨します。

### 2.
DB スキーマの変更は Base.metadata.create_all() ではなく Alembic を使用してください。


---


## APIエンドポイント


| 分類 | メソッド | エンドポイント | 説明 |

|------|------|------|------|

| 著者 | POST | /authors | 新しい著者を登録します。|

| 著者 | GET | /authors | 登録されている著者の一覧を取得します。 | ※機能要件にはありませんでしたが、動作確認を円滑に行えるよう、機能追加いたしました。

| 著者 | DELETE | /authors/{authors_id} | 指定されたIDの著者を削除します。 | ※機能要件にはありませんでしたが、動作確認を円滑に行えるよう、機能追加いたしました。

| 書籍 | POST | /books | 新しい書籍を登録します。登録時には、既存の著者IDを指定する必要があります。 |

| 書籍 | GET | /books | 登録されている書籍の一覧を取得します。レスポンスには、各書籍に対応する著者名も含みます。 |

| 書籍 | GET | /books/{book_id} | 指定されたIDの書籍情報を取得します。レスポンスには、書籍に対応する著者名も含みます。 |

| 書籍 | DELETE | /books/{book_id} | 指定されたIDの書籍を削除します。 |


---


## 実行例

### 1. 著者登録
curl -X POST "http://localhost:8000/authors" -H "Content-Type: application/json" -d "{ \"name\": \"太宰治\" }"

### 2, 著者一覧取得　※機能要件にはありません。
curl -X GET "http://localhost:8000/authors"

### 3. 著者削除　※機能要件にはありません。
curl -X DELETE "http://localhost:8000/authors/<著者ID>"

### 4. 書籍登録
curl -X POST "http://localhost:8000/books" -H "Content-Type: application/json; charset=utf-8" -d "{ \"title\": \"走れメロス\", \"author_id\": \"<著者ID>\" }"

### 5. 書籍一覧取得
curl -X GET "http://localhost:8000/books"

### 6. 書籍一覧取得（ID指定）
curl -X GET "http://localhost:8000/books/<書籍ID>"

### 7. 書籍削除
curl -X DELETE "http://localhost:8000/books/<書籍ID>"


---


## アーキテクチャ等で意識した点
本プロジェクトでは、保守性・拡張性・実務での利用を意識したアーキテクチャ設計を行っています。

### 1. レイヤードアーキテクチャの採用
・API層（main.py）：ルーティングとリクエスト／レスポンス定義に専念
・CRUD層（crud.py）：DB操作ロジックを集約
・Model層（models.py）：SQLAlchemy によるテーブル定義
・Schema層（schemas.py）：Pydantic による入出力バリデーション
・DB接続管理（database.py）：SQLAlchemyのEngine・SessionLocal・Baseを集約し、
　FastAPIのDependsを利用してリクエスト単位で安全に DBセッションを管理しています。
　これにより各レイヤーが DB接続設定に直接依存しない構成としています。
責務を明確に分離することで、機能追加や修正時の影響範囲を限定できる構成としています。

### 2. ORM + マイグレーションによるDB管理
・ORMにSQLAlchemyを使用し、PythonコードベースでDBを操作
・テーブル作成・変更は Alembic によるマイグレーション管理を採用
・Base.metadata.create_all() を使用せず、本番運用を想定した構成
これにより、DBスキーマの変更履歴を安全に管理できるようにしています。


---


## 作成者
川崎　せりか


---