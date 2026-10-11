import os
import subprocess

VIDEO_DIR = os.path.expanduser("~/storage/shared/VideoPython")
os.makedirs(VIDEO_DIR, exist_ok=True)

def buscar_video():
    nombre = input("Nombre del video (ej. video.mp4): ").strip()
    ruta = os.path.join(VIDEO_DIR, os.path.basename(nombre))
    if not os.path.isfile(ruta):
        print("No se encontró el video:", ruta)
        return None
    return ruta

def ejecutar(comando, salida):
    print("\nProcesando... espera a que termine.")
    resultado = subprocess.run(comando)
    if resultado.returncode == 0:
        print("\n¡Terminado! Archivo guardado en:\n", salida)
    else:
        print("\nNo se pudo procesar el archivo. Revisa el nombre y el formato.")

def recortar_video():
    entrada = buscar_video()
    if not entrada:
        return
    try:
        inicio = float(input("Segundo de inicio: "))
        duracion = float(input("Duración en segundos: "))
        if inicio < 0 or duracion <= 0:
            print("Los valores no son válidos.")
            return
        salida = os.path.join(VIDEO_DIR, "video_recortado.mp4")
        ejecutar([
            "ffmpeg", "-y", "-ss", str(inicio), "-i", entrada,
            "-t", str(duracion), "-c:v", "libx264", "-c:a", "aac",
            "-movflags", "+faststart", salida
        ], salida)
    except ValueError:
        print("Escribe números válidos.")

def convertir_mp4():
    entrada = buscar_video()
    if not entrada:
        return
    salida = os.path.join(VIDEO_DIR, "video_convertido.mp4")
    ejecutar([
        "ffmpeg", "-y", "-i", entrada, "-c:v", "libx264",
        "-c:a", "aac", "-movflags", "+faststart", salida
    ], salida)

def vertical_916():
    entrada = buscar_video()
    if not entrada:
        return
    salida = os.path.join(VIDEO_DIR, "video_vertical.mp4")
    filtro = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920"
    )
    ejecutar([
        "ffmpeg", "-y", "-i", entrada, "-vf", filtro,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
        "-c:a", "aac", "-movflags", "+faststart", salida
    ], salida)

def extraer_audio():
    entrada = buscar_video()
    if not entrada:
        return
    salida = os.path.join(VIDEO_DIR, "audio_extraido.mp3")
    ejecutar([
        "ffmpeg", "-y", "-i", entrada, "-vn",
        "-codec:a", "libmp3lame", "-q:a", "2", salida
    ], salida)

def extraer_imagen():
    entrada = buscar_video()
    if not entrada:
        return
    try:
        segundo = float(input("Segundo del video para capturar la imagen: "))
        if segundo < 0:
            print("El segundo no puede ser negativo.")
            return
        salida = os.path.join(VIDEO_DIR, "imagen_extraida.jpg")
        ejecutar([
            "ffmpeg", "-y", "-ss", str(segundo), "-i", entrada,
            "-frames:v", "1", "-q:v", "2", salida
        ], salida)
    except ValueError:
        print("Escribe un número válido.")

def comprimir_video():
    entrada = buscar_video()
    if not entrada:
        return
    salida = os.path.join(VIDEO_DIR, "video_comprimido.mp4")
    ejecutar([
        "ffmpeg", "-y", "-i", entrada, "-c:v", "libx264",
        "-preset", "fast", "-crf", "28", "-c:a", "aac",
        "-b:a", "96k", "-movflags", "+faststart", salida
    ], salida)

def editor_videos():
    while True:
        print("\n🎬 EDITOR DE VIDEOS")
        print("1. Recortar video")
        print("2. Convertir a MP4")
        print("3. Convertir a vertical 9:16")
        print("4. Extraer audio MP3")
        print("5. Extraer una imagen JPG")
        print("6. Comprimir video")
        print("7. Volver al menú")
        opcion = input("Elige: ").strip()

        funciones = {
            "1": recortar_video,
            "2": convertir_mp4,
            "3": vertical_916,
            "4": extraer_audio,
            "5": extraer_imagen,
            "6": comprimir_video
        }
        if opcion == "7":
            break
        elif opcion in funciones:
            funciones[opcion]()
        else:
            print("Opción no válida.")

def juego_gato():
    puntos = 0
    while True:
        print("\n🐱 JUEGO DEL GATO | Puntos:", puntos)
        print("1. Saltar y comer una fruta 🍎")
        print("2. Volver al menú")
        opcion = input("Elige: ").strip()
        if opcion == "1":
            puntos += 1
            print("¡Miau! El gato comió una fruta.")
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")

def menu():
    while True:
        print("\n========================")
        print("     MI APLICACIÓN")
        print("========================")
        print("1. Editor de videos 🎬")
        print("2. Juego del gato 🐱")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            editor_videos()
        elif opcion == "2":
            juego_gato()
        elif opcion == "3":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
