import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class XGBoostClassifier:
    def __init__(self, params=None):
        default_params = {
            'eval_metric': 'logloss',
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 3
        }
        if params:
            default_params.update(params)

        self.model = xgb.XGBClassifier(**default_params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)  

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        return accuracy, report

    def save_model(self, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        joblib.dump(self.model, output_path)

    def load_model(self, model_path):
        self.model = joblib.load(model_path)

    def get_model(self):
        return self.model
