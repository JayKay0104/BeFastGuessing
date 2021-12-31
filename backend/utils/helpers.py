from typing import List, Dict, Union, Any


def filter_playlists(playlists: Dict[str, Union[str, List[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
    """returns a list of playlists with only the required fields

    Args:
        playlists (Dict[str, Union[str, List[Dict[str,]]]]): the playlists returned from spotify

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
    return [f(el) for el in items]


def filter_tracks(tracks: Dict[str, Union[str, List[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
    items = tracks["items"]

    def f(e):
        return {
            'title': e['track']['name'],
            'preview_url': e['track']['preview_url'],
            'artist': e['track']['artists'][0]['name']
        }
    return [f(el) for el in items]