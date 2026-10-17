import requests
from database import db_create_pokemon_table, db_insert_pokemon

def load_pokemon():
    db_create_pokemon_table()

    # Recolecto todos los pokemones, con un timeout de 30s
    url = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1000"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    # La respuesta es json, así que tomo los objetos en "results"
    pokemon = response.json()["results"]

    # Número de pokemones
    total = len(pokemon)

    for i, p in enumerate(pokemon):
        id = int(p["url"].strip("/").split("/")[-1])
        image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"

        db_insert_pokemon(id, p["name"], image)
        print(f"{i/total * 100:.2f} %")

if __name__ == "__main__":
    load_pokemon()