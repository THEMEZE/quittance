# finale 

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

import os
import subprocess

from datetime import datetime
import locale

import random
from datetime import datetime, timedelta
import calendar


def verifier_et_creer_chemin(sortie_path):
    """
    Vérifie si le chemin du fichier existe, et le crée si nécessaire.

    Args:
        sortie_path (str): Chemin du fichier (ex. 'chemin/ver/quitance.tex').

    Returns:
        bool: True si le chemin a été créé ou existait déjà, False en cas d'erreur.
    """
    try:
        # Extraire le dossier du chemin
        chemin_dossier = os.path.dirname(sortie_path)
        
        # Vérifier si le dossier existe, sinon le créer
        if not os.path.exists(chemin_dossier):
            os.makedirs(chemin_dossier)
        
        return True
    except Exception as e:
        print(f"Erreur lors de la création du chemin : {e}")
        return False


# Fonction pour remplacer les champs {{}} dans le modèle
def generer_quittance(donnees):

    modele_path = donnees["modele_path"]
    sortie_path = donnees["sortie_path"]

    verifier_et_creer_chemin(sortie_path)
    
    with open(modele_path, 'r') as modele_file:
        modele_content = modele_file.read()
    
    # Remplacer chaque champ dans le modèle par les valeurs du dictionnaire
    for cle, valeur in donnees.items():
        modele_content = modele_content.replace(f"{{{{{cle}}}}}", str(valeur))
    
    # Sauvegarder le fichier .tex généré
    with open(sortie_path, 'w') as sortie_file:
        sortie_file.write(modele_content)

    print(f"Quittance générée : {sortie_path}")
    
    # Compiler le fichier .tex en PDF
    compiler_quittance(sortie_path)
    
    # Nettoyer les fichiers auxiliaires
    nettoyer_fichiers_auxiliaires(sortie_path)

# Fonction pour compiler le fichier .tex en PDF avec pdflatex
def compiler_quittance(fichier_tex):
    try:
        result = subprocess.run(['pdflatex', fichier_tex], check=True, capture_output=True, text=True)
        print(f"Compilation réussie : {fichier_tex.replace('.tex', '.pdf')}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la compilation : {e.stderr}")
    except FileNotFoundError:
        print("Erreur : pdflatex n'est pas installé. Veuillez installer LaTeX sur votre machine.")

import shutil

def deplacer_fichier(source, destination):
    """
    Déplace un fichier d'un répertoire source vers un répertoire cible.
    Si un fichier du même nom existe déjà dans la destination, ajoute un suffixe unique (_2, _3, etc.).

    Args:
        source (str): Chemin complet du fichier source (ex. 'chemin/source/fichier.txt').
        destination (str): Répertoire de destination (ex. 'chemin/cible/').

    Returns:
        bool: True si le déplacement est réussi, False en cas d'erreur.
    """
    try:
        # Vérifier si le fichier source existe
        if not os.path.isfile(source):
            print(f"Le fichier source '{source}' n'existe pas.")
            return False

        # Créer le répertoire de destination s'il n'existe pas
        if not os.path.exists(destination):
            os.makedirs(destination)

        # Extraire le nom du fichier et son extension
        filename = os.path.basename(source)
        name, ext = os.path.splitext(filename)

        # Vérifier si un fichier du même nom existe déjà
        new_path = os.path.join(destination, filename)
        counter = 2
        while os.path.exists(new_path):
            new_path = os.path.join(destination, f"{name}_{counter}{ext}")
            counter += 1

        # Déplacer le fichier
        shutil.move(source, new_path)
        print(f"Le fichier '{source}' a été déplacé vers '{new_path}'.")
        return True
    except Exception as e:
        print(f"Erreur lors du déplacement : {e}")
        return False

