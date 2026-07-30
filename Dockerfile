FROM python:3.11-slim

# System-Abhängigkeiten für GDAL/GEOS installieren
RUN apt-get update && apt-get install -y \
    libgeos-dev \
    gdal-bin \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements kopieren und installieren
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY app/ /app/

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]