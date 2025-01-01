from . import server
from . import client
import asyncio

def server_main():
    asyncio.run(server.main())

def client_main():
    asyncio.run(client.main())

# Optionally expose other important items at package level
__all__ = ['server_main', 'server', 'client_main', 'client']
