from rich.console import Console
from rich.traceback import install
from rich.theme import Theme

install()
# Rich Theme
fwtheme = Theme({"success": "green", "error": "bold red"})

# Rich console handle
console = Console(theme=fwtheme)
