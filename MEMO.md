# 1. なぜ .py ファイルにも import が必要なのか

✅ 理由：関数やクラスのスコープは「定義されたファイル内」で完結するから
たとえば、以下のような .py ファイル（例：data_loader.py）があるとします：

```
def load_csv_as_pandas(path: Path) -> pd.DataFrame:
    df = pl.read_csv(path)
    return df.to_pandas()
```

この関数内で Path, pl, pd を使っていますが、この .py ファイル内で import していない限り、関数定義時点でエラーになります。Notebook 側で import pandas as pd していても、それは Notebook の名前空間であって、.py ファイルの名前空間とは別です。

🧠 重要なポイント
- Python は 関数定義時点で必要な名前（変数・型・関数）を解決しようとする。
- .py ファイルを import するとき、Python はそのファイルを 一度実行して関数やクラスを登録する。
- その実行時に import が不足していると、当然 NameError や ImportError になります。

💡補足：関数の中でしか使わないなら、関数内で import してもOKのよう
```
def load_csv_as_pandas(path):
    import polars as pl
    df = pl.read_csv(path)
    return df.to_pandas()
```
ただし、これはあまり推奨されません。通常はファイルの冒頭で import をまとめて書く方が可読性・保守性が高いです。

---

