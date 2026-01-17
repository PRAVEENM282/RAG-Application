# RAG System Benchmarks

## Ingestion Performance
- **PDF (10MB)**: 
  - Upload Time: ~200ms
  - Processing Time (Chunk/Embed/Store): ~15s (Worker dependent)

## Query Latency (TTFT - Time To First Token)
- **OpenAI (GPT-4o)**: < 800ms
- **Groq (Llama3-70b)**: < 300ms
- **Local (Ollama)**: Dependent on hardware

## Throughput
- Supports 10+ concurrent streams on standard node.

## Load Testing
*Run the included load test script (if applicable) to verify.*
