import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory

from pytube import YouTube
import re

''' Fonction is_valid_url :
    Action : Vérifie si l'URL correspond à l'expression régulière d'une URL YouTube valide
    
    @param url : URL à vérifier
    
    @return : True si l'URL est valide, False sinon
'''
def is_valid_url(url):
    # Vérifiez si l'URL correspond à l'expression régulière d'une URL YouTube valide
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    match = re.match(youtube_regex, url)

    return bool(match)


''' Fonction check_path: 
    Action : Vérifie si le path de destination est vide.
    
    @return : True si le path n'est pas vide, False sinon
'''
def check_path():
    if path_label["text"] == "":
        return False
    return True


''' Fonction download :

    Action du bouton "Télécharger" : Télécharger la vidéo depuis un URL YouTube valide.
    
    - Vérifie si le path de destination est vide
        Si c'est le cas, on affiche un message d'erreur
    
    - Récupère l'URL de la vidéo à télécharger
    
    - Vérifie si l'URL est valide
        Si c'est le cas, on télécharge la vidéo
        Sinon, on affiche un message d'erreur
    
    - Récupère le format de la vidéo à télécharger  
    - Récupère la vidéo à télécharger
    - Télécharge la vidéo dans le répertoire de destination
'''
def download():
    if not check_path():
        completionLabel["text"] = "Veuillez choisir un répertoire de destination"
        return
    url = entry.get()
    if is_valid_url(url):
        try:
            format = format_var.get().lower()
            videos = YouTube(url)
            video = videos.streams\
                .filter(progressive=True, file_extension='mp4')\
                .order_by('resolution')\
                .desc()\
                .last()
            video.download(path_label["text"])
            completionLabel["text"] = "Téléchargée avec succès."
        except:
            completionLabel["text"] = "Le téléchargement a échoué."
    else:
        completionLabel["text"] = "URL invalide."


""" Fonction - choose_folder :
    Action : Ouvre une fenêtre de dialogue pour choisir le répertoire de destination
    
    - Ouvre une fenêtre de dialogue pour choisir le répertoire de destination
    - Affiche le chemin absolu du répertoire de destination dans un label
"""
def choose_folder():
    folder = askdirectory()
    path_label["text"] = folder

""" Fonction - close_window :
    Action : Ferme la fenêtre
"""
def close_window():
    window.destroy()

## Création d'une fenêtre.
window = Tk()
window.geometry("600x400")
window.title("YouTubeDownloader")
window.iconbitmap("src/YoutubeDownloader.ico")
window.eval('tk::PlaceWindow . center')
window.resizable(False, False)


# Création d'un bouton "Quitter" en haut à droite de la fenêtre
exit_button = Button(window, text="Quitter", command=close_window, bg="red", fg="white")
exit_button.place(relx=1.0, rely=0.0, anchor="ne")

# Création d'un menu déroulant pour choisir le format de vidéo de destination
formats = ["MP4", "AVI", "WEBM"]
format_var = StringVar(window)
format_var.set(formats[0]) # Format par défaut
format_menu = OptionMenu(window, format_var, *formats) # Création du menu déroulant
format_menu.place(relx=0.0, rely=0.0,anchor='nw') # Affichage du menu déroulant

# Création d'un bouton "Parcourir" pour choisir le répertoire de destination
browse_button = tk.Button(window, text="Parcourir", command=choose_folder)
browse_button.place(relx=0.1, rely=0.5, anchor="w")

# Création d'un label pour afficher le chemin absolu du répertoire de destination
path_label = tk.Label(window, text="", font=("Arial", 8, "italic"))
path_label.place(relx=0.25, rely=0.55, anchor="w")

## Création d'un champ de saisie.
entry = tk.Entry(window, width=50)
entry.place(relx=0.5, rely=0.5, anchor="center")

## Création d'un bouton de téléchargement.
downloadButton = tk.Button(window, text="Télécharger", command=download)
downloadButton.place(relx=0.5, rely=0.7, width=200, anchor="center")

## Création d'un label.
completionLabel = tk.Label(window)
completionLabel.place(relx=0.5, rely=0.8, anchor="center")

window.mainloop()




