# API Documentation

The Local Podcast Agent provides a REST API for generating podcasts programmatically.

## Base URL

`http://localhost:8000`

## Endpoints

### GET /

**Description**: Health check endpoint  
**Response**: `{"status": "Podcast Agent API is running"}`

### GET /api/models

**Description**: Get list of available Ollama models  
**Response**: 
```json
{
  "models": ["qwen2.5:0.5b", "llama3.2", "mistral", ...]
}
```

### POST /api/generate

**Description**: Generate a podcast using AI agents  
**Request Body**:
```json
{
  "topic": "string",
  "length": "short|medium|long",
  "host_name": "string",
  "guest_name": "string", 
  "model": "string"
}
```

**Response**:
```json
{
  "jobId": "string",
  "status": "queued"
}
```

### GET /api/status/{job_id}

**Description**: Check the status of a podcast generation job  
**Parameters**: `job_id` - The job identifier from `/api/generate`  
**Response**:
```json
{
  "status": "queued|processing|completed|failed",
  "message": "string",
  "filename": "string|null"
}
```

### POST /api/manual

**Description**: Generate a podcast from a manual script  
**Request Body**:
```json
{
  "script": "string"
}
```

**Response**:
```json
{
  "filename": "string",
  "status": "success"
}
```

### GET /api/audio/{filename}

**Description**: Retrieve a generated audio file  
**Parameters**: `filename` - The filename from generation response  
**Response**: Audio file (WAV format)

## Example Usage

### Generate a Podcast

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Artificial Intelligence",
    "length": "medium",
    "host_name": "Anny",
    "guest_name": "Dany Bhatti",
    "model": "qwen2.5:0.5b"
  }'
```

### Check Job Status

```bash
curl http://localhost:8000/api/status/{job_id}
```

### Generate from Manual Script

```bash
curl -X POST http://localhost:8000/api/manual \
  -H "Content-Type: application/json" \
  -d '{
    "script": "Host: Welcome to the show!\nGuest: Thanks for having me."
  }'
```

## Notes

- The `/api/generate` endpoint runs asynchronously and returns immediately with a job ID
- Use `/api/status/{job_id}` to poll for completion
- The `/api/manual` endpoint runs synchronously and returns immediately
- Audio files are stored temporarily and accessible via `/api/audio/{filename}`