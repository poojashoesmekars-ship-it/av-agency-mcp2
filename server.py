"""AV Digital Agency - MCP server (Phase 1).

Exposes:
  POST /mcp    MCP endpoint (Streamable HTTP)
  GET  /health health check for Render

Phase 1 has NO authentication, so it only offers one harmless read-only tool.
Do not add tools that touch client data until Phase 2 (OAuth) is done.
"""
import logging
import os
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

SERVICE_NAME = "av-agency-mcp"
VERSION = "0.1.0"
STARTED_AT = datetime.now(timezone.utc)

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(SERVICE_NAME)

# Render provides the PORT variable. Binding to 0.0.0.0 is required there.
PORT = int(os.environ.get("PORT", "8000"))

mcp = FastMCP(
    SERVICE_NAME,
    host="0.0.0.0",
    port=PORT,
