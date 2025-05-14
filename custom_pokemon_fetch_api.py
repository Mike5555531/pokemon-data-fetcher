import requests

def get_pokemon_data(pokemon_name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"Name: {data['name'].capitalize()}")
        print(f"ID: {data['id']}")
        print(f"Height: {data['height']}")
        print(f"Weight: {data['weight']}")
        types = ', '.join([t['type']['name'] for t in data['types']])
        print(f"Types: {types}")
        abilities = ', '.join([a['ability']['name'] for a in data['abilities']])
        print(f"Abilities: {abilities}")
        print(f"Sprite URL: {data['sprites']['front_default']}")
    except requests.exceptions.HTTPError:
        print("Pokémon not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
get_pokemon_data('pikachu')
