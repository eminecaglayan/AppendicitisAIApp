FROM python:3.11-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Sistem kütüphanelerini yükle (OpenCV ve diğerleri için)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
 && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Kodları ve verileri kopyala
COPY scripts/ scripts/
COPY scripts/models/ models/
COPY scripts/streamlit_app/ streamlit_app/
COPY data/ data/
COPY outputs/ outputs/

# Varsayılan komut (docker-compose override eder)
CMD ["echo", "✅ Docker imajı hazır. `docker-compose up` ile başlatabilirsiniz."]
