import pandas as pd


def read_table(path: str) -> pd.DataFrame:
    required_columns = [
        "id", "taxon", "pid", "line_1", "line_2", "line_3"
    ]

    df = pd.read_excel(path)

    available_columns = [col for col in required_columns if col in df.columns]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print("Missing columns in source file:")
        for col in missing_columns:
            print(f"- {col}")

    return df[available_columns]