
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

        display.refreshLabel(self.ui.label_2, "")

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
                    display.refreshLabel(self.ui.label_2, "Ce dossier n'existe pas")

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
                    display.refreshLabel(self.ui.label_4, "Ce dossier n'existe pas")

    #def refreshToModif(self):
    #    print(self.ui.tableWidget_2.currentRow())

    def SuppTicket(self):

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
            if (self.ui.tableWidget_2.rowCount() == 0):
                display.refreshLabel(self.ui.label_4, "Ticket supprimé! Ce dossier est maintenant vide : suppression du dossier...")
                cursor = self.data.cursor()
                cursor.execute("DELETE FROM LesDossiers_base WHERE noDos = ?", [int(self.ui.lineEdit_2.text().strip())])
        self.data.commit()