# Fonction pour supprimer les fichiers auxiliaires générés lors de la compilation
def nettoyer_fichiers_auxiliaires(fichier_tex):
    # Obtenir le nom de fichier sans extension
    base_name = os.path.basename(fichier_tex) #os.path.splitext(fichier_tex)[0]
    source_base = fichier_tex.replace(base_name , "")
    #print ( "base_name : " , base_name ) 
    # Extensions des fichiers auxiliaires à supprimer
    extensions_aux = ['.aux', '.log', '.out']
    
    for ext in extensions_aux:
        fichier_aux = base_name.replace(".tex", ext) #+ ext
        #print ( "fichier_aux : " , fichier_aux ) 
        if os.path.exists(fichier_aux):
            os.remove(fichier_aux)
            print(f"Fichier supprimé : {fichier_aux}")
        else:
            print(f"Fichier non trouvé : {fichier_aux}")

    deplacer_fichier(base_name.replace(".tex", ".pdf"), source_base)
    deplacer_fichier(fichier_tex, source_base + "Tex/")

# Fonctions
def update_related_fields(field, value):
    """Met à jour les champs en fonction de `genre` ou `mois`."""
    if field == "genre_proprietaire":
        donnees_quittance["id_genre_proprietaire"] = "M." if value == "Monsieur" else "Mme"
        donnees_quittance["demeurant_genre_proprietaire"] = "demeurant(e)"
    elif field == "genre_locataire":
        donnees_quittance["id_genre_locataire"] = "M." if value == "Monsieur" else "Mme"
        donnees_quittance["demeurant_genre_locataire"] = "demeurant(e)"
        donnees_quittance["Ne_genre"] = "Né" if value == "Monsieur" else "Née"
    elif field == "mois_loyer":
        donnees_quittance["id_mois_loyer"] = f"LOYER-{value}"

def calculate_sums():
    """Calcule automatiquement les sommes."""
    try:

        #nu_loyer = nu_loyer_var.get()
        #nu_loyer = nu_loyer_var.get().replace("/Euro", "").strip() if "/Euro" in nu_loyer_var.get() else nu_loyer_var.get()
        #nu_loyer = nu_loyer_var.get().replace("/Euro", "").strip()


        print ( nu_loyer_var.get() , charge_loyer_var.get() , paye_loyer_var.get()) 
        nu_loyer = int(nu_loyer_var.get().replace("\\EURdig", "").strip())
        charge_loyer = int(charge_loyer_var.get().replace("\\EURdig", "").strip())
        paye_loyer = int(paye_loyer_var.get().replace("\\EURdig", "").strip())

        print( nu_loyer , charge_loyer , paye_loyer ) 

        nu_loyer_var.set(f"{nu_loyer} \\EURdig")
        charge_loyer_var.set(f"{charge_loyer} \\EURdig")
        paye_loyer_var.set(f"{paye_loyer} \\EURdig")
        
        somme_loyer = nu_loyer + charge_loyer
        somme_du = somme_loyer - paye_loyer

        loyer_var.set(f"{somme_loyer} \\EURdig")
        due_var.set(f"{somme_du} \\EURdig")
    except ValueError:
        loyer_var.set("Erreur")
        due_var.set("Erreur")

def select_date(field, var):
    """Ouvre un calendrier pour sélectionner une date."""
    def set_date():
        selected_date = cal.get_date()
        var.set(selected_date)
        window.destroy()

    window = tk.Toplevel(root)
    cal = Calendar(window, date_pattern="dd/mm/yyyy")
    cal.pack(pady=10)
    ttk.Button(window, text="Sélectionner", command=set_date).pack(pady=5)

def format_phone(entry):
    """
    Formate automatiquement les numéros de téléphone pour le format : 0612~34~56~78.
    
    Args:
        entry (tk.Entry): Le champ d'entrée contenant le numéro de téléphone.
    """
    # Récupérer la variable associée
    var = entry.get()
    
    # Nettoyer la valeur
    value = var.strip().replace("~", "").replace(" ", "")
    
    # Vérifier la validité
    if len(value) == 10 and value.isdigit():
        # Formater avec le séparateur spécifique
        formatted = value[:4] + "~" + "~".join([value[i:i+2] for i in range(4, len(value), 2)])
        # Remplir le champ avec le formatage
        entry.delete(0, tk.END)
        entry.insert(0, formatted)
        return entry
    else:
        # Optionnel : Message d'erreur si le format est incorrect
        print("Numéro de téléphone invalide.")
        return var

    


