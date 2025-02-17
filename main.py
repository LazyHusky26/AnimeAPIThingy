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

def genre_recommendations(choice, genre_name):
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

    if choice == '1':
        temp = 'anime'
    elif choice == '2':
        temp = 'manga'
    else:
        print("Invalid Choice")
    
    if genre_name not in genre_ids:
        print(f"Error: Genre '{genre_name}' is not valid or not supported.")
        return

    genre_id = genre_ids[genre_name]
    response = requests.get(f"{base_url}/{temp}", params={"genres": genre_id})
    
    if response.status_code == 200:
        data = response.json()

        good_media = []
        bad_media = []
        average_media = []
        all_media = data['data']

        for temp2 in all_media:
            score = temp2['score']
            if score is not None:
                if score > 7.0:
                    good_media.append(temp2)
                elif score < 5.0:
                    bad_media.append(temp2)
                else:
                    average_media.append(temp2)
        
        print(f"\nWhich category would you like to view for the genre '{genre_name}'?")
        print(f"1. Good {temp.capitalize()}")
        print(f"2. Average {temp.capitalize()}")
        print(f"3. Random {temp.capitalize()}")

        choice = input("\nEnter the number corresponding to your choice: ")

        if choice == "1":
            category_name = f"Good {temp.capitalize()}"
            media_list = good_media
        elif choice == "2":
            category_name = f"Average {temp.capitalize()}"
            media_list = average_media
        elif choice == "3":
            category_name = f"Random {temp.capitalize()}"
            media_list = all_media
        else:
            print("Invalid choice. Please enter a valid number (1-3).")
            return
        
        while True:
            print(f"\n5 {category_name}:\n")
            for i, temp in enumerate(random.sample(media_list, min(5, len(media_list))), 1):
                print(f"{i}. {temp['title']} - Score: {temp['score']}")

            more = input("\nWould you like to see more? (y/n): ").lower()
            if more == 'n':
                break
            elif more != 'y':
                print("Invalid input.")

    else:
        print(f"Error: Could not fetch anime for genre '{genre_name}'.")

def search_char(name):
    response = requests.get(f"{base_url}/characters", params={"q": name})
    
    if response.status_code == 200:
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
                character_role = 'Role not available'
                
                if 'anime' in character and character['anime']:
                    most_popular_anime = character['anime'][0]['anime'].get('title', 'Unknown')
                    anime_list.append(most_popular_anime)
                    character_role = character['anime'][0].get('role', 'Role not available')
                
                if not anime_list:
                    anime_list.append('Unknown')

                manga_list = []
                if 'manga' in character and character['manga']:
                    most_popular_manga = character['manga'][0]['manga'].get('title', 'Unknown')
                    manga_list.append(most_popular_manga)
                
                if not manga_list:
                    manga_list.append('Unknown')

                print(f"Character: {character_name}")
                print(f"Role: {character_role}")
                print(f"Appears in (Anime): {', '.join(anime_list)}")
                print(f"Appears in (Manga): {', '.join(manga_list)}")

            else:
                print("Error: Could not fetch full data.")
        else:
            print("Character not found.")
    else:
        print(f"Error: Could not fetch character data. Status code: {response.status_code}")

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

def top_media():
    print("\nDo you want to see top anime or manga?:")
    print("1. Anime")
    print("2. Manga")
    choice = input("Enter your choice: ")

    if choice == '1':
        temp = 'anime'
    elif choice == '2':
        temp = 'manga'
    else:
        print("Invalid choice.")
        return
    
    response = requests.get(f"{base_url}/top/{temp}")

    if response.status_code == 200:
        data = response.json()
        all_anime = data['data']
        
        start_index = 0
        print(f"\nTop {temp.capitalize()}:")
        while True:
            for i, anime in enumerate(all_anime[start_index:start_index + 5], 1):
                print(f"{i}. {anime['title']}")

            more = input("\nWould you like to see more? (y/n): ").lower()
            if more == 'y':
                start_index += 5
                if start_index >= len(all_anime):
                    print("You've reached the end of the list.")
                    break
            elif more == 'n':
                break
            else:
                print("Invalid input.")
                break
    else:
        print(f"Error {response.status_code}: Could not fetch top {temp}.")

def main():
    while True:
        print("\nWhat would you like to do?")
        print("1. Anime/Manga Search")
        print("2. Anime/Manga Recommendations")
        print("3. Character Search")
        print("4. Top Anime/Manga")
        print("5. Exit")

        choice = input("\nEnter the number corresponding to your choice: ")

        if choice == '1':
            print("\n1. Anime")
            print("2. Manga")

            what = input("Enter your choice: ")

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
            print("3. Recommend by Genre") #genre kinda wonky :(

            rec_choice = input("Enter your choice: ")

            if rec_choice == '1':
                name = input("Enter Anime Name: ")
                anime_recommendations(name)
            elif rec_choice == '2':
                name = input("Enter Manga Name: ")
                manga_recommendations(name)
            elif rec_choice == '3':
                print("\n1. Anime")
                print("2. Manga")
                ch = input("Enter choice: ")
                genre = input("Enter Genre: ")
                genre_recommendations(ch, genre)
            else:
                print("Enter a valid choice")

        elif choice == '3':
            char = input("Enter Character Name: ")
            search_char(char)

        elif choice == '4':
            top_media()
        
        elif choice == '5':
            print("Exiting the program....")
            break
        
        else:
            print("Enter a valid choice")

if __name__ == "__main__":
    main()