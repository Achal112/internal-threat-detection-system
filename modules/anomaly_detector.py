from sklearn.ensemble import IsolationForest
import pandas as pd


class AnomalyDetector:

    def __init__(self):

        self.model = IsolationForest(
            contamination=0.15,
            random_state=42
        )

    def train(self, data):

        df = pd.DataFrame(data)

        self.model.fit(df)

    def predict(self, sample):

        df = pd.DataFrame([sample])

        prediction = self.model.predict(df)[0]

        if prediction == -1:
            return "Anomaly"

        return "Normal"