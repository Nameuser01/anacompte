#!/usr/bin/env python3

# Imports de librairies
import os
from guizero import PushButton, Text, Window, CheckBox, App
import matplotlib.pyplot as plt
from pandas_ods_reader import read_ods


# Imports de fichiers personnels
from globalisation import *


# Concaténer plusieurs fichiers csv en un seul
def lancement_concaténeur():
	# Formatage et écriture des fichiers selectionnées vers le fichier de concaténation (csv)
	def ecriture_csv(nom_fichier):
		os.system(f"echo -n '' > {nom_fichier}")	# Reset du fichier pour ne pas écrire de la donnée sur un fichier déjà exisant
		global dates_opérations, opérations, objet_opérations
		for i in range(0, len(liste_selection)):
			# Lecture fichier
			f = open(liste_selection[i], "r")
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
			if (i > 0):
				del dates_opérations[0]
				del opérations[0]
				del objet_opérations[0]
			else:
				pass  # Ne rien faire

			del dates_opérations[len(dates_opérations) - 1]
			champs_tempo = opérations[0]
			del opérations[0]
			opérations.insert(0, champs_tempo)
			# Ecriture dans le fichier
			ecriture_csv = open(f"{nom_fichier}", "a")
			for b in range (0, len(dates_opérations)):
				ecriture_csv.write(f"{dates_opérations[b]}; {opérations[b]}; {objet_opérations[b]}; ;\n")
			ecriture_csv.close()
		
		selection.info("Information", "Concaténation de fichiers effectuée !")



	# Composition du nouveau nom du fichier concaténé
	def nouveau_nom_compose(liste_noms):
		for i in range(0, len(liste_noms)):
			# Traitement premier fichier lorsqu'il y a plusieurs fichiers à traiter
			if (i == 0 and len(liste_noms) > 1):
				nouveau_nom = liste_noms[i][:-4]
			# Traitement fichiers entre le premier et le dernier fichier
			elif (i > 0 and i < len(liste_noms) - 1):
				nouveau_nom = nouveau_nom + "_" + liste_noms[i][:-4]
			# Traitement dernier fichier classique
			elif (i == len(liste_noms) - 1 and i > 0):
				nouveau_nom = nouveau_nom + "_" + liste_noms[i]
			# Traitement premier et dernier [unique] fichier
			elif (i == 0 and len(liste_noms) == 1):
				nouveau_nom = liste_noms[i]
			else:
				print("Erreur: Pas content !")
		return nouveau_nom


	# Traitement des résultats obtenuse
	def traitement_selection():
		global liste_selection
		liste_selection = []
		for i in range (0, len(fichier_concat)):
			if (globals()[f"fichier" + str(i)].value == 1):
				liste_selection.append(globals()[f"fichier" + str(i)].text)
			else:
				pass
		fermer_fenetre()
		liste_selection.sort()
		nom_recomposé = nouveau_nom_compose(liste_selection)
		ecriture_csv(nom_recomposé)


	# Afficher une fenetre pour selectionner les fichiers a concatener
	def selection_fichiers():
		global selection, fichier_concat
		selection = Window(app, title="Selection fichiers")
		message_selection = Text(selection, text="Quels fichier voulez-vous selectionner ?")

		# Comptage du nombre de fichiers à concaténer
		os.system("ls ????-??.csv > .to_concatenate.foo")

		# Lecture du fichier / récupération des informations sur les fichiers à traiter
		# ajouter un try/except en cas de non existence du fichier
		fichier_concat = open(".to_concatenate.foo", "r")
		fichier_concat_contenu = fichier_concat.read()
		fichier_concat.close()
		os.system("rm .to_concatenate.foo")

		# Traitement de l'information recue
		fichier_concat = fichier_concat_contenu.replace("\n", ";")
		fichier_concat = fichier_concat.split(";")
		del fichier_concat[len(fichier_concat) - 1 ]  # Suppression dernier champs de la liste -> vide
		
		# Exécution de la ligne du fichier externe de globalisation qui correspond a la longueur de fichier_concat
		globals()['glob' + str(len(fichier_concat) - 1)]()

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
	# Boucle d'analyse par dictionnaire des objets d'opérations

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
	print(f"opréations = {opérations}")
	print(f"objet_opréations = {objet_opérations}")
	plt.figure(figsize = (8, 8))
	x = [1, 2, 3, 4, 10]
	plt.pie(x, labels = ['A', 'B', 'C', 'D', 'E'],
	colors = ['red', 'green', 'yellow'], explode = [0, 0.2, 0, 0, 0], autopct = lambda x: str(round(x, 2)) + '%', pctdistance = 0.7, labeldistance = 1.4, shadow = True)
	plt.legend()
	plt.show()


