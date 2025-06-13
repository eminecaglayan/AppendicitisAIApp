# Apandisit Tanısında Yapay Zeka Destekli Karar Sistemi

Bu proje, ultrason görüntüleri ve hasta bilgilerini kullanarak apandisit teşhisine yardımcı olan bir yapay zeka uygulamasıdır.

## Özellikler

- **Ultrason Görüntü Analizi**: U-Net tabanlı derin öğrenme modeli ile apandis çapı tahmini
- **Hasta Bilgileri Analizi**: XGBoost modeli ile klinik parametrelerin değerlendirilmesi
- **Web Arayüzü**: Streamlit ile kullanıcı dostu arayüz
- **Veritabanı**: PostgreSQL ile hasta geçmişi ve tanı kayıtları
- **Docker**: Kolay kurulum ve çalıştırma

## Sistem Mimarisi

- **Frontend**: Streamlit (5 sayfa: Anasayfa, Teşhis, Geçmiş, Veri Bilgisi, Geliştiriciler)
- **Backend**: FastAPI
- **Veritabanı**: PostgreSQL
- **AI Modelleri**: U-Net (görüntü segmentasyonu) + XGBoost (sınıflandırma)
- **Konteynerizasyon**: Docker & Docker Compose

## Kurulum ve Çalıştırma

### Gereksinimler
- Docker Desktop
- Git

### 1. Projeyi İndirin
```bash
git clone https://github.com/KULLANICI_ADINIZ/AppendicitisAIApp.git
cd AppendicitisAIApp
```

### 2. Docker ile Çalıştırın
```bash
# Tüm servisleri başlat
docker compose up --build -d

# Veritabanı tablolarını oluştur
docker exec appendicitisaiapp-api-1 alembic upgrade head
```

### 3. Uygulamaya Erişin
- **Streamlit Arayüzü**: http://localhost:8501
- **FastAPI Dokümantasyonu**: http://localhost:8000/docs
