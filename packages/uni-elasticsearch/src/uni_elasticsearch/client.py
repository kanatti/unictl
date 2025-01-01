import asyncio
import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    async with AsyncExitStack() as stack:
        server_params = StdioServerParameters(
            command='uv',
            args=['run', '--package', 'uni-elasticsearch', 'server'],
            env=None
        )

        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await stack.enter_async_context(ClientSession(stdio, write))

        await session.initialize()

        response = await session.list_tools()
        print("\nConnected to server. Available tools:")
        for tool in response.tools:
            print(f"- {tool.name}: {tool.description}")
            if tool.inputSchema:
                print(f"  Input schema: {tool.inputSchema}")

if __name__ == "__main__":
    asyncio.run(main())