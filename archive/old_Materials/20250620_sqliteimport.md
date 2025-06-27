`# config/constants.py で定義したパスを使用
from config.constants import Paths

# SQLiteManager初期化
db_manager = SQLiteManager(Paths.SQLITE_DB)

# 単一ファイル処理
success = db_manager.bulk_insert_from_file(
    "data/raw/MARA_DL.csv",  # BOMデータ
    "bom_master",
    chunk_size=50000,  # 60万件対応
    dtype_mapping={
        'material_code': 'str',
        'created_date': 'datetime',
        'quantity': 'numeric'
    }
)

# 複数ファイル並列処理
file_mapping = {
    Paths.RAW_DATA / "GetPLMItmPlntInfo_20240620.txt": "plm_items",
    Paths.RAW_DATA / "GetSekkeiWBSJisseki.txt": "wbs_actual",
    Paths.RAW_DATA / "MARA_DL.csv": "bom_master"
}

results = db_manager.parallel_process_files(file_mapping)`