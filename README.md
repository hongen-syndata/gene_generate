🧬 README（English + Japanese）
Gene Variant & Synthetic Sequence Generator
A CLI-based pipeline for generating gene panels, variants, SNPs, and synthetic DNA sequences.

🇺🇸 English Version
Overview
This project provides a CLI-based genomic data generation pipeline that uses LLMs to create:

Gene panels

Variants (SNVs)

SNPs

Synthetic DNA sequences (FASTA)

Database records

It is designed as a foundation for SaMD (Software as a Medical Device) and synthetic genomics applications.

🚀 Current Status
✔ CLI Execution
You can run the entire pipeline by specifying a disease name in main.py:

bash
python main.py
The pipeline performs:

Disease → Gene Panel (LLM)

Variant generation

SNP generation

Synthetic sequence generation (FASTA)

Validation

Database storage

🧪 Supported Variant Types
Currently supported:

Single-base substitution

Single-base deletion

🔧 Planned Extensions
Support for more complex variants is planned:

Multi-base substitutions

Insertions

Frameshift mutations

Complex variants

📡 API (Planned)
The project is currently CLI-only, but FastAPI-based Web API support is planned.

Planned endpoints:

POST /pipeline/run

GET /panel/{id}

GET /sequence/{id}

API support will enable:

Web UI integration (Next.js / Streamlit)

Cloud deployment

External application access

📂 Project Structure
コード
app/
├─ db/               # Database models & session
├─ models/           # Pydantic models
├─ prompts/          # LLM prompts
├─ schemas/          # API schemas (future)
├─ services/         # Core generation logic
├─ utils/            # Utility functions
├─ validation/       # External JSON validation
├─ validator/        # Internal model validation
├─ tests/            # pytest tests
└─ main.py           # CLI entry point
🧬 Pipeline Flow
generate_panel

validate_panel

normalize_panel

validate_gene / validate_variant

generate_snp

validate_snp

generate_sequence

validate_sequence

save_all

🛠 Tech Stack
Python 3.12

SQLAlchemy

Pydantic v2

OpenAI API

pytest / pytest-cov

Ruff

🗺 Roadmap
[ ] FastAPI implementation

[ ] Multi-base variant support

[ ] Insertions / frameshift support

[ ] Dockerization

[ ] Cloud deployment (Azure / GCP / AWS)

[ ] Web UI

[ ] Large gene panel support

📄 License
MIT License (planned)

🇯🇵 日本語版
概要
本プロジェクトは、疾患名から遺伝子パネル・変異（Variant）・SNP・人工 DNA 配列（FASTA）を自動生成する CLI パイプラインです。
SaMD（Software as a Medical Device）領域や人工ゲノムデータ生成の基盤として利用できます。

🚀 現状
✔ CLI で実行可能
main.py に病名を入力することで、以下の処理が自動で実行されます：

bash
python main.py
処理内容：

疾患名 → 遺伝子パネル生成（LLM）

Variant 生成

SNP 生成

人工 DNA 配列（FASTA）生成

バリデーション

DB 保存

🧪 対応している変異
現在対応しているのは 1 塩基変異のみ：

1 塩基置換

1 塩基欠失

🔧 今後の拡張予定
2 塩基以上の置換

挿入（Insertion）

フレームシフト（Frameshift）

複合変異（Complex Variant）

📡 API（今後実装予定）
現在は CLI のみですが、
今後 FastAPI による Web API 化を予定しています。

予定しているエンドポイント：

POST /pipeline/run

GET /panel/{id}

GET /sequence/{id}

API 化により：

Web UI との連携

クラウドデプロイ

外部アプリからの利用

が可能になります。

📂 プロジェクト構成
コード
app/
├─ db/               # DB モデル・接続
├─ models/           # Pydantic モデル
├─ prompts/          # LLM プロンプト
├─ schemas/          # API スキーマ（将来）
├─ services/         # 生成ロジック
├─ utils/            # ユーティリティ
├─ validation/       # 外部 JSON の構造チェック
├─ validator/        # 内部モデルのバリデーション
├─ tests/            # pytest テスト
└─ main.py           # CLI エントリポイント
🧬 パイプラインの流れ
generate_panel

validate_panel

normalize_panel

validate_gene / validate_variant

generate_snp

validate_snp

generate_sequence

validate_sequence

save_all

🛠 技術スタック
Python 3.12

SQLAlchemy

Pydantic v2

OpenAI API

pytest / pytest-cov

Ruff

🗺 ロードマップ
[ ] FastAPI 実装

[ ] 2 塩基以上の変異対応

[ ] 挿入・フレームシフト対応

[ ] Docker 化

[ ] クラウドデプロイ

[ ] Web UI

[ ] 大規模パネル対応
