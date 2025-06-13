# scripts/app/models/tabular_model.py

import pandas as pd
from models.ML.xgboost_classifier import XGBoostClassifier

class TabularModel:
    def __init__(self):
        self.model = None
        self.expected_features = None

    def load_model(self, path: str):
        """XGBoost modelini yükler."""
        self.model = XGBoostClassifier()
        self.model.load_model(path)

        # Modelde beklenen öznitelik isimleri varsa kaydet
        if hasattr(self.model.model, "feature_names_in_"):
            self.expected_features = list(self.model.model.feature_names_in_)

    def predict(self, input_df: pd.DataFrame):
        """Tek satırlık tabular veriden tahmin yapar."""
        if self.model is None:
            raise ValueError("⚠️ Model yüklenmedi.")
        
        # Özellik sırasını garantiye al
        if self.expected_features:
            input_df = input_df[self.expected_features]

        # Tahmin et
        y_pred = self.model.predict(input_df)[0]
        y_proba = self.model.predict_proba(input_df)[0][1]

        label = "appendicitis" if y_pred == 1 else "no appendicitis"
        return label, round(float(y_proba), 4)
