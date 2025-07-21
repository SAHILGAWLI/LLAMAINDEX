# LlamaIndex Pinecone Query API

This project is a FastAPI-based server that provides endpoints for querying and chatting with documents stored in a Pinecone vector database using LlamaIndex and OpenAI LLMs.

## Features
- Query documents using semantic search
- Multi-user chat with context and memory
- Streaming responses for chat endpoints

## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies

## Local Development
1. Clone the repository and navigate to the project directory.
2. Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_key
   PINECONE_API_KEY=your_pinecone_key
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server locally:
   ```bash
   uvicorn query_api:app --reload
   ```

## Deployment (Render)
1. Push your code to a GitHub repository.
2. On [Render](https://render.com), create a new **Web Service** and connect your repo.
3. Set the following in Render's dashboard:
   - **Start Command:**
     ```
     uvicorn query_api:app --host 0.0.0.0 --port $PORT
     ```
   - **Environment Variables:**
     - `OPENAI_API_KEY` (required)
     - `PINECONE_API_KEY` (required)
4. Deploy and test your endpoints at the provided Render URL.

## .gitignore
Your `.gitignore` should contain at least:
```
.env
__pycache__/
```

## Endpoints
- `POST /query`
- `POST /chat`
- `POST /citizen_chat`
- `POST /citizen_chat_stream`

See `query_api.py` for details on request/response formats.

---

Feel free to open issues or PRs for improvements!
