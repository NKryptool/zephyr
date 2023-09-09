import os
import sqlite3
import platform
import json

def extract_cookies(browser_name, system):
    browser_name = browser_name.lower()
    
    # Determina el sistema operativo
    is_windows = system == "windows"
    
    # Define la ruta de las cookies según el sistema operativo
    if is_windows:
        print("Extraccion de cookies en sistema Windows")
        if browser_name == "chrome":
            print("Extraccion de Chrome")
            cookies_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies")
        else:
            cookies_path = None  # Otros navegadores en Windows (ajusta según sea necesario)
    else:
        print("Extraccion de cookies en sistema Linux")
        if browser_name == "chrome":
            print("Extraccion de Chrome")
            cookies_path = os.path.expanduser("~/.config/google-chrome/Default/Cookies")
        elif browser_name == "firefox":
            print("Extraccion de Firefox")
            cookies_path = os.path.expanduser("~/.mozilla/firefox/[profile_name]/cookies.sqlite")
        else:
            cookies_path = None
    
    if cookies_path is None:
        print(f"El navegador {browser_name} no es compatible o el sistema operativo no es reconocido.")
        return

    if not os.path.exists(cookies_path):
        print(f"No se encontraron cookies para el navegador {browser_name}.")
        return

    print("*Inicializando conexion SQLite*")
    # Conecta con la base de datos de cookies
    try:
        connection = sqlite3.connect(cookies_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name, value, host_key, path, expires_utc FROM cookies")
        cookies = cursor.fetchall()
        connection.close()
    except Exception as e:
        print(f"Error al acceder a las cookies: {str(e)}")
        return

    # Imprime las cookies (puedes personalizar cómo se muestran)
    print("Extraccion en proceso...:")
    cookies_with_value = []
    for cookie in cookies:
        name, value, host_key, path, expires_utc = cookie
        cookies_with_value.append({
            "Nombre": name,
            "Valor": value,
            "Dominio": host_key,
            "Ruta": path,
            "Caduca": expires_utc
        })
    if cookies_with_value:
        output_file = "cookies.json"
        print("Escritura de reporte")
        with open(output_file, "w") as json_file:
            json.dump(cookies_with_value, json_file, indent=4)
        print(f"Las cookies con valor se han guardado en {output_file}.")

if __name__ == "__main__":
    browser_name = "chrome"  # Cambia a "firefox" u otro navegador compatible si es necesario
    system = platform.system().lower()  # Obtiene el sistema operativo en tiempo de ejecución
    extract_cookies(browser_name, system)
