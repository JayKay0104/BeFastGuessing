from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse
from utils.helpers import check_if_client_authenticated
from utils.access_manager import return_client
from static.settings import CATEGORIES
from fastapi.middleware.cors import CORSMiddleware
from utils.helpers import filter_playlists, filter_tracks, create_game
import time
import json
import config
from pydantic import BaseModel
from typing import List


class Result(BaseModel):
    songID: str
    playerID: int
    round: int

# Main

app = FastAPI()
app.client = None

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://192.168.3.5:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/login")
async def login() -> JSONResponse:
    # we store the spotipy client in app.client to be able to access it globally
    app.client = return_client()
    # return the user object of the logged in user
    return JSONResponse(app.client.me())


@app.get("/categories")
async def categories() -> JSONResponse:
    return JSONResponse(content=CATEGORIES)


@app.get("/playlists/{category_id}")
async def playlists(category_id: str) -> JSONResponse:
    """ returns up to 50 plalists of a category """
    check_if_client_authenticated(client=app.client)
    playlists = app.client.category_playlists(
        category_id=category_id, limit=50, offset=0)
    filtered_playlists = filter_playlists(playlists=playlists)
    return JSONResponse(content=filtered_playlists)


@app.get("/game/{playlist_id}")
async def game(playlist_id: str) -> JSONResponse:
    """ returns the game filled with sample of tracks from playlist """
    check_if_client_authenticated(client=app.client)
    tracks = app.client.playlist_tracks(
        playlist_id=playlist_id, limit=50, offset=0, market='DE')
    tracks = filter_tracks(tracks=tracks)
    create_game(tracks=tracks)
    await notifier.send_json({'game':config.GAME})
    return JSONResponse(content=config.GAME)


@app.get("/start/{game_data}")
async def results(game_data: str) -> JSONResponse:
    print(game_data)
    config.GAME_START_TIME = time.time()
    config.CORRECT_SONG_ID = game_data
    if len(config.RESULT[1]) == 0:
        await notifier.send_json({'start':config.GAME_START_TIME})
    else:
        await notifier.send_json({'change_round':config.GAME_START_TIME})
        print(len(config.RESULT[1]))
    print(config.CORRECT_SONG_ID)
    return JSONResponse(content=config.GAME_START_TIME)


@app.post("/result/")
async def results(result: Result) -> JSONResponse:
    song_id = result.songID
    player_id = result.playerID
    round = result.round
    round_name = "Round_"+str(round)
    print(song_id)
    print(player_id)
    print(round)
    print(config.CORRECT_SONG_ID)
    points = 0
    if song_id == config.CORRECT_SONG_ID:
        start = config.GAME_START_TIME
        end = time.time()
        difference = (end-start)
        print(difference)
        points = 50 if difference > 20 else 100 - 2.5*difference
    config.RESULT[player_id][round_name] = points
    notifier.send_json({'result':config.RESULT})
    print(config.RESULT)
    return JSONResponse(content=config.RESULT)


# TODO:
# Add Websockets which push messages to the player clients when the game and rounds start 

class Notifier:

    def __init__(self):
        self.connections: List[WebSocket] = []

    async def send_json(self, json_data):
        for sockets_connection in self.connections:
            await sockets_connection.send_json(json_data)
            print("send data to {}".format(sockets_connection))


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

notifier = Notifier()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            #await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)