import click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()
active_plugin = None

@click.command()
def main():
    """Unictl: AI-powered unified control for your systems."""
    console.print(Panel("Unictl: AI-powered unified control for your systems", expand=False))

    while True:
        prompt = f"[bold]unictl{':' + active_plugin if active_plugin else ''}>[/bold]"
        user_input = Prompt.ask("\n" + prompt)
        
        if user_input.lower() == 'exit':
            break
        elif user_input.startswith('/'):
            handle_command(user_input)
        else:
            process_input(user_input)

def handle_command(command):
    global active_plugin
    if command.startswith('/activate'):
        _, plugin = command.split(maxsplit=1)
        active_plugin = plugin
        console.print(f"[green]Activated plugin: {plugin}[/green]")
    elif command == '/help':
        show_help()
    else:
        console.print(f"[red]Unknown command: {command}[/red]")

def process_input(user_input):
    console.print(f"[italic]Processing: {user_input}[/italic]")
    console.print("This is a placeholder response.")

def show_help():
    help_text = """
    Available commands:
    /activate <plugin>  - Activate a specific plugin
    /help               - Show this help message
    exit                - Exit the program
    """
    console.print(Panel(help_text, title="Help", expand=False))

if __name__ == "__main__":
    main()
