import requests
import random

base_url = "https://api.jikan.moe/v4"

def search_anime(name):
    response = requests.get(f"{base_url}/anime", params={"q": name})

    if response.status_code == 200:
        data = response.json()
        anime = data['data'][0]
        genres = [genre['name'] for genre in anime['genres']]
        themes = [theme['name'] for theme in anime['themes']]

        print(f"Title: {anime['title']}")
        print(f"Type: {anime['type']}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Themes: {', '.join(themes)}")
    else:
        print("Error: Could not fetch data")
    
    #anime_recommendations(data)

def anime_recommendations(data):
    anime_id = data['data'][0]['mal_id']
    response = requests.get(f"{base_url}/anime/{anime_id}/recommendations")

    if response.status_code == 200:
        recommendations_data = response.json()
        recommendations = recommendations_data['data']

        print(f"Anime Recommendations for '{name}':")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{i}. {rec['entry']['title']}")
    else:
        print(f"Error: Could not fetch recommendations for anime ID {anime_id}")

def genre_recommendations(genre_name):
    genre_ids = {
        "Action": 1,
        "Adventure": 2,
        "Cars": 3,
        "Comedy": 4,
        "Dementia": 5,
        "Demons": 6,
        "Drama": 8,
        "Ecchi": 9,
        "Fantasy": 10,
        "Game": 11,
        "Harem": 12,
        "Historical": 13,
        "Horror": 14,
        "Josei": 15,
        "Kids": 16,
        "Magic": 17,
        "Martial Arts": 18,
        "Mecha": 19,
        "Military": 20,
        "Music": 21,
        "Mystery": 22,
        "Psychological": 23,
        "Romance": 24,
        "Samurai": 25,
        "School": 26,
        "Seinen": 27,
        "Shounen": 28,
        "Slice of Life": 29,
        "Space": 30,
        "Sports": 31,
        "Super Power": 32,
        "Supernatural": 33,
        "Thriller": 34,
        "Vampire": 35
    }

    if genre_name not in genre_ids:
        print(f"Error: Genre '{genre_name}' is not valid or not supported.")
        return

    genre_id = genre_ids[genre_name]
    response = requests.get(f"{base_url}/anime", params={"genres": genre_id})
    
    if response.status_code == 200:
        data = response.json()

        good_anime = []
        bad_anime = []
        average_anime = []
        all_anime = data['data']

        for anime in all_anime:
            score = anime['score']
            if score is not None:
                if score > 7.0:
                    good_anime.append(anime)
                elif score < 5.0:
                    bad_anime.append(anime)
                else:
                    average_anime.append(anime)
        
        print(f"\nWhich category would you like to view for the genre '{genre_name}'?")
        print("1. Good Anime)")
        print("2. Average Anime")
        print("3. Random Anime")

        choice = input("\nEnter the number corresponding to your choice: ")

        if choice == "1":
            category_name = "Good Anime"
            anime_list = good_anime
        elif choice == "2":
            category_name = "Average Anime"
            anime_list = average_anime
        elif choice == "3":
            category_name = "Random Anime"
            anime_list = all_anime
        else:
            print("Invalid choice. Please enter a valid number (1-4).")
            return
        
        print(f"\n5 {category_name}:\n")
        for i, anime in enumerate(random.sample(anime_list, min(5, len(anime_list))), 1):
            print(f"{i}. {anime['title']} - Score: {anime['score']}")

    else:
        print(f"Error: Could not fetch anime for genre '{genre_name}'.")

#def

name = input("Enter the name: ")
#search_anime(name)
genre_recommendations(name)
