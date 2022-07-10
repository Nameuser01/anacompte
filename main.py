#!/usr/bin/env python3

# Imports de librairies
import os
# from guizero import PushButton, Text, Window, CheckBox, App
import matplotlib.pyplot as plt
from pandas_ods_reader import read_ods


# Imports de fichiers personnels
from globalisation import *


# Fonction de comparaison de deux matrices
def comparaison_matricielle(to_compare, is_positif):
    # Séléction du comparant
    bit_stop = False
    theme = ""
    op_positives = [
        ["voiture", "vélo", "velo", "train", "avion", "bateau", "navette",
         "navigo", "essence", "e10", "e5", "gazole", "b7", "péage", "peage"],
        ["nike", "adidas"],
        ["courses", "carrefour", "casino", "lidl", "leclerc", "nourriture",
        "boisson"],
        ["loyer"]
    ]
    op_negatives = [
        ["virement"],
        ["cheque", "chèque"],
        ["bourse", "apl"],
    ]
    if (is_positif == True):
        for a in range(len(op_positives)):
            for b in range(len(op_positives[a])):
                print(f"to_compare[1] vaut {to_compare[1]}")
                if (to_compare[1] == "’"):
                    to_compare = to_compare[2:]
                else:
                    pass
                print(f"{to_compare.lower()} == {op_positives[a][b].lower()} ?")
                if (to_compare.lower() == op_positives[a][b].lower()):
                    print(f"theme = {a}")
                    theme = a
                else:
                    pass
    else:
        for a in range(len(op_negatives)):
            for b in range(len(op_negatives[a])):
                if (to_compare[1] == "’"):
                    to_compare = to_compare[2:]
                else:
                    pass
                print(f"{to_compare.lower()} == {op_positives[a][b].lower()} ?")
                if (to_compare.lower() == op_positives[a][b].lower()):
                    print(f"theme = {a}")
                    theme = a + len(op_positives)
                else:
                    pass

    return theme



# Faire des statistiques sur les types d'opérations
def sujets_proportions(opérations, objet_opérations):
    themes_list = ["mobilités", "vêtements", "alimentaire",
        "logement", "virements", "dépôts",
        "aides", "autre"
    ]
    opérations_list = [0, 0, 0, 0, 0, 0, 0, 0]
    for a in range(len(objet_opérations)):
        tmp = objet_opérations[a].split()
        if (opérations[a] < 0):
            positif = True
        else:
            positif = False

        for b in range(len(tmp)):
            theme = ""
            theme = comparaison_matricielle(tmp[b], positif)
            if (theme != ""):
                break
            else:
                pass
        if (theme == ""):
            opérations_list[len(opérations_list) - 1] += opérations[a]
        else:
            opérations_list[theme] += opérations[a]

    plt.figure(figsize = (8, 8))
    plt.pie(opérations_list, labels = themes_list,
        colors = ['red', 'green', 'yellow'],
        autopct = lambda x: str(round(x, 2)) + '%', pctdistance = 0.7,
        labeldistance = 1.4
    )
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
        # print(f"debeug boucle:\ndate: {dates_opérations[i]} -> i: {i} -> solde_courant: {solde_courant}")
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
            print("C'est cassé ;-(")

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
    fichier = "/home/<user>/Documents/py/anacompte/main/" + str(nom_fichier)  # MODIFIER
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
            # Remplacer par une interface graphique
            analyse_statistique("2021.ods")
            input("\n\n[INFO]: Appuyer sur entrée pour continuer...")
        else:
            print("\n\n[Erreur]: Entrée utilisateur incorrecte !")
            input("\n\n[INFO]: Appuyez sur entrée pour continuer...")
        os.system("clear")

    print("Fin de l'exécution de ce programme !")


os.system("clear")
main()

