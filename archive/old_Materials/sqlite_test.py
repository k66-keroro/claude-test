
"""
SQLite格納確認 - 最短テストスクリプト
既存ファイルを使ってすぐに動作確認
"""

import sqlite3
import pandas as pd
from pathlib import Path
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_sqlite_test():
    """最短SQLite格納テスト"""
    
    # 1. データベースファイル設定
    db_path = Path("quick_test.db")
    
    # 2. サンプルデータ作成（既存ファイルがない場合）
    sample_file = Path("sample_data.csv")
    if not sample_file.exists():
        print("📁 サンプルデータを作成中...")
        sample_data = pd.DataFrame({
            'ID': range(1, 101),
            '商品名': [f'商品_{i:03d}' for i in range(1, 101)],
            '価格': [i * 100 for i in range(1, 101)],
            '在庫数': [i * 5 for i in range(1, 101)],
            '登録日': pd.date_range('2024-01-01', periods=100, freq='D')
        })
        sample_data.to_csv(sample_file, index=False, encoding='utf-8-sig')
        print(f"✅ サンプルファイル作成: {sample_file}")
    
    # 3. SQLiteに格納
    print("🔄 SQLiteに格納中...")
    try:
        # ファイル読み込み
        df = pd.read_csv(sample_file, encoding='utf-8-sig')
        print(f"📊 読み込み完了: {len(df)}行, {len(df.columns)}列")
        print(f"列名: {list(df.columns)}")
        
        # SQLite接続・格納
        with sqlite3.connect(db_path) as conn:
            df.to_sql('test_table', conn, if_exists='replace', index=False)
            print(f"✅ SQLite格納完了: {db_path}")
        
    except Exception as e:
        print(f"❌ 格納エラー: {e}")
        return False
    
    # 4. 格納確認
    print("🔍 格納データ確認中...")
    try:
        with sqlite3.connect(db_path) as conn:
            # テーブル一覧
            tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
            print(f"📋 テーブル一覧: {tables['name'].tolist()}")
            
            # データ確認
            result = pd.read_sql("SELECT * FROM test_table LIMIT 5", conn)
            print(f"📄 データサンプル (最初の5行):")
            print(result.to_string(index=False))
            
            # 行数確認
            count = pd.read_sql("SELECT COUNT(*) as count FROM test_table", conn)
            print(f"📊 総行数: {count['count'].iloc[0]}行")
            
            # テーブル構造確認
            schema = pd.read_sql("PRAGMA table_info(test_table)", conn)
            print(f"🔧 テーブル構造:")
            for _, row in schema.iterrows():
                print(f"  {row['name']}: {row['type']}")
        
        print("✅ 格納確認完了！")
        return True
        
    except Exception as e:
        print(f"❌ 確認エラー: {e}")
        return False

def detect_encoding(file_path: Path) -> str:
    """ファイルのエンコーディングを自動判定"""
    try:
        import chardet
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 最初の10KB読み込み
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            print(f"🔍 エンコーディング検出: {encoding} (信頼度: {confidence:.2f})")
            return encoding
    except ImportError:
        print("⚠️ chardetがインストールされていません。一般的なエンコーディングを試行します")
        return None

def try_read_file(file_path: Path):
    """複数のエンコーディングを試してファイルを読み込み"""
    
    # 試行するエンコーディングのリスト（日本語ファイル対応）
    encodings = ['utf-8-sig', 'utf-8', 'shift-jis', 'euc-jp', 'cp932', 'iso-2022-jp']
    
    # chardetによる自動判定を最初に試す
    detected_encoding = detect_encoding(file_path)
    if detected_encoding and detected_encoding not in encodings:
        encodings.insert(0, detected_encoding)
    
    # 各エンコーディングを試行
    for encoding in encodings:
        try:
            print(f"🔄 エンコーディング試行: {encoding}")
            
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path, encoding=encoding, dtype=str)
            elif file_path.suffix.lower() == '.txt':
                # タブ区切りとカンマ区切りを両方試す
                try:
                    df = pd.read_csv(file_path, sep='\t', encoding=encoding, dtype=str)
                    if len(df.columns) == 1:  # タブ区切りでない場合
                        df = pd.read_csv(file_path, sep=',', encoding=encoding, dtype=str)
                except:
                    df = pd.read_csv(file_path, sep=',', encoding=encoding, dtype=str)
            else:
                return None, None
            
            print(f"✅ 読み込み成功: {encoding}")
            return df, encoding
            
        except UnicodeDecodeError:
            print(f"❌ {encoding} は失敗")
            continue
        except Exception as e:
            print(f"❌ {encoding} でエラー: {str(e)[:100]}")
            continue
    
    return None, None

def test_with_your_file(file_path: str):
    """既存ファイルでのテスト"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ ファイルが見つかりません: {file_path}")
        return False
    
    print(f"📁 ファイル処理開始: {file_path}")
    print(f"📏 ファイルサイズ: {file_path.stat().st_size / 1024 / 1024:.2f}MB")
    
    # データベース設定
    db_path = Path(f"test_{file_path.stem}.db")
    table_name = file_path.stem.lower().replace('-', '_').replace(' ', '_')
    
    try:
        # ファイル形式判定・読み込み
        if file_path.suffix.lower() in ['.xlsx', '.xls']:
            print("📊 Excelファイルを読み込み中...")
            df = pd.read_excel(file_path, dtype=str)
            encoding_used = "Excel形式"
        elif file_path.suffix.lower() in ['.csv', '.txt']:
            print("📊 テキストファイルを読み込み中...")
            df, encoding_used = try_read_file(file_path)
            if df is None:
                print("❌ 全てのエンコーディングで読み込み失敗")
                return False
        else:
            print(f"❌ サポートされていないファイル形式: {file_path.suffix}")
            return False
        
        print(f"📊 読み込み完了: {len(df)}行, {len(df.columns)}列")
        print(f"📝 使用エンコーディング: {encoding_used}")
        
        # 列名確認
        print("📋 列名一覧:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1:2d}. {col}")
        
        # SQLiteに格納
        print("🔄 SQLiteに格納中...")
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        print(f"✅ 格納完了: {table_name} -> {db_path}")
        
        # 確認
        with sqlite3.connect(db_path) as conn:
            count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", conn)
            sample = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 3", conn)
            
            print(f"📊 格納行数: {count['count'].iloc[0]}行")
            print("📄 サンプルデータ:")
            print(sample.to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ 処理エラー: {e}")
        return False

def interactive_test():
    """対話式テスト"""
    print("=== SQLite格納確認ツール ===")
    print("1. サンプルデータでテスト")
    print("2. 既存ファイルでテスト")
    
    choice = input("選択 (1 または 2): ").strip()
    
    if choice == "1":
        quick_sqlite_test()
    elif choice == "2":
        file_path = input("ファイルパスを入力: ").strip()
        test_with_your_file(file_path)
    else:
        print("❌ 無効な選択です")

if __name__ == "__main__":
    # 直接実行の場合
    print("🚀 SQLite格納テスト開始")
    
    # まずサンプルデータでテスト
    success = quick_sqlite_test()
    
    if success:
        print("\n" + "="*50)
        print("✅ 基本テスト成功！")
        print("次は既存ファイルでテストしてみてください")
        print("="*50)
        
        # 既存ファイルのテストを促す
        test_file = input("\n既存ファイルのパスを入力 (Enter でスキップ): ").strip()
        if test_file:
            test_with_your_file(test_file)
    
    print("\n🎉 テスト完了！")
