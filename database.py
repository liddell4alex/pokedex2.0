# Aquí se definen todas las funciones para interactuar con la base de datos
import sqlite3
import os

def db_connect():
    db_path = os.getenv("DB_PATH", "pokemon.db")
    conn = sqlite3.connect(db_path)    # Abre la BD si existe y si no la crea y la abre
    conn.row_factory = sqlite3.Row          # Permite acceder a las columnas de un registro por su nombre
    
    return conn

def db_create_pokemon_table():
    conn = db_connect()

    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS pokemon (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        image TEXT
                        )""")

        conn.commit()
    
    finally:
        conn.close()


def db_insert_pokemon(id=None, name=None, image=None):
    conn = db_connect()

    try:
        if id is None:
            # OR IGNORE permite ignorar la instrucción si el objeto ya existe
            conn.execute("""INSERT OR IGNORE INTO pokemon (name, image)
                            VALUES (?, ?)""", (name, image))
        else:
            conn.execute("""INSERT OR IGNORE INTO pokemon (id, name, image)
                            VALUES (?, ?, ?)""", (id, name, image))


        conn.commit()

    finally:
        conn.close()

def db_delete_pokemon(id):
    conn = db_connect()

    try:
        val = conn.execute("DELETE FROM pokemon WHERE id = ?", (id,))

        conn.commit()

        return val.rowcount > 0

    finally:
        conn.close()

def db_update_pokemon(id, name, image):
    conn = db_connect()

    try:
        val = conn.execute("""UPDATE pokemon
                            SET name = ?, image = ?
                            WHERE id = ?""", (name, image, id))

        conn.commit()

        return val.rowcount > 0

    finally:
        conn.close()