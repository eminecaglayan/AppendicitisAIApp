from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# Geçmiş Hastalar tablosu


class Patient(Base):
    __tablename__ = "gecmis_hastalar"

    id = Column(Integer, primary_key=True, index=True)
    Sex = Column(String, nullable=False)
    Migratory_Pain = Column(String, nullable=False)
    Lower_Right_Abd_Pain = Column(String, nullable=False)
    Contralateral_Rebound_Tenderness = Column(String, nullable=False)
    Coughing_Pain = Column(String, nullable=False)
    Nausea = Column(String, nullable=False)
    Loss_of_Appetite = Column(String, nullable=False)
    Neutrophilia = Column(String, nullable=False)
    Ketones_in_Urine = Column(String, nullable=False)
    RBC_in_Urine = Column(String, nullable=False)
    WBC_in_Urine = Column(String, nullable=False)
    Dysuria = Column(String, nullable=False)
    Stool = Column(String, nullable=False)
    Peritonitis = Column(String, nullable=False)
    Psoas_Sign = Column(String, nullable=False)
    Ipsilateral_Rebound_Tenderness = Column(String, nullable=False)
    Age = Column(Float, nullable=False)
    BMI = Column(Float, nullable=False)
    Height = Column(Float, nullable=False)
    Weight = Column(Float, nullable=False)
    Length_of_Stay = Column(Float, nullable=False)
    Body_Temperature = Column(Float, nullable=False)
    WBC_Count = Column(Float, nullable=False)
    Neutrophil_Percentage = Column(Float, nullable=False)
    RBC_Count = Column(Float, nullable=False)
    Hemoglobin = Column(Float, nullable=False)
    RDW = Column(Float, nullable=False)
    Thrombocyte_Count = Column(Float, nullable=False)
    CRP = Column(Float, nullable=False)

    # İlişkiler
    diagnoses = relationship("Diagnosis", back_populates="patient")

    def to_dict(self):
        # Tüm sütunları sözlüğe çevir
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Geçmiş Tanılar tablosu
class Diagnosis(Base):
    __tablename__ = "gecmis_tanilar"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey(
        "gecmis_hastalar.id"), nullable=False)
    Appendix_Diameter = Column(Float, nullable=False)
    Appendix_Diameter_Categorized = Column(String, nullable=False)
    Diagnosis = Column(String, nullable=False)
    Confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # İlişkiler
    patient = relationship("Patient", back_populates="diagnoses")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
