# AIxOS - AI-Powered Operating System

An intelligent Linux-based operating system that understands and executes natural language commands.

## 🌟 Overview

AIxOS is an AI-powered operating system built on Linux that allows users to interact with their computer using natural language commands. Instead of memorizing complex terminal commands, users can simply type what they want to accomplish in plain English.

**Example Commands:**
- "Install Python and VS Code, and set up a new folder for my coding projects"
- "Show me all Python files modified in the last week"
- "Update all system packages and restart the web server"
- "Create a new Git repository and make an initial commit"

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   AI Interpreter │───▶│ Command Executor│
│ (Natural Lang.) │    │   (GPT/Mistral)  │    │   (Safe Shell)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Memory Manager  │    │ Docker Container│
                       │ (Vector Store)   │    │   (Isolation)   │
                       └──────────────────┘    └─────────────────┘
```

## 🚀 Core Components

- **🐧 Linux Base**: Ubuntu 22.04 foundation with essential tools
- **🤖 LLM Integration**: GPT or Mistral for natural language processing
- **💬 Smart Terminal/Shell**: AI-enhanced command interface with rich output
- **🔗 Glue Code**: Python for system integration and orchestration
- **🧠 Vector Store**: ChromaDB for learning and contextual memory
- **🐳 Docker**: For safety, isolation, portability, reproducibility, and resource management
- **📚 Context7 MCP**: Up-to-date documentation integration

## ✨ MVP Features

### 🗣️ Natural Language Command Translation
- Type commands in plain English
- AI translates to appropriate system commands
- Safe execution with user confirmation in safe mode
- Real-time feedback and error handling
- Command history and learning from past interactions

### 🛡️ Safety Features
- Docker containerization for complete isolation
- Safe mode with command confirmation
- Dangerous command blocking
- Resource limits (CPU, memory)
- Non-root user execution

### 🧠 Learning & Memory
- Remembers successful command patterns
- Learns from user interactions
- Contextual suggestions based on history
- Vector-based semantic search for similar commands

## 🔮 Future Features

- **🎤 Voice Commands**: Speak to your computer naturally
- **🔍 Smart File Finder**: "Find that Python file I was working on yesterday"
- **🔧 Auto-Error Fixing**: Automatically suggest fixes for failed commands
- **🎓 "Teach me Linux" Mode**: Educational mode for learning Linux commands
- **💾 Enhanced Memory**: Advanced user preferences and workflow learning
- **🌐 Web Interface**: Browser-based GUI for AIxOS

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key (for GPT integration)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AIxOS
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Start AIxOS:**
   ```bash
   ./start-aixos.sh
   ```

### Manual Setup

1. **Build the Docker image:**
   ```bash
   docker build -t aixos:latest --target production .
   ```

2. **Start with Docker Compose:**
   ```bash
   docker-compose up aixos
   ```

3. **Development mode:**
   ```bash
   docker-compose --profile dev up aixos-dev
   ```

## 🐳 Docker Benefits

We use Docker for multiple critical reasons:

- **🛡️ Safety**: Isolated environment prevents system damage
- **🔒 Isolation**: Commands run in contained environment
- **📦 Portability**: Works the same on any system with Docker
- **🔄 Reproducibility**: Consistent environment every time
- **⚡ Resource Management**: CPU and memory limits enforced
- **🧹 Clean Environment**: No pollution of host system

## 📚 Context7 MCP Integration

AIxOS integrates with Context7 MCP for up-to-date documentation:

### Usage Guidelines
- Always use Context7 MCP for libraries like Next.js, Supabase, React
- Maximum 5000 tokens per documentation query
- Limit to 3 searches maximum per specific documentation piece
- Automatic injection of current, version-specific documentation

### Supported Libraries
Context7 provides documentation for 9900+ libraries including:
- React, Next.js, Vue.js
- Node.js, Express, FastAPI
- Supabase, MongoDB, PostgreSQL
- Docker, Kubernetes
- And many more...

## 🛠️ Development

### Project Structure
```
AIxOS/
├── aixos/                 # Main application package
│   ├── core/             # Core modules
│   │   ├── config.py     # Configuration management
│   │   ├── shell.py      # Main AI shell interface
│   │   ├── ai_interpreter.py  # Natural language processing
│   │   ├── command_executor.py  # Safe command execution
│   │   └── memory.py     # Learning and memory management
│   └── main.py           # Application entry point
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Docker services configuration
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
└── README.md            # This file
```

### Development Mode

```bash
# Start development environment
./start-aixos-dev.sh

# Or manually:
docker build -t aixos:dev --target development .
docker-compose --profile dev up -d aixos-dev
docker-compose exec aixos-dev /bin/bash
```

### Running Tests

```bash
# Inside the development container
pytest tests/

# With coverage
pytest --cov=aixos tests/
```

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# AI Configuration
OPENAI_API_KEY=your_api_key_here
AI_MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7

# Safety Settings
SAFE_MODE=true
COMMAND_TIMEOUT=30
MAX_OUTPUT_LINES=50

# Storage
VECTOR_STORE_PATH=./data/vector_store
LOG_LEVEL=INFO
```

### Docker Compose Services

- **aixos**: Main application container
- **chromadb**: Vector database for memory (optional)
- **aixos-dev**: Development environment with additional tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 for Python code style
- Use type hints where possible
- Add docstrings to all functions and classes
- Write tests for new features
- Update documentation as needed

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- **Context7**: For providing up-to-date documentation integration
- **Anthropic**: For the Model Context Protocol (MCP)
- **OpenAI**: For GPT API integration
- **Docker**: For containerization technology
- **Ubuntu**: For the solid Linux foundation

---

**AIxOS** - Making Linux accessible through natural language! 🤖✨