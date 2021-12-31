from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from utils.access_manager import return_client
from static.settings import CATEGORIES
from fastapi.middleware.cors import CORSMiddleware
from utils.helpers import filter_playlists, filter_tracks
import json

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
