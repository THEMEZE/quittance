# 🧾 Générateur de Quittances de Loyer

Ce projet est une application **Python** avec interface **Tkinter**, permettant de générer automatiquement des **quittances de loyer** à partir des informations saisies par le bailleur.  
Elle calcule les montants dus, ajoute les dates automatiquement 📅, et génère les documents de quittance prêts à l’emploi 💼.

---

## 📘 Exemple de sortie PDF

Voici un exemple du rendu final généré par le programme 👇

### 🪶 Exemple :
<p align="center"> <img src="quittance.pdf" width="450" alt="Aperçu de la quittance PDF"> </p>

📄 Tu peux aussi télécharger le PDF complet ici :
➡️ [Télécharger la quittance PDF](https://github.com/THEMEZE/quittance/raw/main/example_quittance.pdf)
➡️ [Voir l’exemple de quittance PDF](https://github.com/THEMEZE/quittance/blob/main/example_quittance.pdf)

---

## ⚙️ Fonctionnalités principales

✅ Interface graphique simple et intuitive (Tkinter)  
✅ Sélection de dates via un sélecteur intégré 📆  
✅ Calcul automatique des sommes (loyer, charges, dû) 🧮  
✅ Génération automatique de quittances de loyer pour plusieurs mois 🧾  
✅ Saisie complète des informations locataire/bailleur  
✅ Sauvegarde et génération rapide des fichiers  

---

## 🧱 Structure du projet

📦 quittance/
    📜 main.py # Code principal de l'application
    📜 README.md # Ce fichier !
    📜 requirements.txt # Liste des dépendances Python
    📁 Non_Bailleur/ # (optionnel) Dossier de sortie pour les quittances générées


---

## 🧩 Prérequis

- Python **3.10+** 🐍  
- Système compatible : macOS / Windows / Linux  
- Une connexion Internet (optionnelle pour les mises à jour)

---

## 📦 Installation

Ouvre un terminal dans le dossier du projet et lance :


### 1️⃣ Clone le dépôt
```bash
git clone https://github.com/THEMEZE/quittance.git
cd quittance
```

### 2️⃣ Crée un environnement virtuel (recommandé)
```bash
python3 -m venv venv
source venv/bin/activate     # Sur macOS/Linux
venv\Scripts\activate        # Sur Windows
```

### 3️⃣ Installe les dépendances
```bash
pip install -r requirements.txt
```

## ▶️ Lancement de l’application
Une fois les dépendances installées, exécute simplement :
```bash
python main.py
```
L’interface graphique Tkinter s’ouvrira 🎨
Tu pourras alors renseigner les champs, cliquer sur 🧮 Calculer puis sur 🧾 Générer les quittances.

## 📁 Fichier `requirements.txt`
Ce fichier doit contenir les modules utilisés :
```nginx
tkcalendar
pillow
```
(Tkinter est inclus par défaut avec Python, tu n’as pas besoin de l’installer séparément.)

## 💡 Astuce

Si tu veux générer plusieurs quittances d’un coup, tu peux ajouter cette option dans la fonction `valider()` pour parcourir une plage de dates automatiquement 🗓️.

## 💻 Auteur

👤 Guillaume THÉMÈZE
📧 guillaume.themeze@gmail.fr
🌐 GitHub @THEMEZE

GitHub

## 🏁 Licence
Ce projet est distribué sous licence ??? — tu peux le modifier et le réutiliser librement ✨


> “Automatise ton administratif, concentre-toi sur l’essentiel.” 🚀

## ⚙️ Git Mise à jour

```bash
git add .
git commit -m "Mise à jour"
git push
```