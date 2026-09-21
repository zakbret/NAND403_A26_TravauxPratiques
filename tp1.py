import sys
import json
import os

from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QWidget, QLabel



with open(sys.argv[1], "r", encoding='utf-8') as f:
    data = json.load(f)
    
information = os.path.getsize(sys.argv[1])

total = len(data)

#crée l'application
app = QApplication(sys.argv)

#crée la fenêtre principale
fenetre_principale = QWidget()
disposition = QVBoxLayout()

#crée le tableau
tableau = QTableWidget()
barre_de_recherche = QLineEdit()
nom_fichier = QLabel()
poid_du_fichier = QLabel()
nombre_elements = QLabel()

#initialise la fenêtre principale
disposition.addWidget(barre_de_recherche)
disposition.addWidget(tableau)
disposition.addWidget(nom_fichier)
disposition.addWidget(poid_du_fichier)
disposition.addWidget(nombre_elements)
fenetre_principale.setLayout(disposition)

#initialise le tableau
tableau.setRowCount(len(data))
tableau.setColumnCount(len(data[0]))
tableau.setHorizontalHeaderLabels(data[0].keys())

#affihe le nom du fichier
nom_fichier.setText("Nom du fichier : " + os.path.basename(sys.argv[1]))

#affiche le poid du fichier
poid_du_fichier.setText("taille : " + str(information) + " octets")

#affiche le nombre d'éléments
nombre_elements.setText("nombre d'éléments : " + str(total))

#passe chaque ligne de data et me donne le numéro de ligne et le contenu de la ligne elle même
for numero_ligne, ligne in enumerate(data):
    #passe chaque colone et donne l'ensemble de nom de champ et de valeur et ensuite lui associe un numéro avec enumerate
    #numero_colone = la position de la colonne, nom_colone = le titre du champ, valeur = le contenu
    for numero_colone, (nom_colone, valeur) in enumerate(ligne.items()):

        item_valeur = QTableWidgetItem(str(valeur))
        tableau.setItem(numero_ligne, numero_colone, item_valeur)
        
        


#fonction qui vérifie chaque case et me dit si l'une des cases correspond au texte que je recherche
def rechercher_dans_tableau(texte):

    #passe chaque ligne selon le nombre de ligne dans le tableau
    for ligne in range (tableau.rowCount()):
        correspond = False

        #passe chaque colone selon le nombre de colone dans le tableau
        for colone in range (tableau.columnCount()):

            #stock l'item dans la variable case pour chaque croisement ligne colone
            case = tableau.item(ligne, colone)

            #mets tout en minuscule et verifie si le texte rechercher est contenue dans la case
            if  case and texte.lower() in case.text().lower():
                correspond = True
                break

        #cache les lignes qui ne correspondent pas
        tableau.setRowHidden(ligne, not correspond)

#a chaque fois que je tappe quelque chose dans la barre de recherche ça lance la fonction rechercher_dans_tableau
barre_de_recherche.textChanged.connect(rechercher_dans_tableau)

#active le trie du tableau
tableau.setSortingEnabled(True)


#montre la fenêtre principale
fenetre_principale.show()
sys.exit(app.exec())
