# Echo

An AI-powered transcription application that converts audio to text with automatic speaker diarization using Whisper and pyannote.audio.

## Overview

Echo is a full-stack web application that:
- Transcribes audio and video files to text
- Identifies and labels different speakers (speaker diarization)
- Provides export options (plain text, SRT subtitles, JSON)
- Features a modern React frontend with FastAPI backend

## Tech Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (built on Radix UI)
- **State Management**: React Context API + Zustand
- **File Handling**: React Dropzone

### Backend
- **Framework**: FastAPI (Python)
- **Transcription**: OpenAI Whisper (base/small models)
- **Speaker Diarization**: pyannote.audio
- **Task Queue**: Celery with Redis
- **Database**: SQLite

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │     │   Backend       │     │   Celery        │
│   (React)       │────▶│   (FastAPI)     │────▶│   (Workers)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                     │
                                    ┌────────────────┼────────────────┐
                                    │                │                │
                              ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
                              │  Redis    │  │  Whisper  │  │ pyannote  │
                              │  (Broker) │  │  (STT)    │  │ (Diarization)│
                              └───────────┘  └───────────┘  └───────────┘
                                                     │
                                                ┌────▼────┐
                                                │ SQLite  │
                                                │ (Store) │
                                                └─────────┘
```

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed

### Installation

1. Clone the repository
2. Build and run all services:

```bash
docker-compose up --build
```

This will start:
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)
- Celery worker
- Celery beat (scheduled tasks)

Access the application at [http://localhost:3000](http://localhost:3000)

## Local Development

### Prerequisites
- Python 3.10+
- Node.js 18+
- Redis server

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd echo
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
npm run dev
```

4. **Redis Setup** (in a separate terminal)
```bash
redis-server
```

5. **Celery Worker** (in a separate terminal)
```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

Access the frontend at [http://localhost:3000](http://localhost:3000)

## Configuration

### Backend (.env)
```env
APP_NAME="Echo API"
DEBUG=False
CORS_ORIGINS=http://localhost:3000

WHISPER_MODEL=base
WHISPER_DEVICE=cpu

PYANNOTE_MODEL=pyannote/speaker-diarization

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

MAX_UPLOAD_SIZE=524288000
UPLOAD_DIR=/tmp/transcriber

DATABASE_URL=sqlite:///./transcriber.db
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME="Echo"
VITE_MAX_FILE_SIZE=500
```

## Supported File Formats

- Audio: MP3, WAV, M4A, FLAC, OGG
- Video: MP4, MOV, WEBM

Maximum file size: 500MB (free tier)

## API Endpoints

### POST /api/v1/transcribe
Upload and transcribe an audio file.

### GET /api/v1/jobs/{job_id}
Check job status and get transcription results.

### GET /api/v1/history
List all transcriptions with metadata.

### DELETE /api/v1/jobs/{job_id}
Delete a transcription job.

## Project Structure

```
transcriber/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── services/        # ML services (Whisper, pyannote)
│   │   ├── tasks/           # Celery workers
│   │   └── utils/           # Utilities
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom hooks
│   │   └── types/           # TypeScript types
│   ├── public/
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit your changes: `git commit -m 'feat: add some feature'`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Open a Pull Request

## License

MIT License