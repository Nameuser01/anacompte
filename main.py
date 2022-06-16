#!/usr/bin/env python3

# Imports de librairies
import time
import os
from guizero import PushButton, Text, Window, CheckBox, App


# Concaténer plusieurs fichiers csv en un seul
def lancement_concaténeur():
    # Traitement des résultats obtenus
    def traitement_selection():
        if (fichier1.value == 1 and fichier2.value == 0):
            print("hello world")
        else:
            print("Au revoir en fait, ca marche pas du coup")
        print(fichier1.value)


    # Afficher une fenetre pour selectionner les fichiers a concatener
    def selection_fichiers():
        global selection
        selection = Window(app, title="Selection fichiers")
        message_selection = Text(selection, text="Quels fichier voulez-vous selectionner ?")

        # Comptage du nombre de fichiers à concaténer
        os.system("ls ????-??.csv > .to_concatenate.foo")

        # Lecture du fichier / récupération des informations sur les fichiers à traiter
        # ajouter un try/except en cas de non existence du fichier
        fichiers_concat = open(".to_concatenate.foo", "r")
        fichier_concat_contenu = fichier_concat.read()
        fichier_concat.close()
        os.system("rm .to_concatenate.foo")

        # Traitement de l'information recue
        fichier_concat = fichier_concat.replace("\n", ";")
        fichier_concat = fichier_concat.split(";")
        del fichier_concat[len(fichier_concat) - 1]  # Suppression dernier champs de la liste -> vide
        
        # Exécution de la ligne du fichier externe de globalisation qui correspond a la longueur de fichier_concat
        # ...

        # Génération des variables en fonction du nombre de fichiers à concaténer
        compteur_nbr_checkbox = 0
        for i in fichier_concat:
        	globals()[f"fichier{compteur_nbr_checkbox}"] = CheckBox(selection, text=f"{i}")
        	compteur_nbr_checkbox += 1

        bouton_validation = PushButton(selection, text="Valider selection", command=traitement_selection)
        boutton_quitter_2 = PushButton(selection, text="Fermer", command=fermer_fenetre)


    # Fermer la fenêtre de l'application
    def quitter_main():
        # app.info("Au revoir", "Merci d'avoir utilisé ce programme !")
        app.destroy()


    # Fermer une fenêtre
    def fermer_fenetre():
        selection.hide()


    app = App(title="Choix des fichiers")
    message = Text(app, text="Que voulez vous faire ? ")
    selection_fichiers = PushButton(app, text="Fichiers à sélectionner", command=selection_fichiers)
    bouton_quitter_1 = PushButton(app, text="Quitter", command=quitter_main)

    app.display()




# Faire des statistiques sur les types d'opérations
def sujets_proportions(opérations, objet_opérations):
	# Boucle d'analyse  par dictionnaire des objets d'opérations

	# Opérations négatives
	mobilitée = ["voiture", "vélo", "velo", "train", "avion", "bateau", "navette" "navigo", "essence", "e10", "e5", "gazole", "b7", "péage", "peage"]
	vêtements = ["nike", "adidas"]
	alimentaire = ["courses", "carrefour", "casino", "lidl", "leclerc", "nourriture", "boisson"]
	logement = ["loyer"]

	# Opérations positives
	virements = ["virement"]
	dépôts_chèque = ["cheque", "chèque"]
	aides = ["bourse", "apl"]

	# Processus d'identifications de mots clés
	# for i in jeVerraiPlusTardParceQueCaAl'AirQuandMêmeChiant:


# Suppression du premier champs d'une liste
def suppression_champs_un(nom_liste):
	del nom_liste[0]
	return nom_liste


# Supprimer le dernier champs d'une liste
def suppression_dernier_champs(nom_liste):
	del nom_liste[len(nom_liste) - 1]
	return nom_liste


# Suppression des deux derniers caractères du modèle -> "xx,xx €" / "-xx,xx €"
def suppression_deux_derniers_caractères(nom_liste):
	compteur = 0
	for i in nom_liste:
		nom_liste[compteur] = i.replace(",", ".")
		nom_liste[compteur] = float(nom_liste[compteur][:-2])
		compteur += 1
	return nom_liste


# Reading file formated as suggered in my GitHub
def lire_fichier_personnel(nom_fichier):
	# Lecture fichier
	f = open(nom_fichier, "r")
	fichier = f.read()
	f.close()
	# Parseur
	fichier = fichier.replace("\n", ";")
	fichier = fichier.split(";")
	# Récupérations des valeurs du fichier
	dates_opérations = fichier[0:len(fichier):5]
	opérations = fichier[1:len(fichier):5]
	objet_opérations = fichier[2:len(fichier):5]
	# Filtrage des listes
	dates_opérations = suppression_champs_un(dates_opérations)
	dates_opérations = suppression_dernier_champs(dates_opérations)
	opérations = suppression_champs_un(opérations)
	opérations = suppression_deux_derniers_caractères(opérations)
	objet_opérations = suppression_champs_un(objet_opérations)
	# Affichage global des informations filtrées
	# for i in range (0, len(dates_opérations)):
	# 	print(f"dates: {dates_opérations[i]}")
	# 	print(f"opérations: {opérations[i]}")
	# 	print(f"objet oprérations: {objet_opérations[i]}\n")
	sujets_proportions(opérations, objet_opérations)


def menu(option):
	# Constantes
	if (option == "principal"):
		# Afficher le menu principal
		print("====== Menu principal ======")
		print("0\t-\tQuitter le programme")
		print("a\t+\tlire un fichier personnel")
		print("b\t+\tAssembler des fichiers csv")
		print("\n")
	else:
		print("[Erreur]: Aucun menu à afficher !\n")


# boucle principale du programme
def main():
	stay = True
	choix = 0
	while (stay == True):

		# Choix utilisateur
		menu("principal")
		choix = input("Que voulez vous faire ?\n> ")

		# Conditions
		if (choix == "0"):
			# Quitter le programme
			stay = False
		elif (choix == "a"):
			lire_fichier_personnel("2022-06.csv")
			input("\n\n[INFO]: Appuyer sur entrée pour continuer...")
		elif (choix == "b"):
			lancement_concaténeur()
			input("\n\n[INFO]: Appuyer sur entrée pour continuer...")
		else:
			print("\n\n[Erreur]: Entrée utilisateur incorrecte !")
			input("\n\n[INFO]: Appuyez sur entrée pour continuer...")
		os.system("clear")

	print("Fin de l'exécution de ce programme !")


os.system("clear")
main()
