# RepoAnalyzer-Pro 🚀

A powerful, multi-API repository analysis tool that provides comprehensive insights into any GitHub repository using specialized AI analysis.

**Created with ❤️ by [Vishesh Sanghvi](http://visheshsanghvi.me/)**

## ✨ Features

- **🔍 Multi-API Analysis**: Uses 5 specialized Gemini APIs for different analysis types
- **🏗️ Architecture Flow**: Step-by-step execution flow and component relationships
- **🗺️ Mind Map Generation**: Visual structure and file organization breakdown
- **🔒 Security Analysis**: Critical vulnerabilities and security best practices
- **📊 Code Quality Assessment**: Actionable feedback and improvement suggestions
- **⚡ Performance Insights**: Bottlenecks and optimization opportunities
- **🔄 Real-time Progress**: Live progress tracking with job-based processing
- **💾 Persistent Storage**: Results saved in localStorage for session persistence
- **🎨 Modern UI**: Beautiful SaaS-like interface with tabbed navigation
- **🔐 Secure API Management**: Environment-based API key configuration

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Google Gemini AI**: 5 specialized APIs for different analysis types
- **GitPython**: Repository cloning and parsing
- **Concurrent Processing**: Parallel API calls for faster analysis

### Frontend
- **React + TypeScript**: Modern, type-safe frontend
- **Tailwind CSS**: Utility-first styling
- **Local Storage**: Client-side data persistence
- **Responsive Design**: Works on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/visheshsanghvi112/RepoAnalyzer-Pro.git
cd RepoAnalyzer-Pro

# Install Python dependencies
pip install -r requirements.txt

# Configure API keys (see Environment Variables section below)
cp env.example .env
# Edit .env with your API keys

# Start the backend server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd cache/ambica-pharma-portal

# Install dependencies
npm install

# Start the development server
npm run dev
```

### Environment Variables
Create a `.env` file in the root directory by copying `env.example`:

```bash
cp env.example .env
```

Then edit `.env` with your API keys:

```env
# Option 1: Single API Key (for all analysis types)
GEMINI_API_KEY=your_single_gemini_api_key_here

# Option 2: Multiple Specialized API Keys (recommended for better performance)
GEMINI_API_KEY_ARCHITECTURE=your_architecture_analysis_api_key
GEMINI_API_KEY_MINDMAP=your_mind_map_analysis_api_key
GEMINI_API_KEY_QUALITY=your_code_quality_analysis_api_key
GEMINI_API_KEY_SECURITY=your_security_analysis_api_key
GEMINI_API_KEY_PERFORMANCE=your_performance_analysis_api_key
```

**🔐 Security Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## 📖 Usage

1. **Start the Application**: Both backend and frontend should be running
2. **Enter Repository URL**: Paste any GitHub repository URL
3. **Wait for Analysis**: Real-time progress tracking shows analysis status
4. **Explore Results**: Switch between different analysis tabs:
   - **Overview**: Quick summary of all analyses
   - **Architecture Flow**: How the application works
   - **Mind Map**: Visual structure breakdown
   - **Security**: Vulnerabilities and security posture
   - **Code Quality**: Improvement suggestions
   - **Performance**: Optimization opportunities

## 🔧 API Endpoints

- `GET /health` - Health check endpoint
- `GET /api-status` - Check API key configuration status
- `POST /summarize-repo` - Start repository analysis
- `GET /summary-status` - Check analysis progress
- `GET /get-summary` - Retrieve analysis results

## 🏗️ Architecture

### Backend Structure
```
├── main.py              # FastAPI application and endpoints
├── api_handlers.py      # Specialized AI analysis functions
├── config.py            # Secure API key configuration
├── repo_cloner.py       # Repository cloning logic
├── tree_parser.py       # File tree parsing
├── requirements.txt     # Python dependencies
├── env.example          # Example environment configuration
└── .env                 # Your API keys (not in git)
```

### Frontend Structure
```
cache/ambica-pharma-portal/
├── src/
│   ├── App.tsx          # Main application component
│   ├── components/      # UI components
│   └── ...
├── package.json         # Node.js dependencies
└── ...
```

## 🎯 Analysis Types

### 1. Architecture Flow
- Execution flow and data movement
- Main components and relationships
- Entry points and dependencies
- Complexity assessment

### 2. Mind Map
- Visual repository structure
- File categories and hierarchies
- Core features and modules
- File relationships

### 3. Security Analysis
- Critical vulnerabilities
- Security best practices
- Authentication mechanisms
- Data protection assessment

### 4. Code Quality
- Code organization and structure
- Readability and maintainability
- Documentation quality
- Testing coverage

### 5. Performance
- Performance bottlenecks
- Optimization opportunities
- Scalability considerations
- Resource efficiency

## 🔒 Security Features

- **Secure API Key Management**: Environment-based configuration
- **No Hardcoded Secrets**: All API keys loaded from environment variables
- **Error Handling**: Robust retry logic and fallback responses
- **Input Validation**: Safe repository URL processing
- **CORS Configuration**: Proper cross-origin request handling

## 🚀 Performance Features

- **Parallel Processing**: All 5 analyses run simultaneously
- **Progress Tracking**: Real-time status updates
- **Caching**: Results persist across sessions
- **Error Recovery**: Graceful handling of API failures

## 🔐 API Key Configuration

### Getting Gemini API Keys
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### Configuration Options
- **Single Key**: Use one API key for all analysis types
- **Multiple Keys**: Use different keys for each analysis type (recommended)

### Troubleshooting
If you see "API analysis failed" messages:
1. Check that your `.env` file exists and contains valid API keys
2. Verify your API keys are active and have sufficient quota
3. Ensure the `.env` file is in the root directory of the project

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Creator

**RepoAnalyzer-Pro** was created by **[Vishesh Sanghvi](http://visheshsanghvi.me/)**

- 🌐 **Website**: [visheshsanghvi.me](http://visheshsanghvi.me/)
- 🐙 **GitHub**: [@visheshsanghvi112](https://github.com/visheshsanghvi112)
- 📧 **Contact**: Available through [visheshsanghvi.me](http://visheshsanghvi.me/)

## 🙏 Acknowledgments

- **Vishesh Sanghvi** - Creator and Lead Developer
- Google Gemini AI for powerful analysis capabilities
- FastAPI for the excellent web framework
- React and Tailwind CSS for the beautiful UI

---

**Built with ❤️ by [Vishesh Sanghvi](http://visheshsanghvi.me/) for developers who want to understand their code better!**

*RepoAnalyzer-Pro - Making repository analysis intelligent, comprehensive, and accessible.* 