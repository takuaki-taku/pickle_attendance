# Gunicorn configuration file
import multiprocessing

# 同時実行ワーカー数
workers = multiprocessing.cpu_count() * 2 + 1

# ワーカークラスの指定
worker_class = "sync"

# バインドするアドレスとポート
bind = "0.0.0.0:8000"

# プロセスの名前
proc_name = "event_manager"

# デーモン化の設定
daemon = False

# タイムアウトの設定
timeout = 60

# メモリ消費を抑える設定
preload_app = True

# ワーカーのリクエスト数を制限
max_requests = 1000
max_requests_jitter = 50

# ログレベルの設定
loglevel = "info"
# Gunicorn configuration file
import multiprocessing

# 同時実行ワーカー数
workers = multiprocessing.cpu_count() * 2 + 1

# ワーカークラスの指定
worker_class = "sync"

# バインドするアドレスとポート
bind = "0.0.0.0:8001"

# プロセスの名前
proc_name = "event_manager"

# デーモン化の設定
daemon = False

# タイムアウトの設定
timeout = 60

# メモリ消費を抑える設定
preload_app = True

# ワーカーのリクエスト数を制限
max_requests = 1000
max_requests_jitter = 50

# ログレベルの設定
loglevel = "info"
