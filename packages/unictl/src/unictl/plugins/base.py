from abc import ABC, abstractmethod

class PluginBase(ABC):
    @abstractmethod
    def get_tools(self):
        """Return a list of available tools for the plugin."""
        pass

    @abstractmethod
    def run_tool(self, tool_name, **kwargs):
        """Run a specific tool with the given arguments."""
        pass
