from jikanpy import Jikan
from models import Anime, db

jikan = Jikan()

# Function to fetch current season animes
def fetch_season_animes(year=2024, season='now', page='1'):
    
    season_now = jikan.seasons(extension=season, 
                               page=page, 
                               parameters={'filter': 'tv'})
    anime_list = []
    for anime in season_now['data']:
        new_anime = {
            'mal_id' : anime['mal_id'],
            'title' : anime['title'],
            'score' : anime.get('score', 'N/A'),
            'synopsis' : anime['synopsis'],
            'url' : anime['url'],
            'img_url' : anime['images']['jpg']['image_url']
        }
        anime_list.append(new_anime)
    
    
    return anime_list
       

# Function to search for an anime by name
# def search_anime(name):
#     search = jikan.search(search_type='anime', query=name, parameters={'type': 'tv'})
#     anime_list = []
#     for anime in search['data']:
#         new_anime = {
#             'ani_id': anime['mal_id'],
#             'title': anime['title'],
#             'score': anime.get('score', 'N/A'),
#             'img': anime['images']['jpg']['image_url']
#         }
#         anime_list.append(new_anime)
        
#     return anime_list

