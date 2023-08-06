from rich.console import Console
from rich.table import Table

console = Console()


def waffle_baker(data: dict) -> None:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Ingredient", style="dim", width=58)
    table.add_column("Amount", justify="right", width=28)
    console.print(f'Dish of Coder: [blue] {data["dish"]} [blue]')
    for key, value in data["shopping list"].items():
        table.add_row(key, value)
    console.print(table)
