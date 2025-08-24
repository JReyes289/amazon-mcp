# Contenido del archivo __init__.py proporcionado
from . import server
import asyncio

def main():
    """Punto de entrada principal para el paquete."""
    print("Iniciando el servidor MCP de Fewsats...")
    # Uvicorn lo gestionará cuando se ejecute a través de Docker.
    server.main()

# Opcionalmente, exponer otros elementos importantes a nivel de paquete
__all__ = ['main', 'server']
