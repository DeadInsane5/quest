from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pynput.keyboard import Controller
import time
import io
import qrcode


# ---- Player Class ----
class Player(BaseModel):
    name: str
    energy: int | None = None
    stress: int | None = None
    happiness: int | None = None


keyboard = Controller()
app = FastAPI()
app.mount("/client", StaticFiles(directory="client"), name="client")
origins = ["http://localhost:8000"]
# origins = ["http://192.168.0.100:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins)
# ---- QRCode ----
qr = qrcode.QRCode()
qr.add_data("http://192.168.0.107:8000/client/controller.html")
f = io.StringIO()
qr.print_ascii(out=f)
f.seek(0)
print(f.read())


@app.get("/")
def root():
    return {"message": "server running"}


# @app.post("/api/gamepad/{button_id}")
# async def handle_press(button_id):
#     # keyboard.press(button_id)
#     # time.sleep(0.5)
#     # keyboard.release(button_id)
#     return {"event": f"{button_id} pressed"}
@app.get("/api/profile")
async def get_profile():
    if current_player is None:
        return {"error": "No profile created yet"}
    return current_player


@app.post("/api/profile/create_profile")
async def create_profile(player: Player):
    player.energy = 10
    player.stress = 10
    player.happiness = 10
    global current_player
    current_player = player
    print(player)
    return player


@app.patch("/api/profile")
async def update_profile(updates: dict):
    global current_player
    if current_player is None:
        return {"error": "No profile exists"}
    if "energy" in updates:
        current_player.energy = updates["energy"]
    if "stress" in updates and current_player.stress > 0:
        current_player.stress = updates["stress"]
    if "happiness" in updates:
        current_player.happiness = updates["happiness"]
    if "name" in updates:
        current_player.name = updates["name"]
    return current_player


@app.websocket("/ws/gamepad")
async def handle_press_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            button = await websocket.receive_text()
            keyboard.press(button)
            time.sleep(0.25)
            keyboard.release(button)
            await websocket.send_text(f"{button} was pressed")
            print(f"{button} was pressed")
    except WebSocketDisconnect:
        await websocket.close()
        print("client disconnected")