def get_month_year_in_french(date_str):
    # Définir la locale en français
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    
    # Convertir la chaîne en objet datetime
    date = datetime.strptime(date_str, "%d/%m/%Y")
    
    # Formater le mois et l'année en français
    return date.strftime("%B %Y").capitalize()

def get_months_range(debut_loyer, fin_loyer):
    # Définir la locale en français
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    
    # Convertir les chaînes de dates en objets datetime
    debut_date = datetime.strptime(debut_loyer, "%d/%m/%Y")
    fin_date = datetime.strptime(fin_loyer, "%d/%m/%Y")
    
    # Initialiser la liste des mois
    mois = []
    
    # Ajouter chaque mois au format 'Mois YYYY'
    current_date = debut_date.replace(day=1)  # Aller au premier jour du mois de début
    while current_date <= fin_date:
        mois.append(current_date.strftime("%B %Y").capitalize())
        # Passer au mois suivant
        next_month = current_date.month % 12 + 1
        year_increment = current_date.year + (current_date.month // 12)
        current_date = current_date.replace(year=year_increment, month=next_month)
    
    return mois



def generate_random_dates(month_year):
    # Définir la locale en français
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    
    # Convertir "Mois YYYY" en une date correspondante au premier jour du mois
    date = datetime.strptime(month_year, "%B %Y")
    
    # Générer une première date entre le 1er et le 10 du mois
    first_random_day = random.randint(1, 10)
    first_random_date = date + timedelta(days=first_random_day - 1)
    
    # Générer une deuxième date dans les 10 jours après la première date
    second_random_day_offset = random.randint(1, 10)
    second_random_date = first_random_date + timedelta(days=second_random_day_offset)
    
    # Vérifier que la deuxième date ne dépasse pas la fin du mois
    _, last_day_of_month = calendar.monthrange(date.year, date.month)
    if second_random_date.day > last_day_of_month:
        second_random_date = datetime(date.year, date.month, last_day_of_month)
    
    # Retourner les dates au format "DD/MM/YYYY"
    return first_random_date.strftime("%d/%m/%Y"), second_random_date.strftime("%d/%m/%Y")




def f_donnees_quittance(month) :
    donnees_quittance = {} 
    
    donnees_quittance["modele_path"] = modele_path_var.get()
    #donnees_quittance["sortie_path"] = sortie_path_var.get()
    donnees_quittance["sortie_path"] = proprietaire_nom.get() +"/" + locataire_nom.get() + "/quittance_" + month.replace(" ", "_") + ".tex"
    
    donnees_quittance["genre_proprietaire"] = genre_proprietaire_var.get()
    donnees_quittance["id_genre_proprietaire"] = "M." if genre_proprietaire_var.get() == "Monsieur" else "Mme."
    donnees_quittance["demeurant_genre_proprietaire"] = "demeurant" if genre_proprietaire_var.get() == "Monsieur" else "demeurante"
    donnees_quittance["Ne_genre_proprietaire"] = "né le " if genre_proprietaire_var.get() == "Monsieur" else "née le"
    donnees_quittance["nom_proprietaire"] = proprietaire_nom.get()
    donnees_quittance["adresse_proprietaire"] = proprietaire_adresse.get()
    donnees_quittance["tel_proprietaire"] = format_phone(proprietaire_tel).get().replace(" ", "~")
    donnees_quittance["mail_proprietaire"] = proprietaire_mail.get()

    donnees_quittance["numero_allocataire"] = numero_allocataire.get()
    donnees_quittance["genre_locataire"] = genre_locataire.get()
    donnees_quittance["id_genre_locataire"] = "M." if genre_locataire.get() == "Monsieur" else "Mme."
    donnees_quittance["demeurant_genre_locataire"] = "demeurant" if genre_locataire.get() == "Monsieur" else "demeurante"
    donnees_quittance["Ne_genre_locataire"] = "né le " if genre_locataire.get() == "Monsieur" else "née le"
    donnees_quittance["nom_locataire"] = locataire_nom.get()
    donnees_quittance["date_naissance_locataire"] = date_naissance_locataire.get()
    donnees_quittance["lieu_naissance_locataire"] = lieu_naissance_locataire.get()
    donnees_quittance["adresse_locataire"] = locataire_adresse.get()
    donnees_quittance["preffession_locataire"] = preffession_locataire.get()
    donnees_quittance["tel_locataire"] = format_phone(locataire_tel).get().replace(" ", "~")
    donnees_quittance["mail_locataire"] = locataire_mail.get()

    donnees_quittance["debut_loyer"] = debut_loyer.get()
    donnees_quittance["fin_loyer"] = fin_loyer.get()
    #donnees_quittance["mois_loyer"] = mois_loyer_var.get()
    donnees_quittance["mois_loyer"] = month
    donnees_quittance["id_mois_loyer"] = f"LOYER-{month}"
    donnees_quittance["somme_nu_loyer"] = f"{float(somme_nu.get().replace("\\EURdig", "").strip())} \\EURdig"
    donnees_quittance["somme_charge_loyer"] = f"{float(somme_charge.get().replace("\\EURdig", "").strip())} \\EURdig"
    somme_totale = float(somme_nu.get().replace("\\EURdig", "").strip()) + float(somme_charge.get().replace("\\EURdig", "").strip())
    somme_paye_val = float(somme_paye.get().replace("\\EURdig", "").strip())
    somme_du_val = somme_totale - somme_paye_val
    donnees_quittance["somme_paye"] = f"{somme_paye_val:.2f} \\EURdig"
    donnees_quittance["somme_loyer"] = f"{somme_totale:.2f} \\EURdig"
    donnees_quittance["somme_paye_loyer"] = f"{somme_paye_val:.2f} \\EURdig"
    donnees_quittance["somme_du_loyer"] = f"{somme_du_val:.2f} \\EURdig"

    date_loyer ,  fais_le = generate_random_dates(month)
    donnees_quittance["date_loyer"] = date_loyer#.get()
    donnees_quittance["fais_le"] = fais_le#.get()
    donnees_quittance["lieu_fait"] = lieu_fait_var.get()
    donnees_quittance["mode_payement"] = mode_payement_var.get()

    donnees_quittance["adresse_loyer"] = adresse_loyer.get()

    # Afficher le dictionnaire
    #print(donnees_quittance)

    return donnees_quittance

def valider():

    mois = get_months_range(debut_loyer_var.get(), fin_loyer_var.get())
    for month in mois :
        print (" Moi : " , month ) 
        
        donnees_quittance = f_donnees_quittance(month)
        # Appeler la fonction de génération de quittance
        generer_quittance(donnees_quittance)

# Dictionnaire pour stocker les données
donnees_quittance = {
    "modele_path" : "quittance_modele_4.tex",
    "sortie_path" : "quittance.tex",
    
    "genre_proprietaire": "Monsieur",
    "id_genre_proprietaire" : "M.",
    "nom_proprietaire": "Paul Martin",
    "demeurant_genre_proprietaire": "demeurant",
    "adresse_proprietaire": "456 Rue de Lyon, 69001 Lyon",
    "tel_proprietaire": "0606~0606~07",
    "mail_proprietaire": "paul.martin@example.com",

    "numero_allocataire": "....",
    "genre_locataire": "Monsieur",
    "nom_locataire": "Jean Dupont",
    "Ne_genre": "Né",
    "date_naissance_locataire": "01/01/1980",
    "lieu_naissance_locataire": "Saint - Paul",
    "demeurant_genre_locataire": "demeurant",
    "adresse_locataire": "123 Rue de Paris, 75001 Paris",
    "preffession_locataire": "Ingénieur",
    "tel_locataire": "0707070707",
    "mail_locataire": "jean.dupont@example.com",

    "debut_loyer" : "01/12/2024",
    "fin_loyer" : "01/12/2025",
    "mois_loyer" : "Descembre 2024",
    "id_mois_loyer" : "LOYET-Descembre 2024",
    "id_genre_locataire" : "M.",
    "somme_nu_loyer": r"580 \EURdig",
    "somme_charge_loyer": r"70 \EURdig",
    "somme_loyer": r"650 \EURdig",
    "somme_paye_loyer": r"600 \EURdig",
    "somme_du_loyer": r"50 \EURdig",
    "date_loyer" : "01/12/2024",
    "adresse_loyer" : "6 rue de la Harpe 75019 Paris",
    "fais_le" : "03/12/2024",
    "lieu_fait" : "Paris",
    "mode_payement" : "Virement bancaire"
    
}

# Fenêtre principale
root = tk.Tk()
root.title("Remplir les informations pour la quittance")
#root.geometry("300x600")
root.geometry()

# Variables

modele_path_var = tk.StringVar(value=donnees_quittance["modele_path"])
sortie_path_var = tk.StringVar(value=donnees_quittance["sortie_path"])

genre_proprietaire_var = tk.StringVar(value=donnees_quittance["genre_proprietaire"])
nom_proprietaire_var = tk.StringVar(value=donnees_quittance["nom_proprietaire"])
adresse_proprietaire_var = tk.StringVar(value=donnees_quittance["adresse_proprietaire"])
tel_proprietaire_var = tk.StringVar(value=donnees_quittance["tel_proprietaire"])
mail_proprietaire_var = tk.StringVar(value=donnees_quittance["mail_proprietaire"])

numero_allocataire_var = tk.StringVar(value=donnees_quittance["numero_allocataire"])
genre_locataire_var = tk.StringVar(value=donnees_quittance["genre_locataire"])
nom_locataire_var = tk.StringVar(value=donnees_quittance["nom_locataire"])
date_naissance_locataire_var = tk.StringVar(value=donnees_quittance["date_naissance_locataire"])
lieu_naissance_locataire_var = tk.StringVar(value=donnees_quittance["lieu_naissance_locataire"])
adresse_locataire_var = tk.StringVar(value=donnees_quittance["adresse_locataire"])
preffession_locataire_var = tk.StringVar(value=donnees_quittance["preffession_locataire"])
tel_locataire_var = tk.StringVar(value=donnees_quittance["tel_locataire"])
mail_locataire_var = tk.StringVar(value=donnees_quittance["mail_locataire"])

debut_loyer_var = tk.StringVar(value=donnees_quittance["debut_loyer"])
fin_loyer_var = tk.StringVar(value=donnees_quittance["fin_loyer"])

mois_loyer_var = tk.StringVar(value=donnees_quittance["mois_loyer"])

adresse_loyer_var = tk.StringVar(value=donnees_quittance["adresse_loyer"])

nu_loyer_var = tk.StringVar(value=donnees_quittance["somme_nu_loyer"])
charge_loyer_var = tk.StringVar(value=donnees_quittance["somme_charge_loyer"])
paye_loyer_var = tk.StringVar(value=donnees_quittance["somme_paye_loyer"])
loyer_var = tk.StringVar(value=donnees_quittance["somme_loyer"])
due_var = tk.StringVar(value=donnees_quittance["somme_du_loyer"])

date_loyer_var = tk.StringVar(value=donnees_quittance["date_loyer"])
fais_le_var = tk.StringVar(value=donnees_quittance["fais_le"])
lieu_fait_var = tk.StringVar(value=donnees_quittance["lieu_fait"])
mode_payement_var = tk.StringVar(value=donnees_quittance["mode_payement"])  

# Widgets

# Configurer les colonnes 
root.grid_columnconfigure(0, weight=1)  # Colonne 0 s'étire avec le poids 1
root.grid_columnconfigure(1, weight=1)  

# Configurer les lignes Models
root.grid_rowconfigure(0, weight=1)  # Ligne 0 s'étire avec le poids 1

ttk.Label(root, text="Model :").grid(row=0, column=0, sticky="e", padx=10, pady=5)
ttk.Combobox(root, textvariable=modele_path_var, values=["quittance_modele_1.tex" , "quittance_modele_2.tex", "quittance_modele_3.tex", "quittance_modele_4.tex"]).grid(row=0, column=1 , sticky="e", padx=10, pady=5)

# Configurer les lignes Propriétaire
root.grid_rowconfigure(1, weight=1) 
root.grid_rowconfigure(2, weight=1) 
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1) 
root.grid_rowconfigure(5, weight=1) 
root.grid_rowconfigure(6, weight=1)

