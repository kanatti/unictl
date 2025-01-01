import click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

console = Console()
active_plugin = None

# This is a placeholder for available plugins and their descriptions.
# In a real implementation, this would be dynamically populated based on installed plugins.
AVAILABLE_PLUGINS = {
    "elasticsearch": "Manage and query Elasticsearch clusters",
    "kubernetes": "Orchestrate and manage Kubernetes resources",
    "docker": "Build, run, and manage Docker containers",
    "aws": "Control and monitor AWS cloud services"
}

@click.command()
def main():
    """Unictl: AI-powered unified control for your systems."""
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
    global active_plugin
    if command.startswith('/activate'):
        _, plugin = command.split(maxsplit=1)
        if plugin in AVAILABLE_PLUGINS:
            active_plugin = plugin
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
    console.print(f"[italic]Processing: {user_input}[/italic]")
    console.print("This is a placeholder response.")

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
