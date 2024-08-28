import os
import re
import shutil
from tkinter import Tk, Button, filedialog, messagebox

def validar_directorio(directorio):
    if not os.path.exists(directorio):
        raise FileNotFoundError(f"El directorio {directorio} no existe.")
    if not os.access(directorio, os.R_OK | os.W_OK):
        raise PermissionError(f"No se tienen permisos adecuados para el directorio {directorio}.")

def obtener_archivos(directorio):
    videos = []
    imagenes = []
    for root, _, files in os.walk(directorio):
        for file in files:
            if re.search(r'\.(jpg|png|gif|jpeg)$', file, re.IGNORECASE):
                imagenes.append(os.path.join(root, file))
            elif re.search(r'\.(mp4|avi|mkv|mov|ts)$', file, re.IGNORECASE):
                videos.append(os.path.join(root, file))
    return videos, imagenes

def renombrar_y_mover_archivos(archivos, tipo, directorio_destino, contador):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    
    for archivo in archivos:
        nombre_base = os.path.basename(archivo)
        if re.match(rf'{tipo}_\d+', nombre_base):
            continue

        nuevo_nombre = f"{tipo}_{contador}{os.path.splitext(archivo)[1]}"
        while os.path.exists(os.path.join(directorio_destino, nuevo_nombre)):
            contador += 1
            nuevo_nombre = f"{tipo}_{contador}{os.path.splitext(archivo)[1]}"
        
        shutil.move(archivo, os.path.join(directorio_destino, nuevo_nombre))
        contador += 1

def procesar_directorio(directorio):
    try:
        validar_directorio(directorio)
        videos, imagenes = obtener_archivos(directorio)
        
        contador = 1
        directorio_imagenes = os.path.join(directorio, 'Imagenes')
        directorio_videos = os.path.join(directorio, 'Videos')

        renombrar_y_mover_archivos(imagenes, 'Foto', directorio_imagenes, contador)
        renombrar_y_mover_archivos(videos, 'Videox', directorio_videos, contador)
        
        messagebox.showinfo("Éxito", f"Las imágenes y videos han sido renombrados, omitiendo los que ya tenían el formato correcto.\nDirectorios de destino:\nImágenes: {directorio_imagenes}\nVideos: {directorio_videos}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    if directorio:
        procesar_directorio(directorio)

def main():
    root = Tk()
    root.title("Renombrador")
    root.geometry("200x100")

    btn_seleccionar = Button(root, text="Seleccionar Directorio", command=seleccionar_directorio)
    btn_seleccionar.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
