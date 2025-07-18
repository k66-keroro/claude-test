# 毎日のデータ更新処理刷新ツール

## 1. プロジェクト概要
既存の手動データ更新処理を自動化・効率化するためのPythonツールです。
多様な形式（CSV, TXT, Excel）のデータファイルを読み込み、SQLiteデータベースに一括で取り込みます。

## 2. アーキテクチャ

### 主要コンポーネント

1. **`src/main.py`** - メインのバッチ処理プログラム
   - 優先順位CSVファイルに基づいてファイルを一括処理
   - テーブル構造の自動最適化（主キー追加＋インデックス作成）

2. **`src/core/sqlite_manager.py`** - 統一SQLite管理クラス
   - ファイル処理の統一インターフェース
   - エンコーディング自動検出
   - テーブル構造最適化

3. **`src/core/sqlite_gui_tool_v2_fixed.py`** - GUI検証・修正ツール
   - 個別ファイルの処理と検証
   - エラー再処理機能
   - データベース管理機能

## 3. プロジェクト構造

```
claude-test/
├── README.md                 # (このファイル) プロジェクトの概要、使い方
├── gemini.md                 # Gemini用の作業ToDoリスト
├── docs/                     # ドキュメント
│   ├── progress.md           # データ取り込みの進捗状況
│   ├── PROGRESS.md           # 現在のプロジェクト進捗
│   └── SPECIFICATION.md      # 仕様書
├── src/                      # ソースコード
│   ├── main.py               # メイン実行スクリプト
│   └── core/                 # コア機能モジュール
│       ├── sqlite_manager.py      # DB操作のコアロジック
│       └── sqlite_gui_tool_v2_fixed.py  # GUI検証ツール
├── config/                   # 設定ファイル
│   ├── constants.py          # 設定定数
│   ├── データベース構成.yaml  # DB設定
│   ├── テキスト一覧.csv      # 処理対象ファイル定義
│   └── index_definitions.txt # インデックス定義
├── data/                     # データディレクトリ
│   ├── csv/                  # 入力データファイル
│   └── sqlite/               # 出力SQLiteデータベース
├── logs/                     # ログファイル
└── archive/                  # 古い資料やアーカイブ
```

## 4. 使用方法

### 4.1. バッチ処理（main.py）
```bash
cd src
python main.py
```

### 4.2. GUIツール
```bash
cd src/core
python sqlite_gui_tool_v2_fixed.py
```

## 5. 主要モジュールと機能

### 5.1. バッチ処理
- **`src/main.py`**:
  - `テキスト一覧.csv` を読み込み、処理の順序を決定
  - `sqlite_manager`を呼び出して、ファイルの取り込み処理を実行
  - 処理完了後に自動的にテーブル構造を最適化

### 5.2. SQLite管理
- **`src/core/sqlite_manager.py`**:
  - ファイル（CSV, TXT, Excel）のエンコーディングを自動判定
  - ファイルの区切り文字（カンマ, タブ, スペース）を判別
  - `pandas`を利用してデータを読み込み、SQLiteに高速で一括挿入
  - 主キーとインデックスの自動追加

### 5.3. 統一インターフェース

#### `SQLiteManager.process_single_file()`
```python
success, error_message = manager.process_single_file(
    file_path=Path("data.csv"),
    table_name="mytable",
    encoding="auto",
    quoting=None,
    finalize_structure=True,  # 主キーとインデックスを追加
    index_columns=["col1", "col2"]
)
```

#### `SQLiteManager.get_file_processing_config()`
```python
config = manager.get_file_processing_config("zm37.txt")
# 戻り値: {'encoding': 'cp932', 'quoting': 'none'}
```

## 6. 設定ファイル

- **`config/テキスト一覧.csv`**: 処理対象ファイルの優先順位を定義（列: ファイル名, テーブル名, 重要度）
- **`config/index_definitions.txt`**: インデックス対象カラムを定義（タブ区切り: テーブル名, カラム1, カラム2）
- **`config/constants.py`**: 設定定数とパス管理
- **`config/データベース構成.yaml`**: SQLiteデータベース設定

## 7. 今後の計画 (ToDo)

### 7.1. 既存の計画
1. **`sqlite_manager.py`の改修**:
   - [x] **済** 区切り文字の判定ロジックを強化し、多様なTXT/CSVファイルに対応
2. **主キーの定義**:
   - [ ] `主キー.xlsx` の情報に基づき、各テーブルに主キー制約を追加する機能を実装
3. **テストコードの作成**:
   - [ ] `tests/` フォルダを作成し、単体テストを実装

### 7.2. 新たな改善提案

#### 🔧 コア機能の改善
1. **テーブル命名規則の標準化**: `sqlite_manager`モジュールにおけるテーブル命名規則を統一し、全テーブルで一貫性を確保
2. **並列処理のサポート追加**: 大規模なデータセットや複数ファイルの同時処理効率を向上
3. **API仕様の策定**: 設計ガイドライン、エラーコード、リクエスト/レスポンス形式の標準化

#### 📊 監視・品質向上
4. **ロギングと監視機能の統合**: パフォーマンスメトリクス追跡とトラブルシューティング機能
5. **徹底的なテスト**: 様々なユースケース、データセット、構成での動作検証
6. **エラーハンドリングの実装**: コードベースとユーザー入力の検証機能強化

#### 🔄 継続的改善
7. **継続的な更新**: ユーザーフィードバックと業界トレンドに基づく機能拡張

### 7.3. 短期間で完了可能な追加タスク

#### 🖥️ ユーザーインターフェース
1. **APIにおけるページネーション**: 複数ファイル表示時のページ分割機能
2. **GUIインターフェースの改善**: PythonとTkinterライブラリを使用した直感的な操作画面
3. **検索機能の統合**: ファイル名や日付範囲での絞り込み検索

#### 📤 データエクスポート機能
4. **処理済みデータのエクスポート**: CSV、JSONなど複数形式でのダウンロード機能
5. **別のファイル形式へのエクスポート**: XLSX形式でのエクスポート機能
6. **レポート生成機能**: 選択基準に基づくカスタムレポート作成

#### 🔐 セキュリティ・共有機能
7. **処理済みデータの共有機能**: 組織・部門内での安全なデータ共有環境

## 8. 技術的な優先順位

### 優先度: 高
- [ ] テーブル命名規則の標準化実装
- [ ] エラーハンドリングの強化
- [ ] 基本的なログ機能の拡充

### 優先度: 中
- [ ] 並列処理機能の実装
- [ ] API仕様の設計・実装
- [ ] テストコードの作成

### 優先度: 低
- [ ] GUI インターフェースの開発
- [ ] 高度な監視機能の実装
- [ ] セキュアな共有機能の実装

## 9. 現在の進捗状況
- [x] **基本的なデータ取り込み機能**: CSV, TXT, Excelファイルの読み込み
- [x] **区切り文字の自動判定**: カンマ, タブ, スペース区切りに対応
- [x] **エンコーディング自動判定**: 文字化けを防ぐ自動判定機能
- [x] **SQLiteデータベースへの一括挿入**: 高速なデータ処理
- [x] **設定ファイルの整備**: 定数・パス管理、データベース設定
- [x] **GUI検証ツール**: 個別ファイル処理と検証機能

## 10. 貢献とフィードバック
このプロジェクトは継続的に改善されています。新機能の提案、バグレポート、コードの改善案などのフィードバックを歓迎します。

---

**claude.txt** - チャットの容量制限対策として、プロジェクトの状況を随時更新中