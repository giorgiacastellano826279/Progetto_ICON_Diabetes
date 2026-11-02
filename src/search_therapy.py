import heapq
import math

class MedicalState:
    def __init__(self, glucose, bmi, blood_pressure):
        self.glucose = round(glucose, 1)
        self.bmi = round(bmi, 1)
        self.blood_pressure = round(blood_pressure, 1)

    def is_goal(self):
        # Obiettivo terapeutico: rientro entro soglie di sicurezza fisiologica
        return self.glucose <= 120.0 and self.bmi <= 27.0 and self.blood_pressure <= 78.0

    def heuristic(self):
        # Euristica h(n): distanza ponderata verso i target clinici
        d_g = max(0.0, self.glucose - 120.0) / 20.0
        d_b = max(0.0, self.bmi - 27.0) / 2.0
        d_bp = max(0.0, self.blood_pressure - 78.0) / 5.0
        return math.sqrt(d_g**2 + d_b**2 + d_bp**2)

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __eq__(self, other):
        return (self.glucose, self.bmi, self.blood_pressure) == (other.glucose, other.bmi, other.blood_pressure)

    def __hash__(self):
        return hash((self.glucose, self.bmi, self.blood_pressure))

ACTIONS = [
    {"name": "Dieta Ipoglucidica", "delta_g": -25.0, "delta_b": -1.5, "delta_bp": -2.0, "cost": 3.0},
    {"name": "Esercizio Fisico Aerobico", "delta_g": -15.0, "delta_b": -1.0, "delta_bp": -6.0, "cost": 2.5},
    {"name": "Terapia con Metformina", "delta_g": -35.0, "delta_b": -0.5, "delta_bp": 0.0, "cost": 4.0},
    {"name": "Gestione Stress e Igiene Sonno", "delta_g": -5.0, "delta_b": 0.0, "delta_bp": -4.0, "cost": 1.5}
]

def a_star_therapy_search(initial_state):
    # Coda di priorita': memorizza tuple (f_score, g_cost, state, path)
    frontier = []
    initial_h = initial_state.heuristic()
    heapq.heappush(frontier, (initial_h, 0.0, initial_state, []))

    explored = set()
    nodes_expanded = 0

    while frontier:
        f, g, current, path = heapq.heappop(frontier)

        if current.is_goal():
            return path, g, nodes_expanded, current

        if current in explored:
            continue
        explored.add(current)
        nodes_expanded += 1

        for act in ACTIONS:
            next_g = max(80.0, current.glucose + act["delta_g"])
            next_b = max(20.0, current.bmi + act["delta_b"])
            next_bp = max(65.0, current.blood_pressure + act["delta_bp"])

            next_state = MedicalState(next_g, next_b, next_bp)
            if next_state not in explored:
                step_cost = act["cost"]
                new_g = g + step_cost
                new_f = new_g + next_state.heuristic()
                heapq.heappush(frontier, (new_f, new_g, next_state, path + [(act["name"], next_state)]))

    return None, None, nodes_expanded, None

if __name__ == "__main__":
    # Test su un paziente tipico con valori patologici
    start = MedicalState(glucose=160.0, bmi=33.5, blood_pressure=86.0)
    print(f"[SEARCH A*] Stato iniziale: Glucosio={start.glucose}, BMI={start.bmi}, Pressione={start.blood_pressure}")
    print("[SEARCH A*] Esecuzione algoritmo A* per identificare il piano terapeutico a costo minimo...")

    plan, total_cost, expanded, final_state = a_star_therapy_search(start)

    if plan:
        print(f"\n[SEARCH A*] Piano terapeutico ottimo identificato in {len(plan)} passi (Costo totale: {total_cost:.2f}, Nodi espansi: {expanded}):")
        for i, (action_name, st) in enumerate(plan, 1):
            print(f"  Step {i}: {action_name} -> [Glicemia: {st.glucose}, BMI: {st.bmi}, Pressione: {st.blood_pressure}]")
        print(f"Stato finale raggiunto: Glucosio={final_state.glucose}, BMI={final_state.bmi}, Pressione={final_state.blood_pressure}")
    else:
        print("Nessun percorso terapeutico trovato.")
