from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def get_models():
    """
    Restituisce un dizionario contenente i modelli da valutare.
    I modelli sensibili alla scala includono uno StandardScaler nella pipeline.
    """
    models = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=42))
        ]),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=4,
            random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
    }
    return models