# Rapports gain / pertes par jours
def solde_evolution_quotidienne(dates_opérations, opérations):
	evolution_solde = []
	dates = []
	solde_courant = 0
	reference = 0
	for i in range(0, len(opérations)):
		solde_courant = solde_courant + opérations[i]
		print(f"debeug boucle:\ndate: {dates_opérations[i]} -> i: {i} -> solde_courant: {solde_courant}")
		if (i == 0):  # Rang n = 1
			evolution_solde.append(solde_courant)
			dates.append(dates_opérations[i])
			reference += 1
		elif (i > 0 and dates_opérations[i] != dates_opérations[i - 1]):  # Rang n > 0 et date différente du rang n - 1
			evolution_solde.append(solde_courant)
			dates.append(dates_opérations[i])
			reference += 1
		elif (i > 0 and dates_opérations[i] == dates_opérations[i - 1]):  # Rang n > 0 et date similaire du rang n - 1
			del evolution_solde[reference - 1]
			evolution_solde.append(solde_courant)
		elif (i == len(opérations)):
			if (dates_opérations[i] == [dates_opérations[i - 1]]):
				del evolution_solde[reference - 1]
				evolution_solde.append(solde_courant)
			else:
				evolution_solde.append(solde_courant)
				dates.append(dates_opérations[i])
				reference += 1
		else:
			print("Yusk0")

	if (solde_courant >= 0):
		color = "g"
	else:
		color = "r"

	plt.grid(True, color='black', linewidth=0.5)
	plt.plot(dates, evolution_solde, color, linewidth=0.5, marker="+", label="évolution solde")
	plt.xticks(rotation=45)
	plt.legend()
	plt.show()


# Production de statistiques sur le / les fichier(s) csv choisi(s)
def analyse_statistique(nom_fichier):
	fichier = "/home/user/Documents/py/anacompte/main/" + str(nom_fichier)  # MODIFIER
	array_ods = read_ods(fichier)
	feuille_mois = 5  # À définir par l'utilisateur
	contenu = read_ods(fichier, feuille_mois)

	dates_opérations = []
	opérations = []
	objet_opérations = []

	for i in range(0, len(contenu.values)):
		dates_opérations.append(contenu.values[i][0])
		opérations.append(contenu.values[i][1])
		objet_opérations.append(contenu.values[i][2])

	solde_evolution_quotidienne(dates_opérations, opérations)
	sujets_proportions(opérations, objet_opérations)


def menu(option):
	# Constantes
	if (option == "principal"):
		# Afficher le menu principal
		print("====== Menu principal ======")
		print("0\t-\tQuitter le programme")
		print("a\t+\tAnalyse sur un mois")
		print("b\t+\tAnalyse sur une année [À faire...]")
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
		choix = choix.lower()

		# Conditions
		if (choix == "0" or choix == "q" or choix == "exit" or choix == "quit" or choix == "leave"):
			# Quitter le programme
			stay = False
		# Production de statistiques concernant un fichier
		elif (choix == "a"):
			# Remplacer cette partie par une interface graphique
			analyse_statistique("2021.ods")
			input("\n\n[INFO]: Appuyer sur entrée pour continuer...")
		# Concaténation de fichiers choisis
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
