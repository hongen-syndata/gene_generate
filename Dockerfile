FROM python:3.12-slim

WORKDIR /app

# 依存関係を先にコピーしてインストール（キャッシュ効率が良い）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY . .

# Render でもローカルでも動くようにポートを環境変数対応
ENV PORT=8000

# FastAPI を起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
