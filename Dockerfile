FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies required for audio processing and media handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsndfile1 \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY ./voicechat/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --require-hashes=false -r /app/requirements.txt

# Copy application source
COPY ./voicechat /app

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the Streamlit app
CMD ["streamlit", "run", "rag_voice.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
