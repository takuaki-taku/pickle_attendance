# イベント管理アプリケーション

## 概要

このアプリケーションは、イベントの作成、管理、参加者の追跡を行うためのウェブベースのツールです。Flask、SQLAlchemy、FullCalendarを使用して構築されており、ユーザー認証、イベントのCRUD操作、参加者管理機能を提供します。

## 機能

- ユーザー認証（登録、ログイン、ログアウト）
- イベントの作成、読み取り、更新、削除（CRUD）
- カレンダーベースのイベント表示
- イベントへの参加登録と参加状況の管理
- 管理者ユーザーによるイベント管理

## セットアップ

1. リポジトリをクローンします：

   ```
   git clone https://github.com/takuaki-taku/pickle_attendance.git
   ```

2. 仮想環境を作成し、アクティベートします：

   ```
   python -m venv venv
   source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   ```

3. 必要なパッケージをインストールします：

   ```
   pip install -r requirements.txt
   ```

4. 環境変数を設定します：

   ```
   export SECRET_KEY=your_secret_key_here
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

   Windowsの場合：

   ```
   set SECRET_KEY=your_secret_key_here
   set FLASK_APP=app.py
   set FLASK_ENV=development
   ```

5. データベースを初期化します：

   ```
   flask db upgrade
   ```

6. アプリケーションを実行します：

   ```
   flask run
   ```

   アプリケーションは http://localhost:5000 で実行されます。

## 使用方法

1. ブラウザで http://localhost:5000 にアクセスします。
2. 新規ユーザーの場合は登録を行い、既存ユーザーの場合はログインします。
3. ホームページでカレンダーを表示し、イベントを閲覧します。
4. 管理者ユーザーは新しいイベントを作成、編集、削除できます。
5. 一般ユーザーはイベントの詳細を確認し、参加状況を更新できます。

## 管理者アカウントの作成

初期の管理者アカウントを作成するには、以下の手順を実行します：

1. Pythonインタラクティブシェルを開きます：

   ```
   python
   ```

2. 以下のコードを実行して管理者ユーザーを作成します：

   ```python
   from app import app, db, User
   with app.app_context():
       admin = User(username='admin', is_admin=True)
       admin.set_password('your_admin_password')
       db.session.add(admin)
       db.session.commit()
   ```

   [仮でアカウントが登録されています。]
   管理者アカウント
   ユーザー名　東
   パスワード　tennispickle

   一般ユーザー
   ユーザー名　sample
   パスワード　sample


3. これで、ユーザー名 'admin' とパスワード 'your_admin_password' で管理者としてログインできます。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細については、[LICENSE](LICENSE) ファイルを参照してください。

## 貢献

プロジェクトへの貢献を歓迎します。問題を報告したり、プルリクエストを送信したりする場合は、GitHub リポジトリの Issues セクションをご利用ください。

## サポート

質問やサポートが必要な場合は、GitHub の Issues セクションに投稿するか、[tatennisku@gmail.com] までメールでお問い合わせください。