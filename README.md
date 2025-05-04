# Georgian Guide AI Assistant

An AI-powered assistant for travelers in Georgia (the country) that helps with finding places to visit, restaurants, and other attractions using Google Maps data.

## Features

- Processes natural language queries about locations in Georgia
- Uses Google Maps MCP with Claude's MCP framework for geographic data
- Provides personalized recommendations based on user preferences
- Structured around schema-first development principles

## Project Structure

```
georgian_guide/
├── src/
│   └── georgian_guide/
│       ├── schemas/        # Central schema definitions (source of truth)
│       ├── core/           # Core application logic
│       ├── llm/            # LLM integration
│       ├── tools/          # Google Maps MCP tools
│       ├── routers/        # Request routing logic
│       └── api/            # API endpoints
├── tests/                  # Test suite
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Setup

1. Create a virtual environment with UV:
   ```
   uv venv
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate   # On Windows
   ```

3. Install dependencies with UV:
   ```
   uv pip sync requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the application:
   ```
   uvicorn src.georgian_guide.api.main:app --reload
   ```

## Usage

Send a natural language query to the `/query` endpoint:

```
POST /query
{
    "query": "I'm a 22 y.o. old guy in Tbilisi, Rustaveli and I want to eat khinkali"
}
```

The assistant will:
1. Process your query
2. Select appropriate Google Maps tools
3. Retrieve relevant information
4. Provide a helpful response with recommendations

## Development

This project follows schema-driven development principles:
- All data models are defined in schemas first
- Code is generated from schemas where possible
- All components validate against the central schemas 