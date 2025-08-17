# AI Clinical Decision Support System (AI‑CDSS)

This repository contains a comprehensive example of an AI‑powered clinical decision support system inspired by the 2022 AHA/ACC/HFSA heart failure guidelines.  It features a retrieval component for evidence‑based answers, a FastAPI backend, a Streamlit frontend, and containerized deployment.  The project serves as both a learning resource and a foundation for building your own healthcare applications.

## Highlights

* **Evidence retrieval** – The backend implements a retrieval engine using `scikit‑learn`'s TF‑IDF vectorizer to index guideline documents and return the most relevant sections for a given free‑text query (derived from patient symptoms).  You can later swap this for a full retrieval‑augmented generation pipeline powered by large language models and vector stores.
* **REST API** – The FastAPI backend exposes two endpoints:
  * `POST /recommendation` – Accepts structured patient data (ID, age, gender, symptoms) and returns a guideline recommendation card.
  * `POST /chat` – Handles free‑form questions about the guidelines.
* **Interactive frontend** – A Streamlit app lets users submit structured patient data or chat with the guidelines.  Conversations persist in session state so history stays visible.
* **Deployed demo** – The project is live!  Access the deployed services:
  * **Backend (FastAPI)** – <https://ai-cdss.onrender.com>
  * **Frontend (Streamlit)** – <https://ai-cdss-8gyum8mhjjnkmkoxthbg.streamlit.app>
* **Containerized deployment** – Dockerfiles and a docker‑compose configuration allow easy local deployment.  Running `docker-compose up` will build and start both services.

## Directory Structure

```text
cdss_comprehensive/
├── data/
│   └── guidelines/
│       └── hf_guideline.txt
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── rag.py
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
└── .gitignore
```

### Guidelines

The `data/guidelines/hf_guideline.txt` file contains a few excerpts from the heart failure guideline.  You can add more documents or replace the file entirely; paragraphs separated by a blank line are treated as separate sections in the retrieval index.

### Running locally

1. Install Docker Desktop or the Docker Engine.
2. Clone this repository and navigate into the project directory.
3. Build and start the services:

   ```bash
   docker-compose up --build
   ```

4. Open the Streamlit frontend.

    - For local development (Docker Compose), visit `http://localhost:8501`.
    - For the hosted demo, visit <https://ai-cdss-8gyum8mhjjnkmkoxthbg.streamlit.app>.

    Use the chatbot to ask guideline‑related questions or fill in the form to get a recommendation for a patient.  The backend will be available locally at `http://localhost:8000` when running with Docker Compose.

### Extending the retrieval engine

To upgrade the proof‑of‑concept TF‑IDF retrieval engine to a true retrieval‑augmented generation pipeline, you can:

* Replace the `TfidfVectorizer` with a large‑language‑model embedding, such as [OpenAIEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html) or [HuggingFaceEmbeddings](https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.huggingface.HuggingFaceEmbeddings.html).
* Swap the simple cosine similarity search for a vector database like Chroma or FAISS.
* Use a language model (e.g. Groq or OpenAI) via LangChain’s `RetrievalQA` chain to generate final answers conditioned on the retrieved snippets.

If you add these enhancements you will need to supply API keys for the embedding and LLM providers.  Store secrets in a `.env` file and load them in `rag.py`.

### Disclaimer

This project is a demonstration and is **not** intended for clinical use.  Always consult a licensed healthcare professional for real medical advice.