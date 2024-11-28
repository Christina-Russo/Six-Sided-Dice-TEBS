from fastapi import WebSocket, FastAPI, WebSocketDisconnect, HTTPException, Request
from asyncio import Event, exceptions
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

"""
The object that the server recognises in the post request. Not sure why it works but it does.
"""
class Item(BaseModel):
    name: str

app = FastAPI()

# Event that keeps clients connected?
has_new_data = Event()

last_data_received: str = ""

# Global list of connections
connections: list[WebSocket] = []

# Not sure what this does. Might assist in keeping clients connected
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Send given data string to all connected clients
async def broadcast(data: str) -> None:
    #print("Broadcasting to", len(connections), "clients")

    for client in connections:
        #print("sending data to:", client)
        try:
            await client.send_text(data)

        except RuntimeError:
            print("RuntimeError")

        except WebSocketDisconnect:
            print("Client:", await disconnect(client), "has Disconnected")

#async def update(data: str) -> None:
#    stored_data = data
#    await broadcast(data)

# Adds client to list of connections
async def connect(websocket: WebSocket) -> None:
    connections.append(websocket)

# Removes client from list of connections. Don't think .remove can find specific client... may need dictionary of ids -> websockets
async def disconnect(client: WebSocket) -> None:
    connections.remove(client)

# Entrypoint for backend to update data to be displayed. Hacky and janky, but I was able to get this working.
@app.post("/post/")
async def create_item(request: Request):
    await broadcast(await request.body())


@app.get("/")
async def get():
    return last_data_received

# Client connection point
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await connect(websocket)

    # Tries to stop client from disconnecting. Might work?
    while True:
        try: 
            await has_new_data.wait()
        except exceptions.CancelledError:
            return