tk.Label(root, text="Propriétaire").grid(row=1, column=0, columnspan=2)

ttk.Label(root, text="Genre :").grid(row=2, column=0)
genre_proprietaire = ttk.Combobox(root, textvariable=genre_proprietaire_var, values=["Monsieur", "Madame"])
genre_proprietaire.grid(row=2, column=1)

ttk.Label(root, text="Nom :").grid(row=3, column=0)
proprietaire_nom = ttk.Entry(root , textvariable=nom_proprietaire_var)
proprietaire_nom.grid(row=3, column=1)

ttk.Label(root, text="Adresse :").grid(row=4, column=0)
proprietaire_adresse = ttk.Entry(root , textvariable=adresse_proprietaire_var)
proprietaire_adresse.grid(row=4, column=1)

ttk.Label(root, text="Téléphone :").grid(row=5, column=0)
proprietaire_tel = ttk.Entry(root , textvariable=tel_proprietaire_var)
proprietaire_tel.grid(row=5, column=1)

ttk.Label(root, text="E-mail :").grid(row=6, column=0)
proprietaire_mail = ttk.Entry(root , textvariable=mail_locataire_var)
proprietaire_mail.grid(row=6, column=1)

# Configurer les lignes Locataire
root.grid_rowconfigure(7, weight=1) 
root.grid_rowconfigure(8, weight=1) 
root.grid_rowconfigure(9, weight=1)
root.grid_rowconfigure(10, weight=1) 
root.grid_rowconfigure(11, weight=1) 
root.grid_rowconfigure(12, weight=1)
root.grid_rowconfigure(13, weight=1) 
root.grid_rowconfigure(14, weight=1) 
root.grid_rowconfigure(15, weight=1)
root.grid_rowconfigure(16, weight=1) 

