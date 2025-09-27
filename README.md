# README.md

# 🇴🇲 OMANI-Chatbot

OMANI-Chatbot is a mental health–focused conversational assistant designed to provide supportive dialogue, intent recognition, and safe responses.  
It integrates **speech-to-text (STT)**, **text-to-speech (TTS)**, **retrieval-augmented generation (RAG)**, and **emotion detection** into a single pipeline.

---

## 📂 Project Structure
```

OMANI-Chatbot.py         # Main entrypoint
app/                     # Core application logic
data/                    # Knowledge base + Chroma vector database
documentation/           # Architecture diagrams and reports
tests/                   # Unit tests, audio samples, transcripts
requirements.txt         # Python dependencies

````

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/russelljeffrey/Omani-therapist-voice.git
````

### 2. Create virtual environment & install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Option A: Run Locally

```bash
streamlit run OMANI-Chatbot.py
```

By default, the Streamlit UI will launch on **[http://localhost:8501](http://localhost:8501)**

---

### Option B: Run with Docker

1. Build the Docker image:

```bash
docker build -t omani-chatbot .
```

2. Run the container:

```bash
docker run -p 8501:8501 omani-chatbot
```

Open your browser at **[http://localhost:8501](http://localhost:8501)** to use the chatbot.

---

## 📖 Documentation

See the `documentation/` folder for:

* `architecture.md` → System overview
* `safety_protocol.md` → Safety design
* `future_roadmap.md` → Planned improvements
* `wer_report.md` → Performance metrics

---

## 🧪 Testing

Run the tests with:

```bash
python -m pytest -s -v tests/
```

---

## 🛡️ Safety Note

This project is for **demo purposes**.
It is **not a substitute for professional mental health care**. If someone is in crisis, they should seek immediate professional support.

---
