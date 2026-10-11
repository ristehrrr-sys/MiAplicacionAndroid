import os
import shutil
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class MiAplicacion(App):
    def build(self):
        self.carpeta = "/storage/emulated/0/VideoPython"
        os.makedirs(self.carpeta, exist_ok=True)

        caja = BoxLayout(orientation="vertical", padding=15, spacing=10)
        caja.add_widget(Label(text="MI APLICACIÓN", font_size=28))

        opciones = [
            ("Recortar video", self.recortar),
            ("Convertir a MP4", self.mp4),
            ("Video vertical 9:16", self.vertical),
            ("Extraer audio MP3", self.audio),
            ("Extraer imagen JPG", self.imagen),
            ("Comprimir video", self.comprimir),
            ("Juego del gato 🐱", self.gato),
        ]

        for nombre, funcion in opciones:
            boton = Button(text=nombre, font_size=18)
            boton.bind(on_press=funcion)
            caja.add_widget(boton)

        return caja

    def aviso(self, mensaje):
        Popup(title="Mi Aplicación", content=Label(text=mensaje),
              size_hint=(0.85, 0.4)).open()

    def pedir_video(self, operacion):
        caja = BoxLayout(orientation="vertical", padding=10, spacing=10)
        nombre = TextInput(hint_text="Nombre del video, ej. video.mp4",
                           multiline=False, size_hint_y=None, height=50)
        caja.add_widget(nombre)
        boton = Button(text="Continuar", size_hint_y=None, height=50)
        caja.add_widget(boton)
        ventana = Popup(title=operacion, content=caja,
                        size_hint=(0.9, 0.4))

        def continuar(_):
            archivo = os.path.basename(nombre.text.strip())
            ruta = os.path.join(self.carpeta, archivo)
            ventana.dismiss()
            if not os.path.isfile(ruta):
                self.aviso("No encuentro el video en VideoPython.")
                return
            self.procesar(ruta, operacion)

        boton.bind(on_press=continuar)
        ventana.open()

    def procesar(self, entrada, operacion):
        if operacion == "Recortar video":
            self.aviso("El recorte necesita elegir el inicio y la duración. Se añadirá en la siguiente versión.")
            return
        if operacion == "Convertir a MP4":
            salida = "video_convertido.mp4"
            filtros = []
            codec = ["-c:v", "libx264", "-c:a", "aac"]
        elif operacion == "Video vertical 9:16":
            salida = "video_vertical.mp4"
            filtros = ["-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"]
            codec = ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-c:a", "aac"]
        elif operacion == "Extraer audio MP3":
            salida = "audio_extraido.mp3"
            filtros = ["-vn"]
            codec = ["-codec:a", "libmp3lame", "-q:a", "2"]
        elif operacion == "Extraer imagen JPG":
            self.aviso("La captura de imagen necesita elegir el segundo del video. Se añadirá en la siguiente versión.")
            return
        else:
            salida = "video_comprimido.mp4"
            filtros = []
            codec = ["-c:v", "libx264", "-preset", "fast", "-crf", "28", "-c:a", "aac", "-b:a", "96k"]

        destino = os.path.join(self.carpeta, salida)
        comando = ["ffmpeg", "-y", "-i", entrada] + filtros + codec + [destino]
        if shutil.which("ffmpeg") is None:
            self.aviso("Falta integrar FFmpeg compatible con Android en la APK.")
            return
        try:
            resultado = subprocess.run(comando, capture_output=True, text=True)
            if resultado.returncode == 0:
                self.aviso("Terminado. Archivo: " + salida)
            else:
                self.aviso("No se pudo procesar. Hay que revisar FFmpeg y el video.")
        except Exception as error:
            self.aviso("Error: " + str(error))

    def recortar(self, _):
        self.pedir_video("Recortar video")

    def mp4(self, _):
        self.pedir_video("Convertir a MP4")

    def vertical(self, _):
        self.pedir_video("Video vertical 9:16")

    def audio(self, _):
        self.pedir_video("Extraer audio MP3")

    def imagen(self, _):
        self.pedir_video("Extraer imagen JPG")

    def comprimir(self, _):
        self.pedir_video("Comprimir video")

    def gato(self, _):
        self.aviso("¡Miau! 🐱 El gato está listo para jugar en una próxima versión.")

if __name__ == "__main__":
    MiAplicacion().run()
