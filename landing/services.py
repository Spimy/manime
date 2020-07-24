import requests

API = 'https://kitsu.io/api/edge/'


def get_anime_by_season(year: str, season: str, sort: str, numPerPage: int = 5):
    query = f'anime?filter[seasonYear]={year}&filter[season]={season}&sort={sort}&page[limit]={numPerPage}'
    url = f'{API}{query}'

    response = requests.get(url)

    if response.status_code != 200:
        raise requests.HTTPError

    return response.json()
