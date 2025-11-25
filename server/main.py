from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# from pynput.keyboard import Controller
import time
import io
import qrcode

# keyboard = Controller()

app = FastAPI()
app.mount("/client", StaticFiles(directory="client"), name="client")

origins = ["http://localhost:8000"]
# origins = ["http://192.168.0.100:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins)

# ---- QRCode ----
# qr = qrcode.QRCode()
# qr.add_data("http://192.168.0.107:8000/client/index.html")
# f = io.StringIO()
# qr.print_ascii(out=f)
# f.seek(0)
# print(f.read())


@app.get("/")
def root():
    return {"message": "server running"}


# @app.post("/api/gamepad/{button_id}")
# async def handle_press(button_id):
#     # keyboard.press(button_id)
#     # time.sleep(0.5)
#     # keyboard.release(button_id)
#     return {"event": f"{button_id} pressed"}


# @app.websocket("/ws/gamepad")
# async def handle_press_ws(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             button = await websocket.receive_text()
#             # keyboard.press(button)
#             time.sleep(0.25)
#             # keyboard.release(button)
#             await websocket.send_text(f"{button} was pressed")
#     except WebSocketDisconnect:
#         await websocket.close()
#         print("client disconnected")
