# 🤖 Test Case Generator

**Autonomous test case generation powered by Claude Agent SDK**

A full-stack application that automatically generates comprehensive test cases from feature descriptions and JIRA acceptance criteria using Claude's agentic capabilities.

[![Claude Agent SDK](https://img.shields.io/badge/Claude-Agent%20SDK-blue)](https://docs.anthropic.com/agent-sdk)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue)](https://react.dev)

---

## 🌟 Features

### Backend (Microservice)
- 🤖 **Autonomous Agent** - Claude Agent SDK with self-directed agentic loop
- 🔧 **Custom MCP Tools** - In-process validation and structuring tools
- 🔄 **Self-Correcting** - Agent validates and fixes its own output
- 📊 **Structured Output** - Guaranteed valid JSON responses
- 🔌 **JIRA Integration** - Fetch requirements from JIRA automatically
- 📝 **Manual Input** - Generate without JIRA
- 🐳 **Docker Ready** - Containerized deployment
- 🚀 **Production Ready** - Async FastAPI, error handling, logging

### Frontend (React UI)
- 🎨 **Modern Design** - Gradient UI with smooth animations
- 🔄 **Dual Mode** - Manual input or JIRA issue key
- ⚡ **Real-time** - Live test case generation with loading states
- 📥 **Export** - Download test cases as JSON
- 📱 **Responsive** - Works on all devices
- 🎯 **Customizable** - Configure test types and options

---

## 📸 Screenshots

[Add screenshots here after deployment]

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              React Frontend (Port 5173)             │
│         Modern UI for Test Case Generation          │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────┐
│          FastAPI Microservice (Port 8000)           │
│         Claude Agent SDK Autonomous Agent           │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────┐           │
│  │    TestCaseGeneratorAgent            │           │
│  │    (Claude Agent SDK)                │           │
│  └───────────┬──────────────────────────┘           │
│              │                                       │
│              ▼                                       │
│  ┌──────────────────────────────────────┐           │
│  │   Autonomous Agentic Loop            │           │
│  │  1. Analyze requirements             │           │
│  │  2. Generate test cases              │           │
│  │  3. Validate (MCP tool)              │           │
│  │  4. Structure output (MCP tool)      │           │
│  └──────────────────────────────────────┘           │
│                                                      │
│  ┌──────────────────────────────────────┐           │
│  │   Custom SDK MCP Tools               │           │
│  │  • validate_test_case                │           │
│  │  • structure_test_cases              │           │
│  └──────────────────────────────────────┘           │
│                                                      │
└─────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         External Integrations                       │
│  • Anthropic Claude API (Sonnet 4.5)               │
│  • JIRA API (Artemis Health)                       │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional)
- Anthropic API key
- JIRA credentials (optional)

### Local Development

#### 1. Clone Repository
```bash
git clone https://github.com/ramki271/test-generator.git
cd test-generator
```

#### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run backend
python -m uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000

#### 3. Setup Frontend
```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Update VITE_API_URL if needed

# Run frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

### Using Docker

```bash
# Backend only
cd backend
docker-compose up --build

# Or build manually
docker build -t test-case-generator .
docker run -p 8000:8000 --env-file .env test-case-generator
```

---

## 🔑 Configuration

### Backend Environment Variables

Create `backend/.env`:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional - for JIRA integration
JIRA_URL=https://your-company.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your_jira_api_token

# Optional - service config
SERVICE_PORT=8000
LOG_LEVEL=INFO
ENABLE_JIRA_MCP=false
```

### Frontend Environment Variables

Create `frontend/.env.local`:

```bash
# Local development
VITE_API_URL=http://localhost:8000

# Production
# VITE_API_URL=https://your-backend.railway.app
```

---

## 📖 Usage

### Via Web UI

1. Open http://localhost:5173
2. Choose mode:
   - **Manual Input**: Enter feature details directly
   - **JIRA Issue**: Enter JIRA issue key
3. Configure options (test types, edge cases, negative tests)
4. Click "Generate Test Cases"
5. View results and export as JSON

### Via API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Generate test cases
curl -X POST http://localhost:8000/api/v1/generate-test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "manual_input": {
      "title": "User Login Feature",
      "description": "Users can authenticate with email and password",
      "acceptance_criteria": [
        "User enters email and password",
        "System validates credentials",
        "User is redirected to dashboard"
      ]
    },
    "test_types": ["functional"],
    "include_edge_cases": true,
    "include_negative_tests": true
  }'
