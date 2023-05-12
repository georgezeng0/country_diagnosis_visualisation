# Python modules
from shiny import App
from pathlib import Path

# From local files
from app_server import server
from app_ui import app_ui

# Static assets directory containing .js and .css files
www_dir = Path(__file__).parent / "www"

# Create the application
app = App(app_ui, server, static_assets=www_dir)

