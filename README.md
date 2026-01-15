# Local Podcast Agent

A sophisticated local podcast generation system that creates AI-powered podcasts with multiple speakers using local LLMs and neural text-to-speech technology.

## 🚀 Features

- **AI-Powered Podcast Generation**: Automatically generates podcast episodes on any topic
- **Multi-Speaker Support**: Different voices for Host and Guest using neural TTS
- **Web Interface**: Modern UI built with Next.js for easy interaction
- **Local Processing**: All processing happens on your machine for privacy
- **Customizable**: Adjustable podcast length, host/guest names, and AI models
- **Audio Mixing**: Automatic mixing with background music using FFmpeg

## 🛠️ Tech Stack

- **Backend**: Python with FastAPI and CrewAI
- **Frontend**: Next.js with React, Tailwind CSS, Framer Motion
- **AI/LLM**: Ollama integration for local language models
- **TTS**: Piper neural text-to-speech
- **Audio Processing**: FFmpeg for mixing and processing
- **Voice Models**: ONNX-based English voice models

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- Ollama (for AI models)
- FFmpeg
- Git

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd local-podcast-agent
```

### 2. Backend Setup

```bash
# Navigate to the main directory
cd /path/to/local-podcast-agent

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install crewai duckduckgo-search fastapi uvicorn pydantic crewai-tools
```

### 3. Frontend Setup

```bash
# Navigate to the web directory
cd web

# Install dependencies
npm install

# Start the development server
npm run dev
```

### 4. Start the API Server

In a new terminal (with the virtual environment activated):

```bash
cd /path/to/local-podcast-agent
source .venv/bin/activate
python api.py
```

### 5. Access the Application

- Web Interface: http://localhost:3000
- API Endpoint: http://localhost:8000

## 🔧 Configuration

### Ollama Setup

Make sure you have Ollama installed and running with at least one model:

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (recommended)
ollama pull qwen2.5:0.5b

# Or any other model you prefer
ollama pull llama3.2
```

### Piper TTS Setup

The project includes pre-built Piper binaries for Linux x86_64. If you're on a different platform, download the appropriate version from the [Piper releases page](https://github.com/rhasspy/piper/releases).

## 🎙️ Usage

### Agent Mode (Automatic Generation)
1. Enter a topic for your podcast
2. Customize host and guest names
3. Select an AI model
4. Choose the desired length (short, medium, long)
5. Click "Generate Episode"
6. Wait for the AI to research and generate the podcast
7. Listen to your generated podcast

### Script Mode (Manual Input)
1. Switch to "Script Mode"
2. Enter your own script in the format:
   ```
   Host: Hello world!
   Guest: Hi there.
   Host: How are you today?
   ```
3. Click "Generate Episode"
4. Listen to your podcast with your custom script

## 🏗️ Project Structure

```
local-podcast-agent/
├── api.py                 # FastAPI server
├── podcast_agent.py       # Main podcast generation logic
├── manual_run.py          # Generate predefined scripts
├── manual_run_ai_agents.py # Another example script
├── test_audio.py          # Audio engine testing
├── test_ops.py            # Operations testing
├── script.txt             # Generated script storage
├── piper/                 # Piper TTS binaries
├── en_US-*.onnx           # Voice model files
├── en_US-*.onnx.json      # Voice model metadata
├── background_music.*     # Background music files
├── web/                   # Next.js frontend
│   ├── app/               # Next.js app router
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
└── README.md              # This file
```

## 🤖 Supported AI Models

The system works with any Ollama-compatible model. Some recommended models:
- `qwen2.5:0.5b` (default, lightweight)
- `llama3.2`
- `mistral`
- `phi3`

## 🎵 Audio Configuration

- **Sample Rate**: 22050 Hz (for voice models)
- **Format**: WAV (processed with FFmpeg)
- **Background Music**: Mixed at 20% volume when no dialogue is present
- **Dialogue Volume**: Boosted to 150% for clarity

## 🧪 Testing

To test the audio engine independently:

```bash
cd /path/to/local-podcast-agent
source .venv/bin/activate
python test_audio.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**: If ports 8000 or 3000 are already in use, you'll get binding errors. Kill the conflicting processes or change the ports in the respective configuration files.

2. **Missing Dependencies**: Make sure all Python and Node.js dependencies are installed in their respective environments.

3. **Ollama Not Running**: Ensure Ollama service is running before attempting to generate podcasts.

4. **FFmpeg Not Found**: Install FFmpeg on your system if audio mixing fails.

### Error Messages

- `"No module named 'crewai'"`: Activate your virtual environment and install dependencies
- `"Address already in use"`: Kill the process using the port or change the port
- `"Ollama not found"`: Install and start Ollama service

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 🐙 GitHub Repository Setup

To initialize this as a GitHub repository:

1. Create a new repository on GitHub
2. Initialize the local repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Local Podcast Agent"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

---

Made with ❤️ using local AI technologies