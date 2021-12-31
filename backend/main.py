from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from utils.access_manager import return_client
from static.settings import CATEGORIES
from fastapi.middleware.cors import CORSMiddleware
from utils.helpers import filter_playlists, filter_tracks
import time
import json

# Global Variables
CORRECT_SONG_NR = None
GAME_START_TIME = None
DATE_FORMAT_STR = '%d/%m/%Y %H:%M:%S.%f'

# Main 

app = FastAPI()
app.client = None

origins = [
    "http://localhost",
    "http://localhost:3000",
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
    """"""
    if app.client is None:
        raise HTTPException(status_code=401, detail="First login needed.")
    playlists = app.client.category_playlists(
        category_id=category_id, limit=50, offset=0)
    filtered_playlists = filter_playlists(playlists=playlists)
    return JSONResponse(content=filtered_playlists)

@app.get("/playlists/{playlist_id}/tracks")
async def tracks(playlist_id: str) -> JSONResponse:
    """"""
    if app.client is None:
        raise HTTPException(status_code=401, detail="First login needed.")
    tracks = app.client.playlist_tracks(
        playlist_id=playlist_id, limit=50, offset=0, market='DE')
    filtered_tracks = filter_tracks(tracks = tracks)
    #print(filtered_tracks)
    return JSONResponse(content=filtered_tracks)

@app.get("/start/{game_data}")
async def results(game_data: str) -> JSONResponse:
    global GAME_START_TIME, CORRECT_SONG_NR
    GAME_START_TIME = time.time()
    CORRECT_SONG_NR = game_data
    return JSONResponse(content=GAME_START_TIME)


@app.get("/result/{player_data}")
async def results(player_data: str) -> JSONResponse:
    global CORRECT_SONG_NR, GAME_START_TIME
    player_data = json.loads(player_data)
    print(player_data)
    print(GAME_START_TIME)
    points = 0
    if player_data['song'] == CORRECT_SONG_NR:
        start = GAME_START_TIME
        end = time.time()
        difference = (end-start)
        print(difference)
        if difference > 20:
            points = 50
        else:
            points = 100 - 2.5*difference

    return JSONResponse(content=points)