tk.Label(root, text="Locataire").grid(row=7, column=0, columnspan=2)

ttk.Label(root, text="Numéro Allocataire :").grid(row=8, column=0)
numero_allocataire = ttk.Entry(root, textvariable=numero_allocataire_var)
numero_allocataire.grid(row=8, column=1)

ttk.Label(root, text="Genre :").grid(row=9, column=0)
genre_locataire = ttk.Combobox(root, textvariable=genre_locataire_var, values=["Monsieur", "Madame"])
genre_locataire.grid(row=9, column=1)

ttk.Label(root, text="Nom :").grid(row=10, column=0)
locataire_nom = ttk.Entry(root , textvariable=nom_locataire_var)#.grid(row=10, column=1)
locataire_nom.grid(row=10, column=1)

ttk.Label(root, text="Date de naissance :").grid(row=11, column=0)
date_naissance_locataire = ttk.Entry(root , textvariable=date_naissance_locataire_var)
date_naissance_locataire.grid(row=11, column=1)
ttk.Button(root, text="📅", command=lambda: select_date("date_naissance_locataire", date_naissance_locataire_var)).grid(row=11, column=2)

ttk.Label(root, text="Lieu de naissance :").grid(row=12, column=0)
lieu_naissance_locataire = ttk.Entry(root , textvariable=lieu_naissance_locataire_var)
lieu_naissance_locataire.grid(row=12, column=1)

