# app/config.py

import os  # Postgres bağlantısı için eklendi

MODEL_IMAGE_PATH = "outputs/model_w/U-Net/best_unet_resnet34_b2.pt"
# MODEL_TABULAR_PATH = "outputs/model_w/ML/xgb_mca_model_no_us_d.pkl"
MODEL_TABULAR_PATH = "outputs/model_w/ML/xgb_mca_model_no_us_d_filled.pkl"
# EXCEL_COLUMN_ORDER = "outputs/filtered_for_final_m.xlsx"
EXCEL_COLUMN_ORDER = "outputs/filtered_for_final_m_filled.xlsx"

EXCEL_PATH = "outputs/mm_per_px_with_diameter.xlsx"
IMG_SIZE = (384, 384)

# 📦 Veritabanı bağlantı URL'si (PostgreSQL)
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/appendicitis")
