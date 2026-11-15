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
    stateless_http=True,  # no sessions: safe on Render restarts
    json_response=True,
)


class AgencyStatus(BaseModel):
    service: str
    version: str
    status: str
    phase: str
    started_at: str
    uptime_seconds: int
    server_time_utc: str


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get agency status",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    )
)
def get_agency_status() -> AgencyStatus:
    """Return the current status of the AV Digital Agency MCP server."""
    now = datetime.now(timezone.utc)
    logger.info("tool called: get_agency_status")
    return AgencyStatus(
        service=SERVICE_NAME,
        version=VERSION,
        status="ok",
        phase="1 - MCP server foundation",
        started_at=STARTED_AT.isoformat(),
        uptime_seconds=int((now - STARTED_AT).total_seconds()),
        server_time_utc=now.isoformat(),
    )


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "service": SERVICE_NAME, "version": VERSION})


if __name__ == "__main__":
    logger.info("starting %s v%s on port %s", SERVICE_NAME, VERSION, PORT)
    mcp.run(transport="streamable-http")
