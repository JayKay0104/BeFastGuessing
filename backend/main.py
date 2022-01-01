from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils.helpers import check_if_client_authenticated
from utils.access_manager import return_client
from static.settings import CATEGORIES
from fastapi.middleware.cors import CORSMiddleware
from utils.helpers import filter_playlists, filter_tracks, create_game
import time
import json
import config


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
    """ returns up to 50 plalists of a category """
    check_if_client_authenticated(client=app.client)
    playlists = app.client.category_playlists(
        category_id=category_id, limit=50, offset=0)
    filtered_playlists = filter_playlists(playlists=playlists)
    return JSONResponse(content=filtered_playlists)


@app.get("/playlists/{playlist_id}/tracks")
async def tracks(playlist_id: str) -> JSONResponse:
    """ returns up to 50 songs of a playlist"""
    check_if_client_authenticated(client=app.client)
    tracks = app.client.playlist_tracks(
        playlist_id=playlist_id, limit=50, offset=0, market='DE')
    filtered_tracks = filter_tracks(tracks=tracks)
    return JSONResponse(content=filtered_tracks)


@app.get("/game/{playlist_id}")
async def game(playlist_id: str) -> JSONResponse:
    """ returns the game filled with sample of tracks from playlist """
    check_if_client_authenticated(client=app.client)
    tracks = app.client.playlist_tracks(
        playlist_id=playlist_id, limit=50, offset=0, market='DE')
    tracks = filter_tracks(tracks=tracks)
    create_game(tracks=tracks)
    return JSONResponse(content=config.GAME)


@app.get("/start/{game_data}")
async def results(game_data: str) -> JSONResponse:
    config.GAME_START_TIME = time.time()
    config.CORRECT_SONG_NR = game_data
    return JSONResponse(content=config.GAME_START_TIME)


@app.get("/result/{player_data}")
async def results(player_data: str) -> JSONResponse:
    player_data = json.loads(player_data)
    print(player_data)
    print(config.GAME_START_TIME)
    points = 0
    if player_data['song'] == config.CORRECT_SONG_NR:
        start = config.GAME_START_TIME
        end = time.time()
        difference = (end-start)
        print(difference)
        points = 50 if difference > 20 else 100 - 2.5*difference
    return JSONResponse(content=points)
