import asyncio
import websockets
from websockets import ServerConnection


async def handler(websocket: ServerConnection):
    async for message in websocket:
        print(f"Получено сообщение от пользователя: {message}")
        for i in range(1, 6):
            await websocket.send(f"{i} Сообщение пользователя: {message}")


async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocket сервер запущен на ws://localhost:8765")
    await server.wait_closed()


asyncio.run(main())