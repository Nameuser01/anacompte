#!/usr/bin/env python3

from guizero import *

# Traitement des résultats obtenus
def traitement_selection():
    if (fichier1.value == 1 and fichier2.value == 0):
        print("hello world")
    else:
        print("Au revoir en fait, ca marche pas du coup")
    print(fichier1.value)


# Afficher une fenetre pour selectionner les fichiers a concatener
def selection_fichiers():
    global fichier1, fichier2, selection
    selection = Window(app, title="Selection fichiers")
    message_selection = Text(selection, text="Quels fichier voulez-vous selectionner ?")
    fichier1 = CheckBox(selection, text="2022-06.csv")
    fichier2 = CheckBox(selection, text="2022-05.csv")
    bouton_validation = PushButton(selection, text="Valider selection", command=traitement_selection)
    boutton_quitter_2 = PushButton(selection, text="Fermer", command=fermer_fenetre)


# Fermer la fenêtre de l'application
def quitter_main():
    # app.info("Au revoir", "Merci d'avoir utilisé ce programme !")
    app.destroy()


# Fermer une fenêtre
def fermer_fenetre():
    selection.hide()

# Code principal
app = App(title="Choix des fichiers")
message = Text(app, text="Que voulez vous faire ? ")
selection_fichiers = PushButton(app, text="Fichiers à sélectionner", command=selection_fichiers)
bouton_quitter_1 = PushButton(app, text="Quitter", command=quitter_main)

app.display()
