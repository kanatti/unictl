Use client script to test server:

```
❯ uv run --package uni-elasticsearch client
2025-01-01 16:30:37,041 - DEBUG - Initializing server 'elasticsearch'
2025-01-01 16:30:37,041 - DEBUG - Registering handler for ListToolsRequest
2025-01-01 16:30:37,041 - DEBUG - Registering handler for CallToolRequest
2025-01-01 16:30:37,041 - DEBUG - Using selector: KqueueSelector
2025-01-01 16:30:37,270 - DEBUG - Initializing server 'elasticsearch'
2025-01-01 16:30:37,270 - DEBUG - Registering handler for ListToolsRequest
2025-01-01 16:30:37,270 - DEBUG - Registering handler for CallToolRequest
2025-01-01 16:30:37,271 - DEBUG - Using selector: KqueueSelector
2025-01-01 16:30:37,271 - DEBUG - Starting Elasticsearch MCP server
2025-01-01 16:30:37,274 - DEBUG - Stdin/stdout streams initialized
2025-01-01 16:30:37,274 - DEBUG - Initializing server with capabilities
2025-01-01 16:30:37,276 - DEBUG - Received message: root=InitializedNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
2025-01-01 16:30:37,276 - DEBUG - Received message: <mcp.shared.session.RequestResponder object at 0x11816ad20>
2025-01-01 16:30:37,276 - INFO - Processing request of type ListToolsRequest
2025-01-01 16:30:37,276 - DEBUG - Dispatching request of type ListToolsRequest
2025-01-01 16:30:37,277 - DEBUG - Response sent

Connected to server. Available tools:
- get-cluster-health: Get health of Elasticsearch cluster
  Input schema: {'type': 'object', 'properties': {}, 'required': []}
- get-indices: Get indices present on the Elasticsearch cluster
  Input schema: {'type': 'object', 'properties': {'prefix': {'type': 'string', 'description': 'Prefix to match indices by.'}}, 'required': ['prefix']}
2025-01-01 16:30:37,279 - DEBUG - Server shutdown complete
```