ttk.Label(root, text="Adresse :").grid(row=13, column=0)
locataire_adresse = ttk.Entry(root , textvariable=adresse_locataire_var)
locataire_adresse.grid(row=13, column=1)

ttk.Label(root, text="Preffession :").grid(row=14, column=0)
preffession_locataire = ttk.Entry(root , textvariable=preffession_locataire_var)
preffession_locataire.grid(row=14, column=1)

ttk.Label(root, text="Téléphone :").grid(row=15, column=0)
locataire_tel = ttk.Entry(root , textvariable=tel_locataire_var)
locataire_tel.grid(row=15, column=1)

ttk.Label(root, text="E-mail :").grid(row=16, column=0)
locataire_mail = ttk.Entry(root , textvariable=mail_locataire_var)
locataire_mail.grid(row=16, column=1)

# Configurer les lignes Locataire
root.grid_rowconfigure(17, weight=1) 
root.grid_rowconfigure(18, weight=1) 
root.grid_rowconfigure(19, weight=1)
root.grid_rowconfigure(20, weight=1) 
root.grid_rowconfigure(21, weight=1) 
root.grid_rowconfigure(22, weight=1)
root.grid_rowconfigure(23, weight=1) 
root.grid_rowconfigure(24, weight=1) 
root.grid_rowconfigure(25, weight=1)
root.grid_rowconfigure(26, weight=1)
root.grid_rowconfigure(27, weight=1) 
root.grid_rowconfigure(28, weight=1) 
root.grid_rowconfigure(29, weight=1) 

