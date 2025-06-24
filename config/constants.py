"""
定数・パス管理モジュール
作成日: 2025年6月24日
目的: システム全体で使用する定数、パス、設定値の統一管理
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Paths:
    """ディレクトリ構造管理クラス"""
    
    # ベースディレクトリ
    BASE_DIR: Path = Path("C:/Projects_workspace/03_unified_system")
    
    # データディレクトリ
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    SQLITE_DIR: Path = DATA_DIR / "sqlite"
    ACCESS_DIR: Path = DATA_DIR / "access"
    BACKUP_DIR: Path = DATA_DIR / "backup"
    
    # ログディレクトリ
    LOGS_DIR: Path = BASE_DIR / "logs"
    ERROR_LOGS_DIR: Path = LOGS_DIR / "errors"
    
    # 設定ディレクトリ
    CONFIG_DIR: Path = BASE_DIR / "config"
    
    # ソースコードディレクトリ
    SRC_DIR: Path = BASE_DIR / "src"
    CORE_DIR: Path = SRC_DIR / "core"
    
    # 一時ディレクトリ
    TEMP_DIR: Path = BASE_DIR / "temp"
    
    @classmethod
    def create_directories(cls) -> None:
        """必要なディレクトリを作成"""
        paths_to_create = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.SQLITE_DIR,
            cls.ACCESS_DIR,
            cls.BACKUP_DIR,
            cls.LOGS_DIR,
            cls.ERROR_LOGS_DIR,
            cls.CONFIG_DIR,
            cls.SRC_DIR,
            cls.CORE_DIR,
            cls.TEMP_DIR
        ]
        
        for path in paths_to_create:
            path.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_full_path(cls, relative_path: str) -> Path:
        """相対パスを絶対パスに変換"""
        return cls.BASE_DIR / relative_path


@dataclass
class FilePatterns:
    """処理対象ファイルパターン定義"""
    
    # PLMファイルパターン
    PLM_PATTERN: str = "GetPLMItmPlntInfo_*.txt"
    PLM_ENCODING: str = "shift_jis"
    PLM_DELIMITER: str = "\t"
    
    # WBSファイルパターン
    WBS_PATTERN: str = "GetSekkeiWBSJisseki.txt"
    WBS_ENCODING: str = "shift_jis"
    WBS_DELIMITER: str = "\t"
    
    # BOMファイルパターン
    BOM_PATTERN: str = "MARA_DL.csv"
    BOM_ENCODING: str = "shift_jis"
    BOM_DELIMITER: str = ","
    
    # 生産ファイルパターン
    PRODUCTION_PATTERN: str = "PP_DL_CSV_SEISAN_YOTEI.csv"
    PRODUCTION_ENCODING: str = "shift_jis"
    PRODUCTION_DELIMITER: str = ","
    
    # 在庫ファイルパターン
    INVENTORY_PATTERN: str = "dbo_提出用_経理_滞留在庫資料_通常.xlsx"
    INVENTORY_ENCODING: str = "utf-8"
    INVENTORY_SHEET_NAME: str = "Sheet1"
    
    # 全パターンの辞書
    @classmethod
    def get_all_patterns(cls) -> Dict[str, Dict[str, str]]:
        """全ファイルパターン情報を辞書で返す"""
        return {
            "PLM": {
                "pattern": cls.PLM_PATTERN,
                "encoding": cls.PLM_ENCODING,
                "delimiter": cls.PLM_DELIMITER,
                "type": "txt"
            },
            "WBS": {
                "pattern": cls.WBS_PATTERN,
                "encoding": cls.WBS_ENCODING,
                "delimiter": cls.WBS_DELIMITER,
                "type": "txt"
            },
            "BOM": {
                "pattern": cls.BOM_PATTERN,
                "encoding": cls.BOM_ENCODING,
                "delimiter": cls.BOM_DELIMITER,
                "type": "csv"
            },
            "PRODUCTION": {
                "pattern": cls.PRODUCTION_PATTERN,
                "encoding": cls.PRODUCTION_ENCODING,
                "delimiter": cls.PRODUCTION_DELIMITER,
                "type": "csv"
            },
            "INVENTORY": {
                "pattern": cls.INVENTORY_PATTERN,
                "encoding": cls.INVENTORY_ENCODING,
                "sheet_name": cls.INVENTORY_SHEET_NAME,
                "type": "xlsx"
            }
        }


@dataclass
class ProcessConfig:
    """処理性能設定"""
    
    # チャンク処理設定
    DEFAULT_CHUNK_SIZE: int = 50000
    LARGE_FILE_CHUNK_SIZE: int = 100000
    MEMORY_LIMIT_MB: int = 512
    
    # 並行処理設定
    MAX_WORKERS: int = 4
    TIMEOUT_SECONDS: int = 300
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2
    
    # ファイルサイズ閾値
    SMALL_FILE_MB: int = 10
    MEDIUM_FILE_MB: int = 100
    LARGE_FILE_MB: int = 500
    
    # エンコーディング設定
    SUPPORTED_ENCODINGS: List[str] = None
    ENCODING_DETECTION_CONFIDENCE: float = 0.7
    ENCODING_SAMPLE_SIZE: int = 10240
    
    def __post_init__(self):
        """デフォルト値の設定"""
        if self.SUPPORTED_ENCODINGS is None:
            self.SUPPORTED_ENCODINGS = [
                "utf-8", "shift_jis", "cp932", 
                "iso-2022-jp", "euc-jp"
            ]
    
    @classmethod
    def get_chunk_size(cls, file_size_mb: float) -> int:
        """ファイルサイズに応じて適切なチャンクサイズを返す"""
        if file_size_mb <= cls.SMALL_FILE_MB:
            return cls.DEFAULT_CHUNK_SIZE
        elif file_size_mb <= cls.MEDIUM_FILE_MB:
            return cls.DEFAULT_CHUNK_SIZE
        else:
            return cls.LARGE_FILE_CHUNK_SIZE
    
    @classmethod
    def get_worker_count(cls, file_count: int) -> int:
        """ファイル数に応じて適切なワーカー数を返す"""
        return min(cls.MAX_WORKERS, max(1, file_count))


@dataclass
class DatabaseConfig:
    """データベース設定"""
    
    # SQLiteファイル設定
    DB_FILENAME: str = "unified_database.db"
    BACKUP_PREFIX: str = "backup_"
    
    # SQLite最適化設定
    PRAGMA_SETTINGS: Dict[str, str] = None
    
    # テーブル名設定
    TABLE_MAPPING: Dict[str, str] = None
    
    # インデックス設定
    AUTO_INDEX_COLUMNS: List[str] = None
    COMPOSITE_INDEXES: List[Dict[str, any]] = None
    
    def __post_init__(self):
        """デフォルト値の設定"""
        if self.PRAGMA_SETTINGS is None:
            self.PRAGMA_SETTINGS = {
                "journal_mode": "WAL",
                "synchronous": "NORMAL",
                "cache_size": "10000",
                "mmap_size": "268435456",
                "temp_store": "MEMORY",
                "page_size": "4096"
            }
        
        if self.TABLE_MAPPING is None:
            self.TABLE_MAPPING = {
                "PLM": "plm_item_plant_info",
                "WBS": "wbs_sekkei_jisseki",
                "BOM": "bom_mara_data",
                "PRODUCTION": "production_yotei",
                "INVENTORY": "inventory_teiryu"
            }
        
        if self.AUTO_INDEX_COLUMNS is None:
            self.AUTO_INDEX_COLUMNS = [
                "id", "date", "code", "item_code", 
                "plant_code", "created_at", "updated_at"
            ]
        
        if self.COMPOSITE_INDEXES is None:
            self.COMPOSITE_INDEXES = [
                {
                    "columns": ["date", "plant_code"],
                    "name": "idx_date_plant"
                },
                {
                    "columns": ["item_code", "plant_code"],
                    "name": "idx_item_plant"
                },
                {
                    "columns": ["created_at", "updated_at"],
                    "name": "idx_timestamps"
                }
            ]


@dataclass
class LoggingConfig:
    """ログ設定"""
    
    # ログレベル
    LOG_LEVEL: str = "INFO"
    
    # ログファイル設定
    LOG_FILENAME: str = "unified_system.log"
    ERROR_LOG_FILENAME: str = "errors.log"
    
    # ログフォーマット
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    
    # ローテーション設定
    MAX_FILE_SIZE: str = "10MB"
    BACKUP_COUNT: int = 5
    
    # 詳細ログ出力対象
    DETAILED_MODULES: List[str] = None
    
    def __post_init__(self):
        """デフォルト値の設定"""
        if self.DETAILED_MODULES is None:
            self.DETAILED_MODULES = [
                "sqlite_manager",
                "file_processor",
                "database_operations"
            ]


# システム全体で使用する定数
class SystemConstants:
    """システム定数クラス"""
    
    # バージョン情報
    SYSTEM_VERSION: str = "1.0.0"
    SYSTEM_NAME: str = "統合データ更新処理システム"
    
    # 日付フォーマット
    DATE_FORMAT: str = "%Y-%m-%d"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"
    
    # ファイル拡張子
    SUPPORTED_EXTENSIONS: Tuple[str, ...] = (".csv", ".txt", ".xlsx", ".xls")
    
    # エラーメッセージ
    ERROR_MESSAGES: Dict[str, str] = {
        "FILE_NOT_FOUND": "指定されたファイルが見つかりません: {filepath}",
        "ENCODING_ERROR": "ファイルのエンコーディングを判定できません: {filepath}",
        "DATABASE_ERROR": "データベース操作でエラーが発生しました: {error}",
        "PROCESSING_ERROR": "ファイル処理中にエラーが発生しました: {error}",
        "MEMORY_ERROR": "メモリ不足によりエラーが発生しました",
        "TIMEOUT_ERROR": "処理がタイムアウトしました"
    }
    
    # 成功メッセージ
    SUCCESS_MESSAGES: Dict[str, str] = {
        "FILE_PROCESSED": "ファイルの処理が完了しました: {filepath}",
        "DATABASE_UPDATED": "データベースの更新が完了しました: {table_name}",
        "BACKUP_CREATED": "バックアップファイルを作成しました: {backup_path}",
        "SYSTEM_INITIALIZED": "システムの初期化が完了しました"
    }


# 環境変数の取得
def get_env_variable(key: str, default: str = None) -> Optional[str]:
    """環境変数を取得"""
    return os.getenv(key, default)


# 設定の検証
def validate_configuration() -> List[str]:
    """設定の妥当性を検証し、問題点をリストで返す"""
    issues = []
    
    # ディレクトリの存在確認
    paths = Paths()
    if not paths.BASE_DIR.exists():
        issues.append(f"ベースディレクトリが存在しません: {paths.BASE_DIR}")
    
    # 設定ファイルの存在確認
    config_file = paths.CONFIG_DIR / "database_config.yaml"
    if not config_file.exists():
        issues.append(f"設定ファイルが存在しません: {config_file}")
    
    return issues


# 初期化処理
def initialize_system() -> bool:
    """システムの初期化"""
    try:
        # ディレクトリ作成
        Paths.create_directories()
        
        # 設定検証
        issues = validate_configuration()
        if issues:
            print("設定に問題があります:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        print(SystemConstants.SUCCESS_MESSAGES["SYSTEM_INITIALIZED"])
        return True
        
    except Exception as e:
        print(f"システム初期化中にエラーが発生しました: {e}")
        return False


if __name__ == "__main__":
    # テスト実行
    print(f"{SystemConstants.SYSTEM_NAME} v{SystemConstants.SYSTEM_VERSION}")
    print("=" * 50)
    
    # 初期化テスト
    if initialize_system():
        print("✅ システム初期化成功")
        
        # 設定値の表示
        print("\n📁 パス設定:")
        paths = Paths()
        print(f"  ベースディレクトリ: {paths.BASE_DIR}")
        print(f"  データディレクトリ: {paths.DATA_DIR}")
        print(f"  ログディレクトリ: {paths.LOGS_DIR}")
        
        print("\n📋 ファイルパターン:")
        patterns = FilePatterns.get_all_patterns()
        for name, config in patterns.items():
            print(f"  {name}: {config['pattern']}")
        
        print("\n⚙️  処理設定:")
        process_config = ProcessConfig()
        print(f"  チャンクサイズ: {process_config.DEFAULT_CHUNK_SIZE:,}")
        print(f"  最大ワーカー数: {process_config.MAX_WORKERS}")
        print(f"  タイムアウト: {process_config.TIMEOUT_SECONDS}秒")
        
    else:
        print("❌ システム初期化失敗")
