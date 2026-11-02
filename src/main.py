from preprocess import load_and_clean_data
from reasoner_bridge import enrich_dataset_with_reasoning
from evaluate import run_ablation_study
from csp_diet_planner import plan_diet_for_patient
from search_therapy import MedicalState, a_star_therapy_search
import pandas as pd

def main():
    print("="*80)
    print(" SISTEMA KBS NEURO-SIMBOLICO PER LA GESTIONE DEL RISCHIO DIABETE")
    print("="*80)

    # 1. Pipeline dati & ontologia
    df_clean = load_and_clean_data()
    df_enr = enrich_dataset_with_reasoning()

    # 2. Selezione di un paziente campione identificato ad alto rischio dalla KB
    high_risk_patients = df_enr[df_enr["KB_HighRiskProfile"] == 1]
    sample = high_risk_patients.iloc[0]
    print(f"\n[ANALISI CLINICA] Paziente selezionato: Età={sample['Age']}, Glucosio={sample['Glucose']}, BMI={sample['BMI']}, Pressione={sample['BloodPressure']}")
    print(f"Stato Dedotto dalla KB: Hyperglycemic={sample['KB_Hyperglycemic']}, Obese={sample['KB_Obese']}, HighRiskProfile={sample['KB_HighRiskProfile']}")

    # 3. Pianificazione Dieta tramite CSP (Ch. 4)
    print("\n--- [MODULO CSP] Pianificazione Dieta Vincolata ---")
    diet, max_c, max_cal = plan_diet_for_patient(sample)
    if diet:
        print(f"Dieta generata con vincoli (Max Carb: {max_c}g, Max Cal: {max_cal} kcal):")
        for meal, dish in diet.items():
            print(f"  * {meal.capitalize()}: {dish['nome']} (Carb: {dish['carboidrati']}g, Cal: {dish['calorie']} kcal)")

    # 4. Ricerca Piano Terapeutico Ottimo tramite A* (Ch. 3)
    print("\n--- [MODULO RICERCA A*] Percorso di Normalizzazione Clinica ---")
    st_init = MedicalState(glucose=sample['Glucose'], bmi=sample['BMI'], blood_pressure=sample['BloodPressure'])
    plan, cost, nodes, final_st = a_star_therapy_search(st_init)
    if plan:
        print(f"Piano A* generato in {len(plan)} step (Costo totale: {cost}, Nodi espansi: {nodes}):")
        for idx, (act, st) in enumerate(plan, 1):
            print(f"  Step {idx}: {act} -> [Glicemia: {st.glucose}, BMI: {st.bmi}, Pressione: {st.blood_pressure}]")

    print("\n" + "="*80)
    print(" Pipeline completata con successo.")
    print("="*80)

if __name__ == "__main__":
    main()
