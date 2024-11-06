# Configurer le nom de la branche par défaut pour tous les nouveaux dépôts (facultatif)
git config --global init.defaultBranch main

# Naviguer vers le répertoire créé par le script
#cd chemin/vers/le/repertoire/quantum-mechanics-thesis

# Initialiser un dépôt Git local et créer la branche main
git init
git checkout -b main

# Ajouter le dépôt GitHub comme remote
git remote add origin git@github.com:THEMEZE/quittance.git

# Ajouter tous les fichiers au dépôt local
git add .

# Faire un commit initial
git commit -m "Initial commit with project structure"

# Pousser les fichiers vers GitHub
git push -u origin main
