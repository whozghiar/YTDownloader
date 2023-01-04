import tkinter as tk
import moviepy.editor as mp
import re
import os
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox


from pytube import YouTube
from moviepy.editor import *
from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

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

""" Fonction - choose_folder :
    Action : Ouvre une fenêtre de dialogue pour choisir le répertoire de destination
    
    - Ouvre une fenêtre de dialogue pour choisir le répertoire de destination
    - Mets à jour le label du répertoire de destination
    
    @param label : Label du répertoire de destination
"""
def choose_directory(label):
    folder = askdirectory()
    label["text"] = folder
    return

""" Fonction - close_window :
    Action : Ferme la fenêtre
    
    @param window : Fenêtre à fermer
"""
def close_window(window):
    window.destroy()
    return


""" Fonction - check_path :
    Action : Active ou désactive la saisie de l'URL en fonction du chemin du répertoire de destination
    
    - Si le chemin du répertoire de destination est vide, on désactive la saisie de l'URL
    - Sinon, on active la saisie de l'URL
    - La fonction est appelée toutes les 100ms
    
    @param : window : Fenêtre principale
    @param : directory_path_label : Label du chemin du répertoire de destination
    @param : entry : Champ de saisie de l'URL
"""
def check_directory_path(window,directory_path_label,input):
    if directory_path_label["text"] != "":
        input.config(state="normal")
    else:
        input.config(state="disabled")
    window.after(100, check_directory_path, window,directory_path_label,input)

'''
    Fonction - updateButton :
    Action : Active ou désactive le bouton "Télécharger" en fonction de l'URL saisie
    
    - Si l'URL est valide, on active le bouton "Télécharger"
    - Sinon, on désactive le bouton "Télécharger"
    - La fonction est appelée toutes les 100ms
    
    @param window : Fenêtre principale
    @param entry : Champ de saisie de l'URL
    @param button : Bouton "Télécharger"
    
'''
def updateButton(window,entry,button):
    url = entry.get()
    if is_valid_url(url):
        button.config(state="normal")
        button.config(bg="green", fg="white")
    else:
        button.config(state="disabled")
        button.config(bg="red", fg="white")
    window.after(100, updateButton, window,entry,button)

def format_title(title):
    #print(f"Original Title : {title}")

    formated_title = title.replace(":", "°") \
        .replace("/", "°") \
        .replace("\\", "°") \
        .replace("*", "°") \
        .replace("?", "°"). \
        replace("\"", "°") \
        .replace("<", "°") \
        .replace(">", "°") \
        .replace("|", "°")
    return formated_title

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

def download(inputURL, directory_path_label,format_var, subtitleBox):
    url = inputURL.get()
    download_directory = directory_path_label["text"]
    format = format_var.get().lower()
    cc = subtitleBox.get()
    lang = "en"
    #messagebox.showinfo("Infos : ", f"URL : {url} \nRépertoire de destination : {download_directory} \nFormat : {format},\nCC : {cc}")

    try :
        videos = YouTube(url)
        # Récupérer la vidéo la plus haute qualité

        video = videos.streams \
            .filter(adaptive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first()

        audio = videos.streams\
            .filter(only_audio=True)\
            .order_by('abr')\
            .desc()\
            .first()

        #print(video)
        #print (audio)
        author = format_title(videos.author.title()) #messagebox.showinfo("Infos : ", f"Auteur : {author} \nTitre : {title}")


        subdirectory = f"{download_directory}/{author}"
        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory)

        video_file_name = os.path.basename(video.download(subdirectory))
        audio_file_name = os.path.basename(audio.download(subdirectory))

        # Récupérer l'exension du fichier du fichier audio (situé après le dernier point)
        title_file_name = audio_file_name.split(".")[0]
        extension = audio_file_name.split(".")[-1]
        mp3_file_name = audio_file_name.replace(f".{extension}", ".mp3")

        os.rename(f"{subdirectory}/{audio_file_name}", f"{subdirectory}/{mp3_file_name}")

        audio_file_name = mp3_file_name
        #print(video_file_name)
        #print(audio_file_name)

        videoclip = VideoFileClip(f"{subdirectory}/{video_file_name}")
        audioclip = CompositeAudioClip([AudioFileClip(f"{subdirectory}/{audio_file_name}")])
        videoclip.audio = audioclip
        videoclip.write_videofile(f"{subdirectory}/{video_file_name}", codec="libx264", audio_codec="aac")


        #messagebox.showinfo("Infos : ", "Téléchargement terminé !")
    except Exception as e:
        messagebox.showerror("ERROR", f"Erreur lors du téléchargement : {e}")
    
    if cc:
        subtitle_name_file = download_subtitle(videos,title_file_name,lang,subdirectory)
        print(f"Fichier de sous-titres : {subtitle_name_file}")
        #link_subtitle(video_file_name,subtitle_name_file,subdirectory)

        """
        ## Lier les sous-titres au fichier vidéo
        
        print(f"subtitles file : {title_subtitles_file}")
        print(f"video file : {title}")

        try:
            video = mp.VideoFileClip(f"{subdirectory}/{title}.mp4")
            # Subtitles in UTF-8 format
            
            
            subtitles = SubtitlesClip(f"{subdirectory}/{title_subtitles_file}")
            result = CompositeVideoClip([video, subtitles.set_position(("center", "bottom"))])
            result.write_videofile(f"{subdirectory}/{title}_subititlized.mp4")

            messagebox.showinfo("Infos : ", "Liaison des sous-titres terminée !")
        except Exception as e:
            messagebox.showerror("Erreur lors de la liaison des sous-titres : ", e)
        """

