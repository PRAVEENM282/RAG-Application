# Enterprise RAG System

A production-grade, full-stack Retrieval-Augmented Generation system featuring:
- **Clean Architecture** (SOLID, Ports & Adapters)
- **Real-time Streaming** (Tokens & Citations via WebSockets)
- **Pluggable LLMs** (OpenAI, Groq, Gemini, Local)
- **Async Ingestion Pipeline** (Redis + Workers)

## Architecture

```ascii
Frontend (React) <-> WebSocket <-> Backend API (FastAPI)
                                      |
                                  RAG Service
                                      |
       +------------------+-----------+-----------+
       |                  |                       |
  LLM Provider      Context Builder         Vector Store
       |                                          ^
       v                                          |
  (OpenAI/Groq)                                   |
                                                  |
Ingestion Flow:                                   |
Upload -> API -> Redis Queue -> Worker -> Chunk -> Embed -> ChromaDB
```

## Quick Start

1. **Clone the repository**
2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```
3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```
4. **Access the App**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/docs

## Features

- **Decoupled Worker**: Heavy file processing happens in background workers.
- **Provider Agnostic**: Switch models just by changing `LLM_PROVIDER` env var.
- **Resilient**: Redis-backed queue ensures no upload is lost.
- **Scalable**: Stateless API servers, scalable workers.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Pydantic, Redis, ChromaDB
- **Frontend**: React, Vite, Tailwind-style CSS, WebSockets
- **Ops**: Docker, Docker Compose

## API Documentation

See `/docs` endpoint for full Swagger UI.
