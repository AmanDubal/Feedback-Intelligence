# Feedback Intelligence

**Platform-Independent AI-Powered Product Feedback Analysis System**

Analyze, cluster, and prioritize feedback from any source using advanced AI and machine learning.

## 🌟 Features

- **Platform-Independent**: Ingest feedback from any source (CSV, API, Email, Manual, Webhooks, etc.)
- **AI-Powered Analysis**: Automatic sentiment analysis and issue categorization
- **Smart Clustering**: Group similar feedback items automatically
- **Priority Management**: Intelligent prioritization based on impact and urgency
- **Text Preprocessing**: Advanced NLP preprocessing for better analysis
- **Embeddings**: Vector embeddings for semantic similarity
- **REST API**: Full-featured FastAPI backend
- **Modern Frontend**: Next.js React dashboard with real-time visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd feedback-intelligence
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Frontend Setup**
```bash
cd frontend
npm install
```

### Running the Application

1. **Start Backend**
```bash
cd backend
uvicorn app.main:app --reload
# Backend will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

2. **Start Frontend**
```bash
cd frontend
npm run dev
# Frontend will be available at http://localhost:3000
```

## 📋 Project Structure

```
feedback-intelligence/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   │   └── integrations/  # Feedback source integrations
│   │   └── utils/        # Utilities (embeddings, preprocessing)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/         # Pages
│   │   ├── components/  # React components
│   │   ├── lib/         # Utilities
│   │   └── types/       # TypeScript types
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml
├── .env                 # Environment configuration (DO NOT COMMIT)
├── .env.example        # Environment template
└── README.md
```

## 🔌 Integrations

The system supports feedback ingestion from multiple sources:

- **CSV Files** - Upload feedback data in CSV format
- **JSON API** - Programmatic feedback submission
- **Email** - Feedback collected via email
- **Manual Input** - Direct submission through the UI
- **Webhooks** - Real-time feedback from external systems
- **Custom Sources** - Extensible for any feedback source

## 🛠️ API Endpoints

### Integrations
- `POST /api/v1/integrations/sources/register` - Register a feedback source
- `POST /api/v1/integrations/feedback/ingest` - Submit feedback batch
- `POST /api/v1/integrations/feedback/upload` - Upload feedback file
- `GET /api/v1/integrations/sync/status` - Get sync status
- `POST /api/v1/integrations/sync/manual` - Trigger sync

### Analysis
- `GET /api/v1/analysis/dashboard` - Dashboard metrics
- `GET /api/v1/analysis/clusters` - Get feedback clusters
- `GET /api/v1/analysis/trends` - Get trend analysis

### Feedback
- `GET /api/v1/feedback` - List feedback
- `POST /api/v1/feedback` - Create feedback
- `GET /api/v1/feedback/{id}` - Get feedback details

## ⚙️ Configuration

All configuration is managed through the `.env` file:

```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend Database
DATABASE_URL=sqlite:///./feedback.db

# API Settings
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# AI Services
OPENAI_API_KEY=your_key_here
EMBEDDING_MODEL=text-embedding-3-small

# Vector Database (Optional)
QDRANT_URL=http://localhost:6333

# Environment
ENVIRONMENT=development
```

## 🧠 AI Capabilities

### Sentiment Analysis
- Detects sentiment (positive, negative, neutral)
- Generates sentiment scores

### Text Preprocessing
- Tokenization
- Lemmatization
- Stop word removal
- Normalization

### Embeddings
- Vector embeddings for semantic similarity
- Powered by OpenAI embeddings
- Enables similarity-based clustering

### Clustering
- Automatic grouping of similar feedback
- Unsupervised clustering algorithms
- Identifies common themes

### Prioritization
- AI-driven priority scoring
- Considers frequency, sentiment, and impact
- Helps identify high-impact issues first

## 📊 Dashboard Features

- **Real-time Metrics** - View key statistics at a glance
- **Feedback Analysis** - Detailed analysis of feedback items
- **Cluster Visualization** - See grouped feedback patterns
- **Priority List** - Action-prioritized feedback
- **Trend Analysis** - Historical trends and patterns
- **Source Management** - Configure and manage feedback sources

## 🔐 Security

- Environment variables for sensitive configuration
- Secure credential storage
- CORS configuration for API access
- Input validation and sanitization

## 📝 Environment Configuration

Never commit `.env` file with sensitive information. Use `.env.example` as a template:

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env  # or use your editor

# Start using
npm run dev  # Frontend
uvicorn app.main:app --reload  # Backend
```

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

This will start:
- Backend API (port 8000)
- Frontend (port 3000)
- SQLite Database

## 📚 Technologies

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **Scikit-learn** - Machine learning
- **NLTK** - Natural language processing
- **OpenAI API** - Advanced AI capabilities

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 💬 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Built with ❤️ for intelligent feedback analysis**
