# 🏛️ Legal Platform ReAct Agent API

A sophisticated FastAPI-based legal intelligence platform powered by **LlamaIndex ReAct Agents**, **Pinecone vector database**, and **OpenAI LLMs**. This system provides intelligent analysis for legal compliance, case research, and document management.

## 🚀 Key Features

### **Multi-Agent Intelligence System**
- **🔍 ReAct Agents**: Reasoning + Acting paradigm for intelligent decision making
- **📋 Compliance Agent**: FHIR compliance analysis and checklist generation
- **⚖️ Legal Agent**: BNS law research with severity classification
- **📄 Document Agent**: Intelligent document analysis and categorization
- **📁 Case Agent**: Similar case discovery and precedent analysis

### **Advanced Capabilities**
- **🎯 Intelligent Grid Population**: AI-powered data population for 4-grid dashboard
- **🔄 Real-time Streaming**: WebSocket support for live updates
- **🧠 Multi-Document RAG**: Semantic search across legal knowledge bases
- **📊 Structured Responses**: Pydantic models for type-safe API responses
- **⚡ Parallel Processing**: Async agent execution for optimal performance

### **Legal Domain Expertise**
- **FHIR Compliance**: Medical-legal compliance tracking and validation
- **BNS Law Database**: Bharatiya Nyaya Sanhita legal reference system
- **Case Precedents**: Historical case analysis and similarity scoring
- **Document Intelligence**: Legal document classification and summarization

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

5. Test the API using the enhanced tester:
   ```bash
   streamlit run agent_tester.py
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

## 🔗 API Endpoints

### **🎯 ReAct Agent Endpoints**

#### Master Dashboard Population
```http
POST /dashboard/populate
Content-Type: application/json

{
  "case_id": "CASE-2024-001",
  "case_context": "Medical malpractice case involving surgical complications",
  "user_role": "analyst",
  "jurisdiction": "Maharashtra"
}
```

#### Individual Grid Endpoints
- **📋 Compliance Grid**: `POST /grid/compliance`
- **⚖️ Laws Grid**: `POST /grid/laws`
- **📄 Documents Grid**: `POST /grid/documents`
- **📁 Cases Grid**: `POST /grid/cases`

#### Real-time Streaming
- **🔄 WebSocket**: `WS /dashboard/stream`

### **💬 Original Chat Endpoints**
- **Single Query**: `POST /query`
- **Multi-turn Chat**: `POST /chat`
- **Citizen Chat**: `POST /citizen_chat`
- **Streaming Chat**: `POST /citizen_chat_stream`

### **🏥 Health & Status**
- **Health Check**: `GET /health`
- **Agent Status**: `GET /agents/status`
- **API Info**: `GET /`

## 📚 Usage Examples

### Dashboard Population
```python
import requests

response = requests.post("http://localhost:8000/dashboard/populate", json={
    "case_id": "CASE-2024-001",
    "case_context": "Medical malpractice case involving surgical complications at City Hospital",
    "user_role": "analyst",
    "jurisdiction": "Maharashtra"
})

dashboard_data = response.json()
print(f"Compliance: {dashboard_data['grid_1_compliance']['percentage']}% complete")
print(f"Found {len(dashboard_data['grid_2_laws']['laws'])} relevant laws")
```

### Individual Grid Testing
```python
# Test compliance grid
response = requests.post("http://localhost:8000/grid/compliance", json={
    "case_id": "CASE-2024-001",
    "context": "FHIR compliance for medical case"
})

compliance = response.json()
for item in compliance['checklist_items']:
    status = "✅" if item['status'] == 'completed' else "⏳"
    print(f"{status} {item['item']}")
```

### WebSocket Streaming
```javascript
const ws = new WebSocket('ws://localhost:8000/dashboard/stream');

ws.onopen = function() {
    ws.send(JSON.stringify({
        "case_id": "CASE-2024-001",
        "case_context": "Medical malpractice case"
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(`Grid ${data.grid}: ${data.status}`);
};
```

## 🧪 Testing

### Using the Enhanced Tester
1. Start the API server:
   ```bash
   uvicorn query_api:app --reload
   ```

2. Launch the test interface:
   ```bash
   streamlit run agent_tester.py
   ```

3. Test different sections:
   - **🏠 Dashboard Population**: Test the master endpoint
   - **📋 Individual Grids**: Test each grid separately
   - **🔄 Real-time Streaming**: WebSocket testing
   - **💬 Original Chat APIs**: Legacy chat endpoints
   - **🏥 Health & Status**: System health checks

### Using the Original Tester
```bash
streamlit run api_tester.py
```

## 🏗️ Architecture

### **Agent System**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │  Agent Manager   │    │  ReAct Agents   │
│   Endpoints     │───▶│  Orchestrator    │───▶│  - Compliance   │
│                 │    │                  │    │  - Legal        │
└─────────────────┘    └──────────────────┘    │  - Documents    │
                                                │  - Cases        │
                                                └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  LlamaIndex RAG  │
                    │  + Pinecone DB   │
                    └──────────────────┘
```

### **Data Flow**
1. **Request**: Client sends case context to dashboard endpoint
2. **Agent Dispatch**: Agent manager runs 4 specialized agents in parallel
3. **RAG Processing**: Each agent queries relevant knowledge bases
4. **Response Parsing**: Raw agent outputs parsed into structured responses
5. **Grid Population**: Frontend receives structured data for each grid

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=quickstart
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

### Agent Configuration
Agents can be customized in `agents.py`:
- **System prompts** for specialized behavior
- **Tool selection** for different knowledge bases
- **Response modes** for different output formats
- `POST /citizen_chat_stream`

See `query_api.py` for details on request/response formats.

---

Feel free to open issues or PRs for improvements!
