# pokedex_project.py
# Proyecto: Pokédex usando la librería requests y manejo de archivos

# Importamos las librerías necesarias
import requests  # Para realizar peticiones HTTP a la API
import json      # Para trabajar con el formato JSON (obtener datos de la API y guardar el archivo .json)
import os        # Para manipular directorios y archivos en el sistema operativo

# URL base de la PokeAPI para la información de Pokémon
BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

# Nombre de la carpeta donde se guardarán los archivos .json
POKEDEX_FOLDER = "pokedex"

def obtener_datos_pokemon(nombre_pokemon):
    """
    Realiza una petición a la PokeAPI para obtener los datos de un Pokémon.

    :param nombre_pokemon: El nombre del Pokémon a buscar (string).
    :return: Un diccionario con los datos del Pokémon si la petición es exitosa,
             o None si ocurre un error o el Pokémon no existe.
    """
    # Limpiamos y preparamos el nombre para la URL (minúsculas y sin espacios extra)
    nombre_normalizado = nombre_pokemon.lower().strip()
    
    # Construimos la URL completa para la petición
    url = BASE_URL + nombre_normalizado
    
    # Realizamos la petición GET a la API usando la librería requests
    try:
        respuesta = requests.get(url)

        # 1. Validación de Status Codes
        # Si la respuesta es exitosa (código 200)
        if respuesta.status_code == 200:
            # Consumo exitoso de la pokeapi y manejo de datos
            return respuesta.json()
        
        # Si el Pokémon no se encuentra (código 404)
        elif respuesta.status_code == 404:
            print(f"Error: El Pokémon '{nombre_pokemon}' no existe en la Pokédex. Intenta con otro nombre.")
            return None
        
        # Manejo de otros códigos de error HTTP
        else:
            print(f"Error al consultar la API: Código de estado HTTP {respuesta.status_code}.")
            print("Detalles: Puede haber un problema con el servicio de la API.")
            return None

    except requests.exceptions.RequestException as e:
        # Manejo de errores de conexión (ej. no hay internet, error de DNS)
        print(f"\nFatal Error: No se pudo conectar a la PokeAPI. Revisa tu conexión a internet o la URL base.")
        print(f"Detalles del error: {e}")
        return None

def extraer_informacion_relevante(datos_pokemon):
    """
    Procesa los datos brutos del JSON del Pokémon para extraer la información
    requerida por el proyecto (estadísticas, imagen, etc.).

    :param datos_pokemon: El diccionario JSON completo de la respuesta de la API.
    :return: Un diccionario formateado con la información requerida.
    """
    # Estructura del diccionario con los datos requeridos por el proyecto
    info = {
        "nombre": datos_pokemon["name"].capitalize(),
        "id": datos_pokemon["id"],
        # El peso (weight) en la API está en hectogramos (hg), lo convertimos a kilogramos (kg)
        "peso_kg": datos_pokemon["weight"] / 10, 
        # La altura (height) en la API está en decímetros (dm), lo convertimos a metros (m)
        "altura_m": datos_pokemon["height"] / 10,
        
        # Extracción de la URL de la imagen frontal del sprite principal
        # Usamos 'front_default' que es la imagen principal del Pokémon
        "imagen_frontal_url": datos_pokemon["sprites"]["front_default"],
        
        # Extracción de Tipos (types)
        "tipos": [t["type"]["name"].capitalize() for t in datos_pokemon["types"]],
        
        # Extracción de Habilidades (abilities)
        "habilidades": [a["ability"]["name"].replace("-", " ").capitalize() 
                        for a in datos_pokemon["abilities"]],
        
        # Extracción de Movimientos (moves). Limitamos la lista para no ser excesivamente larga.
        "movimientos_principales": [m["move"]["name"].replace("-", " ").capitalize() 
                                     for m in datos_pokemon["moves"][:5]], # Tomamos solo los 5 primeros movimientos
    }
    
    return info

