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

        print(f"\nTitle: {anime['title']}")
        print(f"Type: {anime['type']}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Themes: {', '.join(themes)}")
    else:
        print("Error: Could not fetch data")

def anime_recommendations(name):
    response = requests.get(f"{base_url}/anime", params={"q": name})
    data = response.json()

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

def manga_recommendations(name):
    response = requests.get(f"{base_url}/manga", params={"q": name})
    data = response.json()

    manga_id = data['data'][0]['mal_id']
    response = requests.get(f"{base_url}/manga/{manga_id}/recommendations")

    if response.status_code == 200:
        recommendations_data = response.json()
        recommendations = recommendations_data['data']

        print(f"Manga Recommendations for '{name}':")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{i}. {rec['entry']['title']}")
    else:
        print(f"Error: Could not fetch recommendations for anime ID {manga_id}")

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
        print("1. Good Anime")
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
            print("Invalid choice. Please enter a valid number (1-3).")
            return
        
        print(f"\n5 {category_name}:\n")
        for i, anime in enumerate(random.sample(anime_list, min(5, len(anime_list))), 1):
            print(f"{i}. {anime['title']} - Score: {anime['score']}")

    else:
        print(f"Error: Could not fetch anime for genre '{genre_name}'.")

def search_char(name):
    response = requests.get(f"{base_url}/characters", params={"q": name})
    data = response.json()

    if data['data']:
        character = data['data'][0]
        character_id = character['mal_id']
        print(f"Character found: {character['name']} (ID: {character_id})")

        response = requests.get(f"{base_url}/characters/{character_id}/full")

        if response.status_code == 200:
            data = response.json()
            character = data['data']
            character_name = character['name']

            anime_list = []
            if 'anime' in character:
                most_popular_anime = character['anime'][0]['anime'].get('title', 'Unknown')
                anime_list.append(most_popular_anime)
                character_role = character['anime'][0].get('role', 'Role not available')
            if not anime_list:
                anime_list.append('Unknown')

            manga_list = []
            if 'manga' in character:
                most_popular_manga = character['manga'][0]['manga'].get('title', 'Unknown')
                manga_list.append(most_popular_manga)
            if not manga_list:
                manga_list.append('Unknown')

            print(f"Character: {character_name}")
            print(f"Role: {character_role}")
            print(f"Appears in (Anime): {', '.join(anime_list)}")
            print(f"Appears in (Manga): {', '.join(manga_list)}")

        else:
            print("Error: Could not fetch full data")
    else:
        print("Character not found.")

def search_manga(name):
    response = requests.get(f"{base_url}/manga", params={"q": name})

    if response.status_code == 200:
        data = response.json()
        manga = data['data'][0]
        genres = [genre['name'] for genre in manga['genres']]
        themes = [theme['name'] for theme in manga['themes']]

        print(f"\nTitle: {manga['title']}")
        print(f"Type: {manga['type']}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Themes: {', '.join(themes)}")
    else:
        print("Error: Could not fetch data")

def main():
    while True:
        print("\nWhat would you like to do?")
        print("1. Anime/Manga Search")
        print("2. Anime/Manga Recommendations")
        print("3. Character Search")
        print("4. Exit")

        choice = input("\nEnter the number corresponding to your choice: ")

        if choice == '1':
            print("\n1. Anime")
            print("2. Manga")

            what = input("\nEnter your choice: ")

            if what == '1':
                name = input("Enter Anime name: ")
                search_anime(name)
            elif what == '2':
                name = input("Enter Manga name: ")
                search_manga(name)
            else:
                print("Enter a valid choice")

        elif choice == '2':
            print("\n1. Recommend by Anime")
            print("2. Recommend by Manga")
            print("3. Recommend by Genre") #genre kinda broken :(

            rec_choice = input("\nEnter your choice: ")

            if rec_choice == '1':
                name = input("Enter Anime Name: ")
                anime_recommendations(name)
            elif rec_choice == '2':
                name = input("Enter Manga Name: ")
                manga_recommendations(name)
            elif rec_choice == '3':
                genre = input("Enter Genre: ")
                genre_recommendations(genre)
            else:
                print("Enter a valid choice")

        elif choice == '3':
            char = input("Enter Character Name: ")
            search_char(char)

        elif choice == '4':
            print("Exiting the program....")
            break
        else:
            print("Enter a valid choice")

if __name__ == "__main__":
    main()