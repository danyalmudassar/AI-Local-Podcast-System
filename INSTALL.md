# Installation Guide

This guide will walk you through installing and setting up the Local Podcast Agent on your system.

## Prerequisites

Before installing, make sure you have the following software installed on your system:

- **Python 3.8 or higher**
- **Node.js 18 or higher**
- **npm** (usually comes with Node.js)
- **Git**
- **FFmpeg**
- **Ollama** (for AI models)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/local-podcast-agent.git
cd local-podcast-agent
```

### 2. Install System Dependencies

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### On macOS:
```bash
brew install ffmpeg
```

#### On Windows:
Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add it to your PATH.

### 3. Install Ollama

Visit [https://ollama.ai](https://ollama.ai) and follow the installation instructions for your operating system.

After installation, pull a model (recommended):
```bash
ollama pull qwen2.5:0.5b
```

Or any other model you prefer:
```bash
ollama pull llama3.2
```

### 4. Set Up Python Environment

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 5. Set Up Frontend

```bash
# Navigate to the web directory
cd web

# Install Node.js dependencies
npm install
```

### 6. Run the Application

#### Terminal 1 - API Server:
```bash
# From the main project directory
cd /path/to/local-podcast-agent
source .venv/bin/activate  # if using virtual environment
python api.py
```

#### Terminal 2 - Web Interface:
```bash
# From the web directory
cd /path/to/local-podcast-agent/web
npm run dev
```

### 7. Access the Application

Open your browser and go to [http://localhost:3000](http://localhost:3000)

The API will be available at [http://localhost:8000](http://localhost:8000)

## Alternative: Using the Setup Script

Instead of following steps 2-5 manually, you can run the provided setup script:

```bash
chmod +x setup.sh
./setup.sh
```

## Docker Installation (Alternative Method)

If you prefer using Docker:

1. Make sure you have Docker and Docker Compose installed
2. Run the following command from the project root:

```bash
docker-compose up --build
```

Note: You'll still need to have Ollama running separately.

## Troubleshooting

### Common Issues:

1. **Port already in use**: Make sure ports 8000 and 3000 are available
2. **Module not found**: Ensure your virtual environment is activated
3. **Ollama not responding**: Check that Ollama service is running
4. **FFmpeg not found**: Verify FFmpeg is installed and in your PATH

### Verifying Installation:

To verify that everything is working:

1. Check that Ollama is running: `curl http://localhost:11434/api/tags`
2. Check that the API is running: `curl http://localhost:8000`
3. Visit the web interface at [http://localhost:3000](http://localhost:3000)

## Updating

To update to the latest version:

```bash
git pull origin main
cd web
npm install
cd ..
source .venv/bin/activate
pip install -r requirements.txt
```

---

That's it! You now have Local Podcast Agent installed and running on your system.