
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
    def refreshDossier(self):

        display.refreshLabel(self.ui.label_2, "")

        if not self.ui.lineEdit.text().strip():
            self.ui.tableWidget.setRowCount(0)
            display.refreshLabel(self.ui.label_2, "Veuillez indiquer un numéro de dossier")
        else :
            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT nomSpec,dateRep,noPlace,noRang,libelleCat FROM LesTickets NATURAL JOIN LesSpectacles WHERE noDos = ?", [int(self.ui.lineEdit.text().strip())])
            except Exception as e:
                self.ui.tableWidget.setRowCount(0)
                display.refreshLabel(self.ui.label_2, "Impossible d'afficher ce dossier : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.tableWidget, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_2, "Ce dossier n'existe pas")