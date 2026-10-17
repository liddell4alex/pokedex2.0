from fastapi import FastAPI, Request
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

from database import db_connect, db_insert_pokemon, db_delete_pokemon, db_update_pokemon

from pydantic import BaseModel

# Ruta de los templates
templates = Jinja2Templates(directory='templates')

# Instancia fastapi y pokeapi
app = FastAPI()

# Modelo base para los atributos de los pokemones
class NewPokemon(BaseModel):
    name: str
    image: str

# URL principal
@app.get("/")
def inicio(_request: Request):
    conn = db_connect()

    try:
        pokemon = conn.execute("SELECT * FROM pokemon").fetchall()  # Obtiene todos los registros encontrados

    finally:
        conn.close()

    return templates.TemplateResponse(
        request=_request,
        name="index.html",
        context={"pokemon": [dict(p) for p in pokemon]}
    )

@app.post("/post")
def insert_pokemons(_pokemon: NewPokemon):
    try:
        db_insert_pokemon(None, _pokemon.name, _pokemon.image)

    except Exception as e:
        print(f"Error: {e}")

    return {
        "mensaje": "Pokemon agregado correctamente",
        "pokemon": _pokemon
    }

@app.delete("/delete/{pokemon_id}")
def delete_pokemons(pokemon_id: int):
    delete = db_delete_pokemon(pokemon_id)

    if not delete:
        raise HTTPException(
            status_code=404,
            detail="No existe un pokemón con ese id"
        )

    return {
        "mensaje": "Pokemón eliminado correctamente",
        "id": pokemon_id 
    }

@app.put("/put/{pokemon_id}")
def update_pokemons(pokemon_id: int, _pokemon: NewPokemon):
    update = db_update_pokemon(pokemon_id, _pokemon.name, _pokemon.image)

    if not update:
        raise HTTPException(
            status_code=404,
            detail="No existe un pokemón con ese id"
        )
    
    return {
        "mensaje": "Pokemón actualizado correctamente",
        "id": pokemon_id,
        "pokemon": _pokemon
    }