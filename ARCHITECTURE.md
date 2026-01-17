# Architecture

## System Overview

This is a production-grade, full-stack Retrieval-Augmented Generation (RAG) system built with Clean Architecture principles (SOLID, Ports & Adapters pattern).

## High-Level Architecture

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

## Core Components

### 1. Frontend Layer (React)
- **Technology**: React with Vite, WebSocket client
- **Responsibilities**:
  - User authentication and session management
  - Document upload interface
  - Real-time chat interface with streaming responses
  - Citation display and document management

### 2. Backend API Layer (FastAPI)
- **Technology**: FastAPI, Python 3.11+
- **Responsibilities**:
  - RESTful API endpoints for authentication, document management
  - WebSocket endpoint for real-time chat streaming
  - JWT-based authentication
  - Request validation and error handling

### 3. RAG Service (Core Business Logic)
- **Pattern**: Clean Architecture with Dependency Injection
- **Components**:
  - **Query Handler**: Processes user queries
  - **Context Builder**: Retrieves relevant document chunks from vector store
  - **LLM Orchestrator**: Manages LLM provider interactions
  - **Citation Tracker**: Maps generated text to source documents

### 4. Vector Store (ChromaDB)
- **Technology**: ChromaDB
- **Responsibilities**:
  - Stores document embeddings
  - Performs semantic similarity search
  - Manages document metadata and collections

### 5. Ingestion Pipeline
- **Technology**: Redis Queue, Background Workers
- **Flow**:
  1. User uploads document via API
  2. API validates and enqueues job to Redis
  3. Worker picks up job asynchronously
  4. Document is processed (PDF extraction, chunking)
  5. Chunks are embedded using sentence-transformers
  6. Embeddings stored in ChromaDB with metadata

### 6. LLM Provider Abstraction
- **Pattern**: Strategy Pattern (Pluggable Providers)
- **Supported Providers**:
  - OpenAI (GPT-4, GPT-3.5)
  - Groq (Llama models)
  - Google Gemini
  - Local models (via compatible APIs)
- **Configuration**: Provider selected via `LLM_PROVIDER` environment variable

## Data Flow

### Query Flow
1. User sends query via WebSocket
2. Backend authenticates request (JWT token)
3. RAG Service retrieves relevant context from ChromaDB
4. Context + Query sent to LLM Provider
5. LLM streams response tokens back through WebSocket
6. Citations extracted and sent alongside tokens
7. Frontend displays streaming response with citations

### Ingestion Flow
1. User uploads document (PDF) via REST API
2. API validates file and creates job in Redis queue
3. Worker retrieves job from queue
4. PDF text extracted using pypdf
5. Text split into chunks using langchain-text-splitters
6. Chunks embedded using sentence-transformers
7. Embeddings + metadata stored in ChromaDB
8. Job status updated (success/failure)

## Design Patterns

### Clean Architecture (Ports & Adapters)
- **Domain Layer**: Core business logic (RAG algorithms, query processing)
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External dependencies (ChromaDB, Redis, LLM APIs)
- **Presentation Layer**: FastAPI routes, WebSocket handlers

### Dependency Injection
- Services injected via FastAPI's dependency system
- Enables easy testing and provider swapping
- Decouples business logic from infrastructure

### Strategy Pattern
- LLM providers implement common interface
- Runtime provider selection based on configuration
- Easy to add new providers without modifying core logic

## Scalability Considerations

### Horizontal Scaling
- **API Servers**: Stateless, can scale horizontally behind load balancer
- **Workers**: Multiple workers can process ingestion jobs in parallel
- **Redis**: Acts as distributed queue for job coordination

### Asynchronous Processing
- FastAPI with async/await for non-blocking I/O
- Background workers prevent API blocking during heavy processing
- WebSocket streaming for real-time user experience

### Resilience
- Redis queue ensures no upload jobs are lost
- Worker retries on failure
- Graceful error handling and user feedback

## Security

- **Authentication**: JWT tokens with expiration
- **Password Hashing**: bcrypt for secure password storage
- **API Keys**: Environment-based configuration for LLM providers
- **CORS**: Configured for frontend-backend communication
- **Input Validation**: Pydantic models for request validation

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: SQLite (user data), ChromaDB (vectors)
- **Queue**: Redis
- **Embeddings**: sentence-transformers
- **PDF Processing**: pypdf
- **Text Splitting**: langchain-text-splitters

### Frontend
- **Framework**: React
- **Build Tool**: Vite
- **Styling**: Custom CSS (Tailwind-inspired)
- **Real-time**: WebSocket API

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Docker Compose for local development
- **Environment Management**: python-dotenv

## Future Enhancements

- Multi-tenancy support with user-specific document collections
- Advanced chunking strategies (semantic chunking, overlapping windows)
- Caching layer for frequently asked queries
- Monitoring and observability (metrics, logging, tracing)
- Support for additional document formats (DOCX, TXT, HTML)
- Fine-tuning embeddings for domain-specific use cases
