import os
import pandas as pd
import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from models import get_models

def run_ablation_study(
    data_path="data/processed/diabetes_enriched.csv",
    output_summary_path="results/ablation_metrics_summary.csv"
):
    print("[EVALUATE] Caricamento dataset arricchito...")
    df = pd.read_csv(data_path)

    # Definizione delle feature per le due configurazioni dello studio di ablazione
    raw_features = [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
    ]
    kb_features = [
        "KB_Hyperglycemic", "KB_Obese", "KB_Hypertensive",
        "KB_Senior", "KB_HighRiskProfile"
    ]
    enriched_features = raw_features + kb_features
    target = "Outcome"

    X_raw = df[raw_features]
    X_enriched = df[enriched_features]
    y = df[target]

    # Repeated Stratified K-Fold (5 fold x 5 ripetizioni = 25 stime per modello)
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)

    scoring = {
        "accuracy": "accuracy",
        "f1_macro": "f1_macro",
        "roc_auc": "roc_auc"
    }

    results = []
    models = get_models()

    print("\n[EVALUATE] Inizio Studio di Ablazione con Repeated Stratified K-Fold (25 run per modello)...\n")

    for model_name, model in models.items():
        print(f"--> Valutazione {model_name}...")

        # 1. Configurazione Baseline (Senza KB)
        scores_raw = cross_validate(model, X_raw, y, cv=cv, scoring=scoring, n_jobs=-1)
        acc_raw_mean, acc_raw_std = np.mean(scores_raw["test_accuracy"]), np.std(scores_raw["test_accuracy"])
        f1_raw_mean, f1_raw_std = np.mean(scores_raw["test_f1_macro"]), np.std(scores_raw["test_f1_macro"])
        auc_raw_mean, auc_raw_std = np.mean(scores_raw["test_roc_auc"]), np.std(scores_raw["test_roc_auc"])

        results.append({
            "Model": model_name,
            "Configuration": "Baseline (No KB)",
            "Accuracy": f"{acc_raw_mean:.4f} ± {acc_raw_std:.4f}",
            "F1-Macro": f"{f1_raw_mean:.4f} ± {f1_raw_std:.4f}",
            "ROC-AUC": f"{auc_raw_mean:.4f} ± {auc_raw_std:.4f}",
            "Accuracy_mean": acc_raw_mean,
            "F1_mean": f1_raw_mean,
            "AUC_mean": auc_raw_mean
        })

        # 2. Configurazione Enriched (Con KB Reasoning)
        scores_enr = cross_validate(model, X_enriched, y, cv=cv, scoring=scoring, n_jobs=-1)
        acc_enr_mean, acc_enr_std = np.mean(scores_enr["test_accuracy"]), np.std(scores_enr["test_accuracy"])
        f1_enr_mean, f1_enr_std = np.mean(scores_enr["test_f1_macro"]), np.std(scores_enr["test_f1_macro"])
        auc_enr_mean, auc_enr_std = np.mean(scores_enr["test_roc_auc"]), np.std(scores_enr["test_roc_auc"])

        results.append({
            "Model": model_name,
            "Configuration": "Enriched (With KB)",
            "Accuracy": f"{acc_enr_mean:.4f} ± {acc_enr_std:.4f}",
            "F1-Macro": f"{f1_enr_mean:.4f} ± {f1_enr_std:.4f}",
            "ROC-AUC": f"{auc_enr_mean:.4f} ± {auc_enr_std:.4f}",
            "Accuracy_mean": acc_enr_mean,
            "F1_mean": f1_enr_mean,
            "AUC_mean": auc_enr_mean
        })

    # Generazione DataFrame riassuntivo
    summary_df = pd.DataFrame(results)

    # Salvataggio CSV per la relazione
    os.makedirs(os.path.dirname(output_summary_path), exist_ok=True)
    summary_df.to_csv(output_summary_path, index=False)

    print("\n" + "="*80)
    print("                       TABELLA RIASSUNTIVA STUDIO DI ABLAZIONE")
    print("="*80)
    cols_display = ["Model", "Configuration", "Accuracy", "F1-Macro", "ROC-AUC"]
    print(summary_df[cols_display].to_string(index=False))
    print("="*80)
    print(f"\n[EVALUATE] Tabella salvata con successo in '{output_summary_path}'.")

if __name__ == "__main__":
    run_ablation_study()
