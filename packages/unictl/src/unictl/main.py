import click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from litellm import completion
import os

console = Console()
active_plugin = None
active_client = None

# This is a placeholder for available plugins and their descriptions.
# In a real implementation, this would be dynamically populated based on installed plugins.
AVAILABLE_PLUGINS = {
    "elasticsearch": "Manage and query Elasticsearch clusters",
    "kubernetes": "Orchestrate and manage Kubernetes resources",
    "docker": "Build, run, and manage Docker containers",
    "aws": "Control and monitor AWS cloud services"
}

class ElasticsearchClient:
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

@click.command()
def main():
    global active_plugin, active_client
    console.print(Panel("Unictl: AI-powered unified control for your systems", expand=False))
    console.print("[yellow italic]Tip: Type '/help' to see available commands.[/yellow italic]")

    while True:
        prompt = f"[bold]unictl{':' + active_plugin if active_plugin else ''}>[/bold]"
        user_input = Prompt.ask("\n" + prompt)
        
        if not user_input.strip():
            continue
        elif user_input.lower() == 'exit':
            break
        elif user_input.startswith('/'):
            handle_command(user_input)
        else:
            process_input(user_input)

def handle_command(command):
    global active_plugin, active_client
    if command.startswith('/activate'):
        _, plugin = command.split(maxsplit=1)
        if plugin in AVAILABLE_PLUGINS:
            active_plugin = plugin
            if plugin == "elasticsearch":
                active_client = ElasticsearchClient()
            console.print(f"[green]Activated plugin: {plugin}[/green]")
        else:
            console.print(f"[red]Plugin '{plugin}' not found.[/red]")
    elif command == '/help':
        show_help()
    elif command == '/list':
        list_plugins()
    else:
        console.print(f"[red]Unknown command: {command}[/red]")

def process_input(user_input):
    global active_plugin, active_client
    if active_plugin and active_client:
        tools = active_client.get_tools()
        try:
            response = completion(
                model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
                messages=[
                    {"role": "system", "content": f"You are an AI assistant for the {active_plugin} plugin. Use the provided tools to help the user."},
                    {"role": "user", "content": user_input}
                ],
                tools=tools,
                tool_choice="auto"
            )
            message = response['choices'][0]['message']
            console.print(message.content)
            if message.tool_calls:
                console.print("[yellow]Tool Calls:[/yellow]")
                for tool_call in response['choices'][0]['message']['tool_calls']:
                    console.print(f"Function: {tool_call['function']['name']}")
                    console.print(f"Arguments: {tool_call['function']['arguments']}")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
    else:
        console.print("[yellow]Please activate a plugin first using /activate <plugin_name>[/yellow]")

def show_help():
    help_text = """
    Available commands:
    /activate <plugin>  - Activate a specific plugin
    /list               - List all available plugins
    /help               - Show this help message
    exit                - Exit the program
    """
    console.print(Panel(help_text, title="Help", expand=False))

def list_plugins():
    table = Table(show_header=False)
    table.add_column(style="cyan")
    table.add_column(style="magenta")
    
    for plugin, description in AVAILABLE_PLUGINS.items():
        name = f"{plugin} (*)" if plugin == active_plugin else plugin
        table.add_row(name, description)
    
    console.print(table)

if __name__ == "__main__":
    main()
