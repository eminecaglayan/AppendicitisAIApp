# scripts/app/main.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.prediction import DiagnosisRequest
from app.models.image_model import ImageModel
from app.models.tabular_model import TabularModel
from app.utils.mca_transformer import MCATransformer
from app.config import EXCEL_PATH, MODEL_TABULAR_PATH  # 👈 sadece buradan al

import pandas as pd

# ✨ FastAPI uygulaması
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 Modelleri başlat
image_model = ImageModel()
tabular_model = TabularModel()
tabular_model.load_model(MODEL_TABULAR_PATH)

# ✅ Eğer MCA transformer .pkl dosyasını da config'e eklersen buraya da ekleyebilirsin
mca_transformer = MCATransformer(EXCEL_PATH, "outputs/model_w/ML/mca_transformer.pkl")

@app.get("/")
def read_root():
    return {"message": "Appendicitis Diagnosis API is working"}

@app.post("/predict")
def predict_diagnosis(data: DiagnosisRequest):
    features = data.features
    image_path = data.image_path

    # Görselden çap tahmini
    diameter = image_model.predict(image_path)

    features["Appendix_Diameter"] = diameter
    features["Appendix_Diameter_Categorized"] = "yes" if diameter > 6.0 else "no"

    input_df = mca_transformer.transform_single_input(features)
    prediction_label, prediction_proba = tabular_model.predict(input_df)

    return {
        "Diagnosis": prediction_label,
        "Confidence": prediction_proba,
        "Appendix_Diameter": round(diameter, 2),
        "Appendix_Diameter_Categorized": features["Appendix_Diameter_Categorized"]
    }
