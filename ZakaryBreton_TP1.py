import sys
import json
import os

from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QWidget, QLabel, QMessageBox

#crée l'application
app = QApplication([])

try:
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)

#s'il y a une erreur dans le path un message d'erreur apparait
except FileNotFoundError:
    
    message_erreur = QMessageBox()
    message_erreur.setText("Fichier non trouvé")
    message_erreur.setIcon(QMessageBox.Critical)
    message_erreur.exec()
    sys.exit()

#si le fichier n'est pas un json ou qu'il est complètement vide un message d'erreur apparait
except json.JSONDecodeError:

    message_erreur = QMessageBox()
    message_erreur.setText("Fichier non valide")
    message_erreur.setIcon(QMessageBox.Critical)
    message_erreur.exec()
    sys.exit()

#si aucun path n'est mis, un message d'erreur apparait
except IndexError:

    message_erreur = QMessageBox()
    message_erreur.setText("Veuillez indiquer un fichier à ouvrir")
    message_erreur.setIcon(QMessageBox.Critical)
    message_erreur.exec()
    sys.exit()

#si le fichier json est vide un message d'erreur apparait
if not data:
    message_erreur = QMessageBox()
    message_erreur.setText("Fichier vide")
    message_erreur.setIcon(QMessageBox.Critical)
    message_erreur.exec()
    sys.exit()

#récupère le poid du fichier en octet
information = os.path.getsize(sys.argv[1])

#mets le nombre de rangées dans une variable
total = len(data)

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
tableau.setRowCount(total)
tableau.setColumnCount(len(data[0]))
tableau.setHorizontalHeaderLabels(data[0].keys())

#affiche le nom du fichier
nom_fichier.setText("Nom du fichier : " + os.path.basename(sys.argv[1]))

#affiche le poids du fichier
poid_du_fichier.setText("taille : " + str(information) + " octets")

#affiche le nombre d'éléments
nombre_elements.setText("nombre d'éléments : " + str(total))

#passe chaque ligne de data et me donne le numéro de ligne et le contenu de la ligne elle même
for numero_ligne, ligne in enumerate(data):
    #passe chaque colonne et donne l'ensemble de nom de champ et de valeur et ensuite lui associe un numéro avec enumerate
    #numero_colonne = la position de la colonne, nom_colonne = le titre du champ, valeur = le contenu
    for numero_colonne, (nom_colonne, valeur) in enumerate(ligne.items()):

        #mets l'item dans le tableau en prenant en compte son numéro de ligne et de colonne ainsi que sa valeur
        tableau.setItem(numero_ligne, numero_colonne, QTableWidgetItem(str(valeur)))
        
        


#fonction qui vérifie chaque case et me dit si l'une des cases correspond au texte que je recherche
def rechercher_dans_tableau(texte):

    #passe chaque ligne selon le nombre de ligne dans le tableau
    for ligne in range (tableau.rowCount()):
        correspond = False

        #passe chaque colonne selon le nombre de colonne dans le tableau
        for colonne in range (tableau.columnCount()):

            #stock l'item dans la variable case pour chaque croisement ligne colonne
            case = tableau.item(ligne, colonne)

            #mets tout en minuscule et vérifie si le texte recherché est contenu dans la case
            if  case and texte.lower() in case.text().lower():
                correspond = True
                break

        #cache les lignes qui ne correspondent pas
        tableau.setRowHidden(ligne, not correspond)

#a chaque fois que je tappe quelque chose dans la barre de recherche ça lance la fonction rechercher_dans_tableau
barre_de_recherche.textChanged.connect(rechercher_dans_tableau)

#active le tri du tableau
tableau.setSortingEnabled(True)


#montre la fenêtre principale
fenetre_principale.show()
sys.exit(app.exec())
