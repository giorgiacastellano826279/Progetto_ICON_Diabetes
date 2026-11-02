import pandas as pd
import numpy as np

COLUMNS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome"
]

# Colonne in cui il valore 0 rappresenta un dato mancante non fisiologico
ZERO_INVALID_COLS = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

def load_and_clean_data(raw_path="data/raw/diabetes.csv", output_path="data/processed/diabetes_clean.csv"):
    # 1. Caricamento dati grezzi
    df = pd.read_csv(raw_path, header=None, names=COLUMNS)
    print(f"[PREPROCESS] Dataset caricato: {df.shape[0]} righe, {df.shape[1]} colonne.")

    # 2. Sostituzione degli zeri non fisiologici con NaN
    df[ZERO_INVALID_COLS] = df[ZERO_INVALID_COLS].replace(0, np.nan)
    
    # 3. Imputazione con la mediana di ciascuna colonna
    for col in ZERO_INVALID_COLS:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"[PREPROCESS] Imputati NaN per colonna '{col}' con mediana: {median_val:.2f}")

    # 4. Salvataggio dataset pulito
    df.to_csv(output_path, index=False)
    print(f"[PREPROCESS] File pulito salvato con successo in '{output_path}'.")
    return df

if __name__ == "__main__":
    load_and_clean_data()
