from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## 読み込み処理の部分のfuncionsをこの.pyファイルで取り扱う ##

# CSVファイルを読み込むfunction(SampleSubmissionはparquet形式)
def load_table_as_pandas(path: Path, verbose: bool = True) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if path.suffix == ".csv":
        if verbose: print("Datatype is CSV")
        df = pl.read_csv(path)
    elif path.suffix == ".parquet":
        if verbose: print("Datatype is Parquet")
        df = pl.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
    
    return df.to_pandas()

#dfと該当のIDを入力することで、dict形式でデータを出力するfunction
def load_ecg_data_by_id(ecg_id, train_df, config) -> dict:
    row = train_df[train_df["id"] == int(ecg_id)]
    if row.empty:
        raise ValueError(f"ID {ecg_id} が train_df に存在しません")

    fs = float(row["fs"].values[0])
    sig_len = int(row["sig_len"].values[0])
    csv_path = list((config.train_data_dir / str(ecg_id)).glob("*.csv"))[0]
    ecg_df = pd.read_csv(csv_path)

    return {
        "id": str(ecg_id),
        "fs": fs,
        "sig_len": sig_len,
        "duration_sec": sig_len / fs,
        "csv_path": csv_path,
        "ecg_df": ecg_df
    }

# CSVデータからECGデータするfunction
def extract_lead_features(ecg_dict: dict) -> dict:
    ecg_df = ecg_dict["ecg_df"]
    lead_names = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF',
                  'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

    lead_stats = {}
    flat_row = {}

    for lead in lead_names:
        series = pd.to_numeric(ecg_df[lead], errors="coerce").dropna()
        stats = {
            "mean": series.mean(),
            "std": series.std(),
            "min": series.min(),
            "max": series.max(),
            "median": series.median(),
        }
        lead_stats[lead] = stats

        # フラットな特徴量名で展開（例：V1_mean, V1_std, ...）
        for stat_name, value in stats.items():
            flat_row[f"{lead}_{stat_name}"] = value

    ecg_dict["lead_stats"] = lead_stats
    ecg_dict["features_row"] = flat_row
    return ecg_dict


#CSVデータのECGデータをPLOTするfunctio
#
#def plot_ecg_waveform(ecg_dict: dict, plot_leads: list[str] = None):
#    ecg_df = ecg_dict["ecg_df"]
#    fs = ecg_dict["fs"]
#    ecg_id = ecg_dict["id"]
#
#    all_leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF',
#                 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
#    plot_leads = plot_leads or all_leads
#
#    time_axis = np.arange(len(ecg_df)) / fs
#    fig, axes = plt.subplots(len(plot_leads), 1, figsize=(20, 1.5 * len(plot_leads)), sharex=True)
#    fig.suptitle(f'ECG Waveform - ID: {ecg_id} (fs={fs:.1f} Hz)', fontsize=18, fontweight='bold', y=0.995)
#
#    for ax, lead in zip(axes, plot_leads):
#        if lead not in ecg_df.columns:
#            continue
#        ecg_df[lead] = pd.to_numeric(ecg_df[lead], errors="coerce")
#        ax.plot(time_axis, ecg_df[lead], color='black', linewidth=1.2, alpha=0.9)
#        ax.fill_between(time_axis, ecg_df[lead], alpha=0.1, color='gray')
#        ax.set_ylabel(lead, fontsize=13, fontweight='bold', rotation=0, ha='right', va='center')
#        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
#        ax.set_xlim(0, len(ecg_df) / fs)
#        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
#        ax.spines['top'].set_visible(False)
#        ax.spines['right'].set_visible(False)
#
#        stats = ecg_dict.get("lead_stats", {}).get(lead, {})
#        if stats:
#            ax.text(0.02, 0.95, f'μ={stats["mean"]:.3f}, σ={stats["std"]:.3f}',
#                    transform=ax.transAxes, fontsize=9, verticalalignment='top',
#                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
#
#    axes[-1].set_xlabel('Time (seconds)', fontsize=14, fontweight='bold')
#    plt.tight_layout()
#    plt.show()
#

def plot_ecg_waveform(ecg_dict: dict, plot_leads: list[str] = None):
    ecg_df = ecg_dict["ecg_df"]
    fs = ecg_dict["fs"]
    ecg_id = ecg_dict["id"]

    all_leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF',
                 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    plot_leads = plot_leads or all_leads

    time_axis = np.arange(len(ecg_df)) / fs
    fig, axes = plt.subplots(len(plot_leads), 1, figsize=(20, 1.5 * len(plot_leads)), sharex=True)
    fig.suptitle(f'ECG Waveform - ID: {ecg_id} (fs={fs:.1f} Hz)', fontsize=18, fontweight='bold', y=0.995)

    # 🧠 ここで axes をリストに変換（1 lead の場合）にバグらないように対応
    if len(plot_leads) == 1:
        axes = [axes]

    for ax, lead in zip(axes, plot_leads):
        if lead not in ecg_df.columns:
            continue
        ecg_df[lead] = pd.to_numeric(ecg_df[lead], errors="coerce")
        ax.plot(time_axis, ecg_df[lead], color='black', linewidth=1.2, alpha=0.9)
        ax.fill_between(time_axis, ecg_df[lead], alpha=0.1, color='gray')
        ax.set_ylabel(lead, fontsize=13, fontweight='bold', rotation=0, ha='right', va='center')
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_xlim(0, len(ecg_df) / fs)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        stats = ecg_dict.get("lead_stats", {}).get(lead, {})
        if stats:
            ax.text(0.02, 0.95, f'μ={stats["mean"]:.3f}, σ={stats["std"]:.3f}',
                    transform=ax.transAxes, fontsize=9, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    axes[-1].set_xlabel('Time (seconds)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()