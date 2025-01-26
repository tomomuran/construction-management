# Construction Management System

建設現場の管理を効率化するためのDjangoベースの管理システムです。

## 機能

- プロジェクト管理
- スケジュール管理
- コスト管理
- 資材管理
- 作業員管理

## 必要条件

- Python 3.8以上
- Django 5.1以上

## インストール

1. リポジトリのクローン:
```bash
git clone https://github.com/yourusername/construction-management.git
cd construction-management
```

2. 仮想環境の作成と有効化:
```bash
python -m venv venv
source venv/bin/activate  # Linuxの場合
venv\Scripts\activate     # Windowsの場合
```

3. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

4. 環境変数の設定:
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

5. データベースのマイグレーション:
```bash
python manage.py migrate
```

6. 開発サーバーの起動:
```bash
python manage.py runserver
```

## 環境変数

以下の環境変数を`.env`ファイルに設定してください：

- `DJANGO_SECRET_KEY`: Djangoのシークレットキー
- `DJANGO_DEBUG`: デバッグモード（True/False）
- `DJANGO_ALLOWED_HOSTS`: カンマ区切りの許可するホスト名

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 