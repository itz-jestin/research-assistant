# Research Assistant using LangGraph

A Multi-Agent AI Research Assistant built with LangGraph, FastAPI, React, and Tavily Search.

## Features

- Multi-Agent Workflow
- Planner Agent
- Researcher Agent
- Writer Agent
- Critic Agent
- Tavily Web Search
- FastAPI Backend
- React Frontend
- REST API
- LangGraph State Management

## Tech Stack

### Backend
- Python
- FastAPI
- LangGraph
- LangChain
- NVIDIA NIM
- Tavily Search

### Frontend
- React
- Next.js
- Tailwind CSS

## Architecture

User
↓
Planner
↓
Researcher
↓
Writer
↓
Critic
↓
Final Report

## Installation

### Clone

```bash
git clone https://github.com/itz-jestin/research-assistant.git
cd research-assistant
```

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API

POST

```
/research
```

Example

```json
{
    "query":"What is Agentic AI?"
}
```

## Folder Structure

```
research-assistant/
│
├── backend/
├── frontend/
├── README.md
└── .gitignore
```

## Future Improvements

- PDF Export
- Parallel Research Agents
- Streaming Responses
- Authentication
- Citation Support
- Docker Deployment

## Author

Jestin Monachan