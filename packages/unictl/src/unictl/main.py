import click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from litellm import completion
import os
import json
from unictl.plugins.base import PluginBase
from unictl.plugins.elasticsearch import ElasticsearchPlugin

console = Console()
active_plugin = None
active_client = None

def yellow_italic(text):
    return Text(text, style="yellow italic")

def system_info(text):
    console.print(yellow_italic(text))

# This is a placeholder for available plugins and their descriptions.
# In a real implementation, this would be dynamically populated based on installed plugins.
AVAILABLE_PLUGINS = {
    "elasticsearch": "Manage and query Elasticsearch clusters",
    "kubernetes": "Orchestrate and manage Kubernetes resources",
    "docker": "Build, run, and manage Docker containers",
    "aws": "Control and monitor AWS cloud services"
}

@click.command()
@click.option('--plugin', '-p', type=click.Choice(list(AVAILABLE_PLUGINS.keys())), help='Activate a specific plugin on startup')
def main(plugin):
    global active_plugin, active_client
    console.print(Panel("Unictl: AI-powered unified control for your systems", expand=False))
    system_info("Tip: Type '/help' to see available commands.")

    if plugin:
        activate_plugin(plugin)

    while True:
        prompt = f"[bold cyan]unictl{':' + active_plugin if active_plugin else ''}>[/bold cyan] "
        user_input = Prompt.ask("\n" + prompt)
        
        if not user_input.strip():
            continue
        elif user_input.lower() == 'exit':
            break
        elif user_input.startswith('/'):
            handle_command(user_input)
        else:
            process_input(user_input)

def activate_plugin(plugin):
    global active_plugin, active_client
    if plugin in AVAILABLE_PLUGINS:
        active_plugin = plugin
        if plugin == "elasticsearch":
            active_client = ElasticsearchPlugin()
        system_info(f"Activated plugin: {plugin}")
    else:
        system_info(f"Plugin '{plugin}' not found.")

def handle_command(command):
    global active_plugin, active_client
    if command.startswith('/activate'):
        _, plugin = command.split(maxsplit=1)
        activate_plugin(plugin)
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
            console.print("─" * console.width)  # Add a line before each prompt
            console.print(message.content)
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = tool_call.function.arguments
                    console.print(f"[yellow]Calling tool -- {function_name}[/yellow]")
                    
                    try:
                        parsed_args = json.loads(arguments)
                        result = active_client.run_tool(function_name, **parsed_args)
                        if isinstance(result, (dict, list)):
                            pretty_json = json.dumps(result, indent=2)
                            syntax = Syntax(pretty_json, "json", theme="monokai", line_numbers=True)
                            console.print(Panel(syntax, title="Tool Output", expand=False))
                        else:
                            console.print(Panel(str(result), title="Tool Output", expand=False))
                    except json.JSONDecodeError:
                        console.print("[red]Error: Invalid JSON in tool arguments[/red]")
                    except Exception as e:
                        console.print(f"[red]Error executing tool: {str(e)}[/red]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
    else:
        system_info("Please activate a plugin first using /activate <plugin_name>")

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
