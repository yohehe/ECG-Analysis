#DATA PathなどのCONFIGデータを読み込むfunction
import yaml
from pathlib import Path

class DataConfig:
    def __init__(self, config_yaml_path: Path, root: Path):
        with open(config_yaml_path, "r") as f:
            cfg = yaml.safe_load(f)
        self.train_csv_path = root / cfg["train_csv"]
        self.test_csv_path = root / cfg["test_csv"]
        self.sample_submission_csv_path = root / cfg["sample_submission"]
        self.train_data_dir = root / cfg["train_dir"]
        self.test_data_dir = root / cfg["test_dir"]
