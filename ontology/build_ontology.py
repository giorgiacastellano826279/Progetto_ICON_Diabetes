import os
from owlready2 import (
    get_ontology, Thing, DataProperty, FunctionalProperty,
    Imp, default_world
)

def create_diabetes_ontology(output_path="ontology/diabetes_ontology.owl"):
    # 1. Inizializzazione Ontologia
    onto = get_ontology("http://example.org/diabetes_kbs.owl#")

    with onto:
        # --- CLASSI BASE ---
        class Patient(Thing):
            pass

        # --- DATA PROPERTIES ---
        class hasGlucose(DataProperty, FunctionalProperty):
            range = [float]

        class hasBMI(DataProperty, FunctionalProperty):
            range = [float]

        class hasBloodPressure(DataProperty, FunctionalProperty):
            range = [float]

        class hasAge(DataProperty, FunctionalProperty):
            range = [float]

        # --- CLASSI DERIVATE (CONCETTI CLINICI) ---
        class HyperglycemicPatient(Patient):
            pass

        class ObesePatient(Patient):
            pass

        class HypertensivePatient(Patient):
            pass

        class SeniorPatient(Patient):
            pass

        class HighRiskDiabetesProfile(Patient):
            pass

        # --- REGOLE DEDUTTIVE SWRL ---
        # Regola 1: Se glicemia >= 140 -> HyperglycemicPatient
        rule_hyper = Imp()
        rule_hyper.set_as_rule(
            "Patient(?p), hasGlucose(?p, ?g), greaterThanOrEqual(?g, 140.0) -> HyperglycemicPatient(?p)"
        )

        # Regola 2: Se BMI >= 30.0 -> ObesePatient
        rule_obese = Imp()
        rule_obese.set_as_rule(
            "Patient(?p), hasBMI(?p, ?b), greaterThanOrEqual(?b, 30.0) -> ObesePatient(?p)"
        )

        # Regola 3: Se Pressione >= 80.0 -> HypertensivePatient
        rule_hyp = Imp()
        rule_hyp.set_as_rule(
            "Patient(?p), hasBloodPressure(?p, ?bp), greaterThanOrEqual(?bp, 80.0) -> HypertensivePatient(?p)"
        )

        # Regola 4: Se Eta >= 50 -> SeniorPatient
        rule_senior = Imp()
        rule_senior.set_as_rule(
            "Patient(?p), hasAge(?p, ?a), greaterThanOrEqual(?a, 50.0) -> SeniorPatient(?p)"
        )

        # Regola 5 (Complessiva): Se un paziente e' contemporaneamente Obeso e Iperglicemico -> Profilo ad Alto Rischio
        rule_high_risk = Imp()
        rule_high_risk.set_as_rule(
            "HyperglycemicPatient(?p), ObesePatient(?p) -> HighRiskDiabetesProfile(?p)"
        )

    # 2. Salvataggio su file OWL
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    onto.save(file=output_path, format="rdfxml")
    print(f"[ONTOLOGY] Ontologia creata e salvata con successo in '{output_path}'.")

if __name__ == "__main__":
    create_diabetes_ontology()
