
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppFctMod2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_mod_2.ui", self)
        self.data = data

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshDossierMod(self):

        if not self.ui.lineEdit.text().strip():
            self.ui.tableWidget.setRowCount(0)
            display.refreshLabel(self.ui.label_2, "Veuillez indiquer un numéro de dossier")
        else :
            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT nomSpec,dateRep,noRang,noPlace,libelleCat FROM LesTickets NATURAL JOIN LesSpectacles WHERE noDos = ?", [int(self.ui.lineEdit.text().strip())])
            except Exception as e:
                self.ui.tableWidget.setRowCount(0)
                display.refreshLabel(self.ui.label_2, "Impossible d'afficher ce dossier : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.tableWidget, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_2, "Ce dossier n'existe pas, veuillez saisir un numéro de dossier valide")

    def refreshDossierSupp(self):

        display.refreshLabel(self.ui.label_4, "")

        if not self.ui.lineEdit_2.text().strip():
            self.ui.tableWidget_2.setRowCount(0)
            display.refreshLabel(self.ui.label_4, "Veuillez indiquer un numéro de dossier")
        else :
            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT nomSpec,dateRep,noRang,noPlace,libelleCat FROM LesTickets NATURAL JOIN LesSpectacles WHERE noDos = ?", [int(self.ui.lineEdit_2.text().strip())])
            except Exception as e:
                self.ui.tableWidget_2.setRowCount(0)
                display.refreshLabel(self.ui.label_4, "Impossible d'afficher ce dossier : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.tableWidget_2, result)
                display.refreshLabel(self.ui.label_4, "Cliquez sur le ticket à supprimer")
                if i == 0:
                    display.refreshLabel(self.ui.label_4, "Ce dossier n'existe pas, veuillez saisir un numéro de dossier valide")

    #def refreshToModif(self):
    #    print(self.ui.tableWidget_2.currentRow())

    def SuppTicket(self):

        if self.ui.tableWidget_2.rowCount() == 0:
            if not self.ui.lineEdit_2.text().strip():
                display.refreshLabel(self.ui.label_4, "Veuillez indiquer un numéro de dossier")
            else:
                display.refreshLabel(self.ui.label_4, "Ce dossier n'existe pas, veuillez saisir un numéro de dossier valide")
        else:
            bindings = []
            for i in range(self.ui.tableWidget_2.columnCount()):
                bindings.append(self.ui.tableWidget_2.item(self.ui.tableWidget_2.currentRow(),i).text())

            #on récupère le numéro du spectacle concerné
            cursor = self.data.cursor()
            cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?", [bindings[0]])
            numSpec = cursor.fetchone()
            bindings[0] = numSpec[0]

            try:
                cursor = self.data.cursor()
                cursor.execute("DELETE FROM LesTickets WHERE (noSpec = ? AND dateRep = ? AND noRang = ? AND noPlace = ? AND libelleCat = ?)", bindings)
            except Exception as e:
                display.refreshLabel(self.ui.label_4, "Échec suppression : " + repr(e))
            else:
                display.refreshLabel(self.ui.label_4, "Ticket supprimé!")
                self.ui.tableWidget_2.removeRow(self.ui.tableWidget_2.currentRow())
                if self.ui.tableWidget_2.rowCount() == 0:
                    display.refreshLabel(self.ui.label_4, "Ticket supprimé! Ce dossier est maintenant vide : suppression du dossier...")
                    cursor = self.data.cursor()
                    cursor.execute("DELETE FROM LesDossiers_base WHERE noDos = ?", [int(self.ui.lineEdit_2.text().strip())])
            self.data.commit()

    def lire_ligne(self,ligne_courante):
        # ligne_courante = [noSpec, dateRep, noRang, noPlace, libelleCat, noDos]

        for i in range(self.ui.tableWidget.columnCount()):
            ligne_courante.append(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), i).text())

        # on récupère le numéro du spectacle concerné
        cursor = self.data.cursor()
        cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?", [ligne_courante[0]])
        numSpec = cursor.fetchone()
        ligne_courante[0] = numSpec[0]
        # ajout noDos
        ligne_courante.append(self.ui.lineEdit.text().strip())


    def refreshModif(self):

        #on vide les différents comboBox pour pouvoir les mettre à jour quand on sélectionne un nouveau ticket
        if self.ui.comboCat.count() != 0:
            self.ui.comboCat.clear()
        if self.ui.comboPlace.count() != 0:
            self.ui.comboPlace.clear()
        if self.ui.comboRang.count() != 0:
            self.ui.comboRang.clear()

        #TEST
        ligne_courante = []
        self.lire_ligne(ligne_courante)

        #on initialise les comboBox de l'onglet Modifier
        self.ui.comboRang.addItem(ligne_courante[2])
        cursor = self.data.cursor()
        result = cursor.execute("SELECT DISTINCT noRang FROM LesPlaces WHERE (noRang <> ?)",[ligne_courante[2]])
        for i in result:
            self.ui.comboRang.addItem(str(i[0]))

        self.ui.comboPlace.addItem(ligne_courante[3])
        cursor = self.data.cursor()
        result = cursor.execute("SELECT noPlace FROM LesPlaces WHERE (noPlace <> ? AND noRang = ?)",[ligne_courante[3],ligne_courante[2]])
        for i in result:
            self.ui.comboPlace.addItem(str(i[0]))

        self.ui.comboCat.addItem(ligne_courante[4])
        cursor = self.data.cursor()
        result = cursor.execute("SELECT libelleCat FROM LesCategoriesTickets WHERE (libelleCat <> ?)",[ligne_courante[4]])
        for i in result:
            self.ui.comboCat.addItem(str(i[0]))

    def modifTicket(self):
        if self.ui.tableWidget.rowCount() == 0:
            display.refreshLabel(self.ui.label_2, "Dossier vide : veuillez saisir un numéro de dossier valide")
        else:
            if not self.ui.tableWidget.selectedItems():
                display.refreshLabel(self.ui.label_2, "Sélectionnez un ticket")
            else :
                ligne_courante = []
                self.lire_ligne(ligne_courante)
                try:
                    cursor = self.data.cursor()
                    cursor.execute("UPDATE LesTickets SET noRang = ?, noPlace = ?, libelleCat = ? WHERE (noSpec = ? AND dateRep = ? AND noPlace = ? AND noRang = ?)",
                                    [self.ui.comboRang.currentText(),self.ui.comboPlace.currentText(),self.ui.comboCat.currentText(),ligne_courante[0],ligne_courante[1],ligne_courante[3],ligne_courante[2]])
                except sqlite3.IntegrityError:
                    display.refreshLabel(self.ui.label_2, "Échec de la modification: cette place est déjà prise!")
                except Exception as e:
                    display.refreshLabel(self.ui.label_2, "Échec de la modification : " + repr(e))
                else:
                    display.refreshLabel(self.ui.label_2, "Modification réussie!")
                    self.data.commit()
                    self.refreshDossierMod()