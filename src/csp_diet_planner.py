import pandas as pd

# Database degli alimenti disponibili con valori nutrizionali per porzione
FOOD_DB = {
    "colazione": [
        {"nome": "Yogurt Greco e Avena", "calorie": 250, "carboidrati": 25},
        {"nome": "Uova strapazzate e pane integrale", "calorie": 300, "carboidrati": 15},
        {"nome": "Biscotti e Latte Intero", "calorie": 350, "carboidrati": 55},
        {"nome": "Frullato proteico ai frutti di bosco", "calorie": 220, "carboidrati": 18}
    ],
    "pranzo": [
        {"nome": "Insalata di Quinoa con Pollo e Verdure", "calorie": 450, "carboidrati": 35},
        {"nome": "Riso integrale con Salmone e Zucchine", "calorie": 520, "carboidrati": 40},
        {"nome": "Pasta al pomodoro e formaggio", "calorie": 600, "carboidrati": 75},
        {"nome": "Zuppa di legumi con crostini integrali", "calorie": 400, "carboidrati": 45}
    ],
    "cena": [
        {"nome": "Filetto di Merluzzo al vapore con Spinaci", "calorie": 350, "carboidrati": 10},
        {"nome": "Petto di Tacchino alla griglia con Broccoli", "calorie": 380, "carboidrati": 12},
        {"nome": "Pizza margherita", "calorie": 750, "carboidrati": 90},
        {"nome": "Tofu saltato con verdure miste", "calorie": 320, "carboidrati": 15}
    ]
}

class DietCSP:
    def __init__(self, is_hyperglycemic, is_obese):
        self.variables = ["colazione", "pranzo", "cena"]
        self.domains = FOOD_DB

        # Calibrazione dei vincoli in base alle inferenze della KB
        # Se iperglicemico, tetto rigido sui carboidrati giornalieri
        self.max_carbs = 75.0 if is_hyperglycemic else 160.0
        # Se obeso, restrizione calorica target
        self.max_calories = 1400.0 if is_obese else 2000.0

    def is_consistent(self, assignment):
        """Verifica la consistenza parziale o totale dei vincoli del CSP."""
        tot_carbs = sum(item["carboidrati"] for item in assignment.values())
        tot_cal = sum(item["calorie"] for item in assignment.values())

        if tot_carbs > self.max_carbs:
            return False
        if tot_cal > self.max_calories:
            return False
        return True

    def backtrack(self, assignment={}):
        """Algoritmo sistematico di Backtracking Search per CSP."""
        if len(assignment) == len(self.variables):
            return assignment

        var = self.variables[len(assignment)]
        for value in self.domains[var]:
            assignment[var] = value
            if self.is_consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]

        return None

def plan_diet_for_patient(patient_row):
    is_hyper = bool(patient_row.get("KB_Hyperglycemic", 0))
    is_obese = bool(patient_row.get("KB_Obese", 0))
    
    csp = DietCSP(is_hyperglycemic=is_hyper, is_obese=is_obese)
    solution = csp.backtrack({})
    return solution, csp.max_carbs, csp.max_calories

if __name__ == "__main__":
    # Test su un paziente diabetico critico
    print("[CSP] Esempio di pianificazione per Paziente ad Alto Rischio (Iperglicemico + Obeso):")
    sample_patient = {"KB_Hyperglycemic": 1, "KB_Obese": 1}
    sol, max_c, max_cal = plan_diet_for_patient(sample_patient)
    
    if sol:
        tot_c = sum(v["carboidrati"] for v in sol.values())
        tot_k = sum(v["calorie"] for v in sol.values())
        print(f"Vincoli attivi: Max Carboidrati={max_c}g, Max Calorie={max_cal} kcal")
        print(f"Soluzione trovata (Tot Carb={tot_c}g, Tot Cal={tot_k} kcal):")
        for meal, dish in sol.items():
            print(f" - {meal.capitalize()}: {dish['nome']} (Carb: {dish['carboidrati']}g, Cal: {dish['calorie']} kcal)")
    else:
        print("Nessun piano dietetico soddisfa simultaneamente tutti i vincoli.")
