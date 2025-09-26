# Use an official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for audio + ML libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run the chatbot
CMD ["streamlit", "run", "OMANI-Chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
