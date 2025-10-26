#読み込み処理の部分のfuncionsをこの.pyファイルで取り扱う
import yaml
from pathlib import Path


# Pathの管理を行うCONFIGデータパス

PROJECT_ROOT = Path("/mnt/c/Users/yohei/Desktop/physionet-ecg-image-digitization")

class CONFIG:
    def __init__(self, config_path: Path):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)
        self.train_csv_path = PROJECT_ROOT / cfg["train_csv"]
        self.test_csv_path = PROJECT_ROOT / cfg["test_csv"]
        self.sample_submission_csv_path = PROJECT_ROOT / cfg["sample_submission"]
        self.train_data_dir = PROJECT_ROOT / cfg["train_dir"]
        self.test_data_dir = PROJECT_ROOT / cfg["test_dir"]

# 使用例
config = CONFIG(PROJECT_ROOT / "config.yaml")
print(config.train_csv_path)
