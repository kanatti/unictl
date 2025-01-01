from typing import Any
import asyncio
import httpx
import logging
import sys
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Configure logging to stderr
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

server = Server("uni-elasticsearch")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-cluster-health",
            description="Get health of Elasticsearch cluster",
            inputSchema={
                 "type": "object",
                 "properties": {},
                 "required": []
             }
        ),
        types.Tool(
            name="get-indices",
            description="Get indices present on the Elasticsearch cluster",
            inputSchema={
                "type": "object",
                "properties": {
                    "prefix": {
                        "type": "string",
                        "description": "Prefix to match indices by.",
                    },
                },
                "required": ["prefix"],
            },
        ),
    ]

async def make_es_request(client: httpx.AsyncClient, url: str) -> dict[str, Any] | None:
    """Make a request to the Elasticsearch API with proper error handling."""
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = await client.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can fetch Elasticsearch data and notify clients of changes.
    """
    if name == "get-cluster-health":
        async with httpx.AsyncClient() as client:
            health_url = "http://localhost:9200/_cluster/health"
            health_data = await make_es_request(client, health_url)

            if not health_data:
                return [types.TextContent(type="text", text="Failed to retrieve cluster health data")]

            health_text = f"Cluster Health:\n" \
                          f"Status: {health_data.get('status', 'Unknown')}\n" \
                          f"Number of nodes: {health_data.get('number_of_nodes', 'Unknown')}\n" \
                          f"Active shards: {health_data.get('active_shards', 'Unknown')}"

            return [types.TextContent(type="text", text=health_text)]

    elif name == "get-indices":
        if not arguments or "prefix" not in arguments:
            return [types.TextContent(type="text", text="Missing prefix parameter")]

        prefix = arguments["prefix"]
        async with httpx.AsyncClient() as client:
            indices_url = f"http://localhost:9200/_cat/indices/{prefix}*?format=json"
            indices_data = await make_es_request(client, indices_url)

            if not indices_data:
                return [types.TextContent(type="text", text="Failed to retrieve indices data")]

            if not indices_data:
                return [types.TextContent(type="text", text=f"No indices found with prefix '{prefix}'")]

            indices_text = f"Indices with prefix '{prefix}':\n"
            for index in indices_data:
                indices_text += f"- {index['index']}: {index['docs.count']} documents, {index['store.size']} size\n"

            return [types.TextContent(type="text", text=indices_text)]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    logger.debug("Starting Elasticsearch MCP server")
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.debug("Stdin/stdout streams initialized")
        logger.debug("Initializing server with capabilities")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="elasticsearch",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
    logger.debug("Server shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())

