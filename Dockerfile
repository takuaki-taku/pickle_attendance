FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txt をコピー
COPY requirements.txt ./

# パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 環境変数を設定
ENV SECRET_KEY=your_secret_key  
#実際の秘密鍵に置き換えてください
ENV CYTHON_INSTALL=true

# gunicorn を使用してアプリケーションを実行
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]