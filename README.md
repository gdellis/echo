# Echo - AI-Powered Audio Transcription App

![Echo Logo](resources/echo-icon.png)

[![Lint and Test](https://github.com/gdellis/echo/actions/workflows/lint-test.yml/badge.svg)](https://github.com/gdellis/echo/actions/workflows/lint-test.yml)

An AI-powered transcription application that converts audio to text with speaker diarization using OpenAI Whisper and pyannote.audio.

## Features

- 🎤 **Audio Transcription** - Convert audio/video files to text using OpenAI Whisper
- 👥 **Speaker Diarization** - Automatically identify and label different speakers
- 📄 **Multiple Export Formats** - Export as plain text, SRT subtitles, or JSON
- 🚀 **Fast Processing** - Async task processing with Celery
- 📊 **Job History** - Track all your transcription jobs
- 🖼️ **Modern UI** - Built with React, TypeScript, and Tailwind CSS

## Tech Stack

### Frontend

- React 18+ with TypeScript
- Tailwind CSS
- React Dropzone (file uploads)
- Zustand (state management)
- Axios (HTTP client)

### Backend

- FastAPI (Python web framework)
- OpenAI Whisper (speech-to-text)
- pyannote.audio (speaker diarization)
- Celery + Redis (async task queue)
- SQLite (database)
- Docker (containerization)

## Prerequisites

- Docker and Docker Compose
- git

## Quick Start

1. Clone the repository:

```bash
git clone <repository-url>
cd echo
```

1. Start the application:

```bash
docker-compose up --build
```

This will start:

- Redis on port 6379
- Backend API on <http://localhost:8000>
- Frontend on <http://localhost:3000>
- Celery worker for async processing
- Celery Beat for scheduled tasks

1. Open your browser and navigate to <http://localhost:3000>

## Local Development (Non-Docker)

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Start the backend server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

1. Open a new terminal and navigate to frontend directory:

```bash
cd frontend
```

1. Install dependencies:

```bash
npm install
```

1. Start the development server:

```bash
npm run dev
```

The frontend will be available at <http://localhost:5173>

## Supported File Formats

- Audio: MP3, WAV, M4A, FLAC
- Video: MP4, MOV

## Configuration

### Environment Variables

**Backend (.env):**

```env
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
PYANNOTE_MODEL=pyannote/speaker-diarization
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
DATABASE_URL=sqlite:///./echo.db
MAX_UPLOAD_SIZE=524288000
UPLOAD_DIR=/tmp/echo
```

**Frontend (.env):**

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## API Endpoints

### POST /api/v1/transcribe

Upload and transcribe an audio file.

**Request:**

- `file`: multipart/form-data (audio file)

**Response:**

```json
{
  "job_id": "uuid",
  "status": "queued",
  "message": "File uploaded, processing started"
}
```

### GET /api/v1/jobs/{job_id}

Check job status and get results.

**Response (complete):**

```json
{
  "job_id": "uuid",
  "status": "completed",
  "result": {
    "text": "Full transcription...",
    "segments": [
      {
        "start": 0.0,
        "end": 3.5,
        "text": "Hello everyone",
        "speaker": "SPEAKER_00",
        "confidence": 0.95
      }
    ],
    "speakers": 2,
    "duration": 120.5
  }
}
```

### GET /api/v1/history

List all transcriptions with metadata.

### DELETE /api/v1/jobs/{job_id}

Delete a transcription job.

## Project Structure

```
echo/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── services/     # ML services (Whisper, Diarization)
│   │   ├── tasks/        # Celery tasks
│   │   └── utils/        # Utility functions
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   └── types/        # TypeScript types
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Troubleshooting

### Common Issues

1. **Whisper model download fails**
   - The first run will download the Whisper model (~140MB for base model)
   - Be patient, this may take a few minutes

2. **Port already in use**
   - Change the port in docker-compose.yml
   - Update VITE_API_URL in frontend/.env accordingly

3. **File too large**
   - Default max file size is 500MB
   - Increase MAX_UPLOAD_SIZE in docker-compose.yml

## License

MIT