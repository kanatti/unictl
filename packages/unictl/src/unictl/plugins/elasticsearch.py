import httpx
from unictl.plugins.base import PluginBase

class ElasticsearchPlugin(PluginBase):
    def __init__(self, base_url="http://localhost:9200"):
        self.base_url = base_url

    def get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "get-cluster-health",
                    "description": "Get health of Elasticsearch cluster",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get-indices",
                    "description": "Get indices present on the Elasticsearch cluster",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prefix": {
                                "type": "string",
                                "description": "Prefix to match indices by.",
                            },
                        },
                        "required": ["prefix"],
                    }
                }
            }
        ]

    def run_tool(self, tool_name, **kwargs):
        if tool_name == "get-cluster-health":
            return self._make_request("/_cluster/health")
        elif tool_name == "get-indices":
            prefix = kwargs.get("prefix", "")
            indices = self._make_request(f"/_cat/indices/{prefix}*?format=json")
            return indices
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def _make_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        try:
            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            raise ValueError(f"An error occurred while requesting {e.request.url!r}.")
