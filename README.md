# Comprehensive AI Clinical Decision Support System (CDSS)

This repository contains a fully self‑contained example of an AI‑powered clinical decision support system inspired by the 2022 AHA/ACC/HFSA heart failure guidelines.  Unlike the simple skeleton provided earlier, this project includes a complete retrieval component, an extensible backend, a conversational frontend and containerized deployment.  It is designed to be easy to run locally, to extend for your own use cases and to demonstrate modern AI techniques to colleagues or employers.

## Highlights

* **Evidence retrieval** – The backend includes a simple retrieval engine built with `scikit‑learn`'s TF‑IDF vectorizer.  It indexes guideline documents and returns the most relevant section given a free‑text query (formed from patient symptoms).  This can be replaced with a more sophisticated retrieval‑augmented generation pipeline using large language models and vector databases.
* **REST API** – The service exposes two endpoints via FastAPI:
  * `POST /recommendation` – Accepts structured patient data (ID, age, gender and symptoms) and returns a recommendation card with the top guideline snippet.
  * `POST /chat` – Supports free‑form queries for ad‑hoc questions about the guidelines.
* **Interactive frontend** – A Streamlit app provides both a chatbot interface and a structured form for submitting patient data.  Conversations are stored in the session state so the chat history is visible as you interact.
* **Containerized deployment** – Dockerfiles and a docker‑compose configuration are included.  Running `docker‑compose up` will build and start the backend and frontend services.

## Directory Structure

```
cdss_comprehensive/
├── data/
│   └── guidelines/
│       └── hf_guideline.txt
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── rag.py
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
└── .gitignore
```

### Guidelines

The `data/guidelines/hf_guideline.txt` file contains a few excerpts from the heart failure guideline.  You can add more documents or replace the file entirely.  Each paragraph separated by a blank line will be treated as a separate section in the retrieval index.

### Running locally

1. Install Docker Desktop or the Docker Engine.
2. Clone this repository and navigate into the project directory.
3. Build and start the services:

   ```bash
   docker-compose up --build
   ```

4. Open the Streamlit frontend at [http://localhost:8501](http://localhost:8501).  Use the chatbot to ask guideline‑related questions or fill in the form to get a recommendation for a patient.

### Extending the retrieval engine

The retrieval engine implemented in `backend/rag.py` uses TF‑IDF to illustrate the concept.  To integrate a true retrieval‑augmented generation pipeline, you can:

* Replace the `TfidfVectorizer` with a large‑language‑model embedding, such as [OpenAIEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html) or [HuggingFaceEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.huggingface.HuggingFaceEmbeddings.html).
* Swap the simple cosine similarity search for a vector database like Chroma or FAISS.
* Use a language model (e.g. Groq or OpenAI) via LangChain’s `RetrievalQA` chain to generate final answers conditioned on the retrieved snippets.

If you add these enhancements you will also need to supply API keys for the embedding and LLM providers.  Store secrets in a `.env` file and load them in `rag.py`.

### Disclaimer

This project is a demonstration and is **not** intended for clinical use.  Always consult a licensed healthcare professional for real medical advice.