def download_subtitle(videos_YouTubeStreams,fileName,lang,directory):

    # Tant qu'on arrive pas à télécharger les sous-titres, on réessaye
    while True:
        try:
            # Récupérer les sous-titres de la vidéo en anglais si ils existent sinon en anglais traduit automatiquement
            caption = videos_YouTubeStreams.captions.get_by_language_code(lang)
            caption.download(f"{fileName}.srt",output_path=directory,filename_prefix="[CC]")
            #messagebox.showinfo("Infos : ", "Téléchargement des sous-titres terminé !")
        except Exception as e:
            print(f"ERROR : Erreur lors du téléchargement des sous-titres : {e}")
            lang = "a.en"
        else:
            break
    return f"[CC]{fileName} ({lang}).srt"

def link_subtitle(video_file_name, subtitle_file_name, directory):
    print (f"video file : {video_file_name}")
    print(f"subtitles file : {subtitle_file_name}")
    print(f"directory : {directory}")


def main():
    ## Création d'une fenêtre.
    window = Tk()
    window.geometry("600x400")
    window.title("YouTubeDownloader")
    window.iconbitmap("src/YoutubeDownloader.ico")
    window.eval('tk::PlaceWindow . center')
    window.resizable(False, False)

    # Création d'un label pour le répertoire de destination
    directory_path_label = Label(window, text="", font=("Arial", 8, "italic"))
    directory_path_label.place(relx=0.25, rely=0.55, anchor="w")

    # Création d'un bouton "Quitter" en haut à droite de la fenêtre
    exit_button = Button(window, text="Quitter", command=lambda: close_window(window), bg="red", fg="white")
    exit_button.place(relx=1.0, rely=0.0, anchor="ne")

    # Création d'un menu déroulant pour choisir le format de vidéo de destination
    formats = ["MP4", "AVI", "WEBM"]
    format_var = StringVar(window)
    format_var.set(formats[0]) # Format par défaut
    format_menu = OptionMenu(window, format_var, *formats) # Création du menu déroulant
    format_menu.place(relx=0.0, rely=0.0,anchor='nw') # Affichage du menu déroulant

    # Création d'un bouton "Parcourir" pour choisir le répertoire de destination
    browse_button = tk.Button(window, text="Browse", command=lambda : choose_directory(directory_path_label))
    browse_button.place(relx=0.1, rely=0.5, anchor="w")

    # Créer une checkbox pour télécharger les sous-titres
    values_subtitleBox = tk.BooleanVar()
    subtitleBox = tk.Checkbutton(window, text="Sous-titres",variable= values_subtitleBox,onvalue=True, offvalue=False)
    subtitleBox.place(relx=0.9, rely=0.5, anchor="e")

    ## Création d'un bouton de téléchargement.
    downloadButton = tk.Button(window, text="Télécharger", command= lambda : download(input, directory_path_label,format_var, values_subtitleBox), state="disabled", bg="red", fg="white")
    downloadButton.place(relx=0.5, rely=0.7, width=200, anchor="center")

    ## Création d'un champ de saisie. Il est désactivé par défaut.
    input = tk.Entry(window, width=50, state="disabled")
    input.place(relx=0.5, rely=0.5, anchor="center")

    window.after(100, check_directory_path, window,directory_path_label,input)
    window.after(100, updateButton, window,input,downloadButton)

    window.mainloop()


main()



