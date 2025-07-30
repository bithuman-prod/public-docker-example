# Bithuman AI Voice Agent

A local deployment of Bithuman's AI voice agent with real-time conversation capabilities.

## What You Need

- Docker and Docker Compose
- API keys: `BITHUMAN_API_SECRET` and `OPENAI_API_KEY`
- `.imx` model files (place in `./models/` directory)

## Quick Setup

### 1. Configure Environment

Create a `.env` file:

```bash
BITHUMAN_API_SECRET=your_api_secret_here
OPENAI_API_KEY=your_openai_key_here
```

### 2. Add Models

Place your `.imx` files in the `models/` directory:

```bash
# Example - models/ directory should contain:
models/
└── YourModel.imx
```

### 3. Start Services

```bash
docker compose up
```

Wait for all services to start (first run takes a few minutes).

### 4. Access the App

Open http://localhost:4202 in your browser.

## That's It!

The system runs 4 services:
- **LiveKit**: WebRTC communication server
- **Agent**: AI conversation handler  
- **Frontend**: Web interface
- **Redis**: Message broker

## Development

**Edit agent code:**
```bash
vim agent.py
docker compose restart agent
```

**View logs:**
```bash
docker compose logs -f agent
```

**Stop everything:**
```bash
docker compose down
```

## Troubleshooting

**Services won't start?**
- Check `.env` file exists with valid API keys
- Ensure models/ directory contains `.imx` files
- Run `docker compose logs [service]` to see errors

**Port conflicts?**
- Frontend uses port 4202
- LiveKit uses ports 17880-17881 and UDP 50700-50720

**Clean restart:**
```bash
docker compose down -v
docker compose up --build
```