```

### API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🌐 Deployment

### Railway.app (Recommended)

**Backend:**
```bash
cd backend
railway login
railway init
railway up

# Set environment variables in Railway dashboard
```

**Frontend:**
```bash
cd frontend
vercel  # or use Railway
```

**Detailed Guide**: See [backend/DEPLOYMENT.md](backend/DEPLOYMENT.md)

### Supported Platforms
- ✅ Railway.app (easiest)
- ✅ Google Cloud Run
- ✅ AWS ECS/Fargate
- ✅ Azure Container Instances
- ✅ Heroku
- ✅ Vercel (frontend)
- ✅ Netlify (frontend)

---

## 🛠️ Tech Stack

### Backend
- **Python** 3.11
- **FastAPI** - Modern async web framework
- **Claude Agent SDK** - Autonomous agent capabilities
- **Anthropic API** - Claude Sonnet 4.5
- **JIRA SDK** - Issue integration
- **Uvicorn** - ASGI server
- **Docker** - Containerization

### Frontend
- **React** 18
- **Vite** - Build tool
- **Axios** - HTTP client
- **React Icons** - Icon library
- **CSS3** - Custom styling

---

## 📊 Example Output

The agent generates 8-12 comprehensive test cases per feature, including:

- ✅ **Happy Path** - Successful scenarios
- ✅ **Edge Cases** - Boundary conditions, special characters, max length
- ✅ **Negative Tests** - Invalid inputs, error handling
- ✅ **Security Tests** - SQL injection, XSS prevention
- ✅ **Validation Tests** - Required fields, format validation

Each test case includes:
- Clear title and description
- Type (functional, integration, E2E, unit, API)
- Priority (high, medium, low)
- Preconditions
- Step-by-step actions with expected results
- Overall expected outcome
- Tags for categorization

---

## 🧠 How It Works

### Autonomous Agentic Loop

1. **Receive Request** - API gets feature requirements
2. **Initialize Agent** - Claude Agent SDK with custom tools
3. **Agentic Loop** - Agent autonomously:
   - Analyzes acceptance criteria
   - Generates comprehensive test cases
   - Validates each test case using tools
   - Self-corrects any issues
   - Structures output in required format
4. **Return Results** - Structured JSON response

**No user interaction required** - the agent handles everything!

### Claude Agent SDK Integration

Uses official Claude Agent SDK with:
- **Model**: Claude Sonnet 4.5 (1M context)
- **Mode**: Non-interactive (`permission_mode="acceptEdits"`)
- **Tools**: Custom SDK MCP servers (in-process)
- **Async Generator Workaround**: Fixes SDK MCP bug

---

## 📁 Project Structure

```
test-generator/
├── backend/                    # FastAPI Microservice
│   ├── app/
│   │   ├── agents/            # Claude Agent SDK implementation
│   │   ├── api/               # FastAPI routes
│   │   ├── models/            # Pydantic schemas
│   │   ├── services/          # JIRA integration
│   │   └── main.py            # App entry point
│   ├── tests/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   └── Documentation (DEPLOYMENT.md, ARCHITECTURE.md, etc.)
│
├── frontend/                   # React Application
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── App.css            # Styles
│   │   └── main.jsx           # Entry point
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
└── README.md                   # This file
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing
```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev

# Open http://localhost:5173 and test the UI
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **Anthropic** - Claude Agent SDK and Claude API
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Railway** - Deployment platform

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check [backend/DEPLOYMENT.md](backend/DEPLOYMENT.md) for deployment help
- Review [backend/CLAUDE_AGENT_SDK_ARCHITECTURE.md](backend/CLAUDE_AGENT_SDK_ARCHITECTURE.md) for architecture details

---

## 🔗 Links

- **Live Demo**: [Coming soon after deployment]
- **API Documentation**: http://localhost:8000/docs (local)
- **Claude Agent SDK**: https://docs.anthropic.com/agent-sdk
- **GitHub Repository**: https://github.com/ramki271/test-generator

---

**Built with ❤️ using Claude Agent SDK**

---

## 📚 Documentation

- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
- [Deployment Guide](backend/DEPLOYMENT.md)
- [Architecture Details](backend/CLAUDE_AGENT_SDK_ARCHITECTURE.md)
- [Implementation Summary](backend/IMPLEMENTATION_SUMMARY.md)
