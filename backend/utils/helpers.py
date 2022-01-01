from typing import List, Dict, Union, Any
from fastapi.exceptions import HTTPException
import spotipy
import random
import config


def filter_playlists(playlists: Dict[str, Union[str, List[Dict[str, Any]]]], min_number_of_tracks: int = 32) -> List[Dict[str, Any]]:
    """returns a list of playlists with only the required fields

    Args:
        playlists (Dict[str, Union[str, List[Dict[str,]]]]): the playlists returned from spotify
        min_number_of_tracks (int): the minimum number of tracks the playlist should contain. Defaults to 32 (means min 8 rounds)

    Returns:
        List[Dict[str, Any]]: the filtered playlist
    """

    items = playlists["playlists"]["items"]

    def f(e):
        return {
            "id": e["id"],
            "name": e["name"],
            "description": e["description"],
            "href": e["href"],
            "tracks": e["tracks"]["href"],
            "number_of_tracks": e["tracks"]["total"],
            "uri": e["uri"],
            "image": e["images"][0]["url"]
        }
    return [f(el) for el in items if el["tracks"]["total"] > min_number_of_tracks]


def filter_tracks(tracks: Dict[str, Union[str, List[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
    """filters the required info from the tracks data returned from spotify api

    Args:
        tracks (Dict[str, Union[str, List[Dict[str, Any]]]]): the dict containting the tracks returned by the spotify endpoint

    Returns:
        List[Dict[str, Any]]: filtered tracks
    """
    items = tracks["items"]

    def f(e):
        return {
            'id': e['track']['id'],
            'title': e['track']['name'],
            'preview_url': e['track']['preview_url'],
            'artist': e['track']['artists'][0]['name'],
            'artist_title': f"{e['track']['artists'][0]['name']} - {e['track']['name']}"
        }
    return [f(el) for el in items]


def create_game(tracks: Dict[str, Union[str, List[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
    """ first resets the variable GAME and then fills it with sample of tracks """
    # reset global variable GAME
    config.reset_game()
    fill_game_with_k_samples_of_n_tracks(tracks=tracks)


def fill_game_with_k_samples_of_n_tracks(tracks: List[Dict[str, Any]], k: int = 10, n: int = 4) -> None:
    """ fills the global variable GAME from config with k games containing 
    a sample of n (defaults to 4) tracks from list of tracks """
    # shuffle the list
    random.shuffle(tracks)
    len_tracks = len(tracks)
    # check if we can create k samples of size 4
    if len_tracks <= k*n:
        # set k to the maximum amount of samples of size n for the size of tracks
        k = len_tracks // n
    # create the k samples
    for i in range(k):
        # create a random number between 0 and 3
        # that is used to pick the song that should be played
        idx = random.randint(0, 3)
        sample = tracks[-n:]
        # store the selected i.e. the song that shall be played and the sample in config.GAME
        config.GAME[f"Round_{i+1}"] = {
            "selected": sample[idx],
            "sample": sample
        }
        # remove the sample from the tracks
        del tracks[-n:]


def check_if_client_authenticated(client: Union[None, spotipy.Spotify]) -> None:
    """ checks if client is already authenticated if not raises HTTPException """
    if client is None:
        raise HTTPException(status_code=401, detail="First login needed.")
