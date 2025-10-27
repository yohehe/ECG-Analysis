## OSの分類判定
import platform
from pathlib import Path

def detect_os() -> str:
    """
    Detect the current operating system.
    Returns one of: 'windows', 'mac', 'wsl', 'linux'
    """
    system = platform.system().lower()

    if system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'mac'
    elif system == 'linux':
        try:
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                if 'microsoft' in version_info or 'wsl' in version_info:
                    return 'wsl'
        except FileNotFoundError:
            pass
        return 'linux'
    else:
        return 'unknown'

# detect
#detect_os()

# windowsPathをwslのPathに変換するfunction

def windows_to_wsl_path(windows_path: str) -> Path:
    """
    Convert a Windows-style path to WSL-style /mnt/... path.
    
    Example:
        "C:\\Users\\yohei\\Desktop\\ECG_Dataset_fromKaggle"
        → Path("/mnt/c/Users/yohei/Desktop/ECG_Dataset_fromKaggle")
    """
    # Remove drive letter and colon
    drive, rest = windows_path[0].lower(), windows_path[2:]
    
    # Replace backslashes with forward slashes
    rest = rest.replace("\\", "/")
    
    # Construct WSL path
    wsl_path = f"/mnt/{drive}{rest}"
    
    return Path(wsl_path)

# 絶地PATHで環境依存せずにsrcフォルダをimportできるようにするコード例
## Notebookの作業ディレクトリを基準にパスを追加
#project_root = Path.cwd()
#sys.path.append(str(project_root / "src"))
#
#from myfunctions import detect_os, windows_to_wsl_path

# CONFIGで設定したPathの確認
def check_config_paths(config_class):
    missing = []
    for attr in dir(config_class):
        if attr.startswith("_"):
            continue
        value = getattr(config_class, attr)
        if isinstance(value, Path):
            if not value.exists():
                missing.append((attr, value))
    if missing:
        print("以下のパスが存在しません:")
        for name, path in missing:
            print(f" - {name}: {path}")
    else:
        print("すべてのパスが存在します")

# 使用例 CONFIGで設定したPathの存在確認
#check_config_paths(CONFIG)

#config.yamlを配置したフォルダをルートフォルダと設定する
def find_project_root(marker: str = "config.yaml") -> Path:
    path = Path.cwd()
    while not (path / marker).exists() and path != path.parent:
        path = path.parent
    return path
