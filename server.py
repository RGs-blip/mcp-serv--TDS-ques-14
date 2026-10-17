import hashlib

from mcp.server.mcpserver import MCPServer, Context
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "23f1001344@ds.study.iitm.ac.in"

mcp = MCPServer("IITM MCP Challenge Server")


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """
    Return the first 16 lowercase hex characters of
    SHA-256(challenge + ':' + normalized_email).
    """
    request = ctx.request_context.request
    headers = request.headers

    challenge = headers.get("x-exam-challenge", "")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    digest = hashlib.sha256(f"{challenge}:{EMAIL}".encode("utf-8")).hexdigest()
    return digest[:16]


app = mcp.streamable_http_app(
    transport_security=TransportSecuritySettings(
        allowed_hosts=["mcp-serv-tds-ques-14.onrender.com"]
    )
)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")