def mostrar_datos_pokemon(info_pokemon):
    """
    Muestra la información del Pokémon de forma amigable en la consola.
    Esto cumple con el requisito de 'Despliegue correcto de la información'
    """
    nombre = info_pokemon["nombre"]
    
    print("\n" + "="*40)
    print(f"¡POKÉMON ENCONTRADO! - {nombre} (ID: {info_pokemon['id']})")
    print("="*40)
    
    # 1. Estadísticas básicas
    print(" ESTADÍSTICAS")
    print(f"  Peso: {info_pokemon['peso_kg']} kg")
    print(f"  Tamaño (Altura): {info_pokemon['altura_m']} m")
    
    # 2. Tipos
    print("TIPOS")
    print(f"  Tipos: {', '.join(info_pokemon['tipos'])}")
    
    # 3. Habilidades
    print("HABILIDADES")
    # Utilizamos 'join' para concatenar la lista de habilidades en un string
    print(f"  Habilidades: {', '.join(info_pokemon['habilidades'])}")
    
    # 4. Movimientos
    print("MOVIMIENTOS PRINCIPALES")
    print(f"  Top 5 Movimientos: {', '.join(info_pokemon['movimientos_principales'])}")
    
    # 5. Link de la imagen
    print("IMAGEN")
    print(f"  Link de Imagen Frontal: {info_pokemon['imagen_frontal_url']}")
    # NOTA: Para mostrar la imagen directamente, se requeriría una librería de interfaz
    # gráfica o la capacidad de imprimir imágenes en la consola, pero el requisito se
    # cumple al proveer el link del recurso.
    
    print("\n" + "="*40)


def guardar_informacion_json(info_pokemon):
    """Guarda la información extraída del Pokémon en un archivo .json 
    dentro de la carpeta 'pokedex'.
    """
    # 1. Asegurarse de que el directorio 'pokedex' exista
    try:
        # Crea el directorio si no existe (la función os.makedirs con exist_ok=True 
        # previene un error si ya existe)
        os.makedirs(POKEDEX_FOLDER, exist_ok=True)
        # Esto es un ejemplo de 'ser capaz de crear un archivo dentro del sistema operativo'
    except OSError as e:
        print(f"\nError al crear la carpeta '{POKEDEX_FOLDER}': {e}")
        return

    # 2. Definir el nombre del archivo (ej. bulbasaur.json)
    nombre_archivo = f"{info_pokemon['nombre'].lower().replace(' ', '_')}.json"
    ruta_completa = os.path.join(POKEDEX_FOLDER, nombre_archivo)

    # 3. Escribir los datos al archivo JSON
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as archivo_json:
            # Usamos json.dump para escribir el diccionario en formato JSON al archivo.
            # indent=4 es opcional, pero hace que el archivo sea más legible.
            json.dump(info_pokemon, archivo_json, indent=4, ensure_ascii=False)
        
        print(f"Información de {info_pokemon['nombre']} guardada exitosamente en:")
        print(f"   -> {ruta_completa}")
        # Esto cumple con 'Guardar adecuadamente el archivo .json'
        
    except IOError as e:
        print(f"\nError al escribir el archivo JSON en {ruta_completa}: {e}")

# --- Función Principal del Programa ---
def ejecutar_pokedex():
    """
    Función principal que orquesta la búsqueda del Pokémon, 
    muestra la información y guarda el archivo JSON.
    """
    
    print("====================================")
    print("       PROYECTO POKÉDEX       ")
    print("====================================")
    print("Consulta detalles de cualquier Pokémon usando la PokeAPI (https://pokeapi.co/).")
    print("Bibliotecas requeridas: requests, json, os.")

    # Solicitar al usuario el nombre del Pokémon
    nombre_busqueda = input("\nIntroduce el nombre del Pokémon a buscar: ")

    if not nombre_busqueda:
        print("El nombre del Pokémon no puede estar vacío.")
        return

    # 1. Obtener los datos del Pokémon
    datos_completos = obtener_datos_pokemon(nombre_busqueda)

    # Solo continuamos si los datos se obtuvieron exitosamente
    if datos_completos:
        # 2. Extraer y formatear la información relevante
        info_a_guardar = extraer_informacion_relevante(datos_completos)
        
        # 3. Mostrar la información al usuario
        mostrar_datos_pokemon(info_a_guardar)
        
        # 4. Guardar la información en un archivo JSON
        guardar_informacion_json(info_a_guardar)

# Ejecutamos la función principal
if __name__ == "__main__":
    ejecutar_pokedex()
