
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppFctInt2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_int_2.ui", self)
        self.data = data
        self.refreshPlacesRes()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshPlacesRes(self):

        display.refreshLabel(self.ui.label_fct_int_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT nomSpec,dateRep, nbPtot - nbPlacesRestantes FROM (SELECT noSpec, nomSpec, dateRep, nbPlacesRestantes, (SELECT COUNT(noPlace) FROM LesPlaces) nbPtot FROM LesRepresentations NATURAL JOIN LesSpectacles)")
        except Exception as e:
            self.ui.table_fct_int_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_int_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_int_2, result)