tk.Label(root, text="Loyer").grid(row=17, column=0, columnspan=2)
#ttk.Label(root, text="Mois :").grid(row=14, column=0)
#ttk.Combobox(root, textvariable=mois_loyer_var, values=["Novembre 2024", "Décembre 2024", "Janvier 2025"]).grid(row=14, column=1)

ttk.Label(root, text="Debut Loyer:").grid(row=18, column=0)
debut_loyer = ttk.Entry(root, textvariable=debut_loyer_var)
debut_loyer.grid(row=18, column=1)
ttk.Button(root, text="📅", command=lambda: select_date("debut_loyer", debut_loyer_var)).grid(row=18, column=2)

ttk.Label(root, text="Fin Loyer:").grid(row=19, column=0)
fin_loyer = ttk.Entry(root, textvariable=fin_loyer_var)
fin_loyer.grid(row=19, column=1)
ttk.Button(root,  text="📅", command=lambda: select_date("fin_loyer", fin_loyer_var)).grid(row=19, column=2)

ttk.Label(root, text="Adresse Loyer:").grid(row=20, column=0)
adresse_loyer = ttk.Entry(root , textvariable=adresse_loyer_var)
adresse_loyer.grid(row=20, column=1)

ttk.Label(root, text="Loyer nu (€) :").grid(row=21, column=0)
somme_nu = ttk.Entry(root , textvariable=nu_loyer_var)
somme_nu.grid(row=21, column=1)

ttk.Label(root, text="Charges (€) :").grid(row=22, column=0)
somme_charge = ttk.Entry(root , textvariable=charge_loyer_var)
somme_charge.grid(row=22, column=1)

ttk.Label(root, text="Payé (€) :").grid(row=23, column=0)
somme_paye = ttk.Entry(root , textvariable=paye_loyer_var)
somme_paye.grid(row=23, column=1)

ttk.Label(root, text="Mode de payement :").grid(row=24, column=0)
mode_payement = ttk.Entry(root , textvariable=mode_payement_var)
mode_payement.grid(row=24, column=1)


ttk.Button(root, text="Calculer", command=calculate_sums).grid(row=25, column=2, columnspan=2)

ttk.Label(root, text="Somme Loyer (€) :").grid(row=25, column=0)
loyer = ttk.Entry(root, textvariable=loyer_var, state="readonly")
loyer.grid(row=25, column=1)

ttk.Label(root, text="Somme Due (€) :").grid(row=26, column=0)
due = ttk.Entry(root, textvariable=due_var, state="readonly")
due.grid(row=26, column=1)

#ttk.Label(root, text="Date de paiement :").grid(row=17, column=0)
#date_loyer = Calendar(root)
#date_loyer.grid(row=17, column=1)
#ttk.Label(root, text="Fait le :").grid(row=18, column=0)
#fait_le = Calendar(root)
#fait_le.grid(row=18, column=1)

# Dates
ttk.Label(root, text="Date Loyer:").grid(row=28, column=0)
date_loyer = ttk.Entry(root, textvariable=date_loyer_var)
date_loyer.grid(row=28, column=1)
ttk.Button(root, text="📅", command=lambda: select_date("date_loyer", date_loyer_var)).grid(row=28, column=2)

ttk.Label(root, text="Fait Le:").grid(row=29, column=0)
fais_le = ttk.Entry(root, textvariable=fais_le_var)
fais_le.grid(row=29, column=1)
ttk.Button(root,  text="📅", command=lambda: select_date("fais_le", fais_le_var)).grid(row=29, column=2)

ttk.Label(root, text="Lieu fait :").grid(row=30, column=0)
lieu_fait = ttk.Entry(root , textvariable=lieu_fait_var)
lieu_fait.grid(row=30, column=1)

# Bouton Valider
ttk.Button(root, text="Valider", command=valider).grid(row=31, column=0, columnspan=2)

# Lancer la boucle principale
root.mainloop()