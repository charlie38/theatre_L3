
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppFctInt1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_int_1.ui", self)
        self.data = data
        self.refreshRepVides()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshRepVides(self):

        display.refreshLabel(self.ui.label_fct_int_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec, dateRep FROM LesRepresentations_base EXCEPT SELECT DISTINCT noSpec, dateRep FROM LesTickets")
        except Exception as e:
            self.ui.table_fct_int_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_int_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_int_1, result)