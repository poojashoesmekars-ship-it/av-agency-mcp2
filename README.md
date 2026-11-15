# av-agency-mcp

AV Digital Agency MCP server. **Phase 1:** `/mcp` (Streamable HTTP), `/health`, one read-only tool `get_agency_status`.

## Run locally
```
pip install -r requirements.txt
python server.py
```
Health: http://localhost:8000/health  |  MCP: http://localhost:8000/mcp

## Deploy on Render
New > Blueprint (or Web Service) > connect this repo. `render.yaml` sets everything.
Endpoint: `https://<service-name>.onrender.com/mcp`

## Status
- Phase 1 is NOT authenticated. Do not add tools that touch client data before Phase 2 (OAuth).
- Free Render plan sleeps when idle; first request after sleep can be slow.
- Never commit `.env` or any credentials.
