import asyncio
import hashlib

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

EMAIL = "23f1001344@ds.study.iitm.ac.in"
URL = "http://127.0.0.1:8000/mcp"


async def main():
    challenge = "0123456789abcdef0123456789abcdef"

    headers = {
        "X-Exam-Challenge": challenge,
        "X-Exam-Timestamp": "1700000000000",
        "X-Exam-Signature": "not-checked",
    }

    async with httpx2.AsyncClient(headers=headers) as http_client:
        transport = streamable_http_client(URL, http_client=http_client)

        async with Client(transport) as client:
            tools = await client.list_tools()
            print("Tools:", [tool.name for tool in tools.tools])

            result = await client.call_tool("solve_challenge", {})
            answer = result.content[0].text
            print("Server answer:", answer)

            expected = hashlib.sha256(
                f"{challenge}:{EMAIL}".encode("utf-8")
            ).hexdigest()[:16]

            print("Expected answer:", expected)


asyncio.run(main())