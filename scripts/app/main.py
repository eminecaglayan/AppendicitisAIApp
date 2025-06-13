# scripts/app/main.py

from app.config import EXCEL_PATH, MODEL_TABULAR_PATH  # sadece buradan al
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas.prediction import DiagnosisRequest
from app.models.image_model import ImageModel
from app.models.tabular_model import TabularModel
from app.utils.mca_transformer import MCATransformer
from app.db.session import get_db
from app.db.models import Patient, Diagnosis


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
mca_transformer = MCATransformer(
    EXCEL_PATH, "outputs/model_w/ML/mca_transformer.pkl")


@app.get("/")
def read_root():
    return {"message": "Appendicitis Diagnosis API is working"}


@app.post("/predict")
def predict_diagnosis(data: DiagnosisRequest, db: Session = Depends(get_db)):
    features = data.features
    image_path = data.image_path
    original_features = features.copy()

    # Görselden çap tahmini
    diameter = image_model.predict(image_path)
    # Convert numpy types to Python native types for database compatibility
    diameter = float(diameter)

    features["Appendix_Diameter"] = diameter
    features["Appendix_Diameter_Categorized"] = "yes" if diameter > 6.0 else "no"

    input_df = mca_transformer.transform_single_input(features)
    prediction_label, prediction_proba = tabular_model.predict(input_df)
    # Convert numpy types to Python native types
    prediction_proba = float(prediction_proba)

    # Veritabanına kayıt
    hasta = Patient(**original_features)
    db.add(hasta)
    db.flush()  # ID yaratmak için
    tani = Diagnosis(
        patient_id=hasta.id,
        Appendix_Diameter=float(round(diameter, 2)),
        Appendix_Diameter_Categorized=features["Appendix_Diameter_Categorized"],
        Diagnosis=str(prediction_label),
        Confidence=float(prediction_proba)
    )
    db.add(tani)
    db.commit()

    return {
        "Diagnosis": prediction_label,
        "Confidence": prediction_proba,
        "Appendix_Diameter": round(diameter, 2),
        "Appendix_Diameter_Categorized": features["Appendix_Diameter_Categorized"]
    }


@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    """Geçmiş hastalar ve tanılar listesini döner"""
    hastalar = db.query(Patient).all()
    tanilar = db.query(Diagnosis).all()
    return {
        "gecmis_hastalar": [h.to_dict() for h in hastalar],
        "gecmis_tanilar": [t.to_dict() for t in tanilar]
    }
