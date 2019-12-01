
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppFctMod1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_mod_1.ui", self)
        self.data = data

        self.ui.comboBox.addItem('')

        cursor = self.data.cursor()
        result = cursor.execute("SELECT DISTINCT nomSpec FROM LesSpectacles")
        for i in result:
            self.ui.comboBox.addItem(str(i[0]))

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshIns(self):

        display.refreshLabel(self.ui.label_3, "")
        try:
            cursor = self.data.cursor()
            cursor.execute("INSERT INTO LesRepresentations_base(noSpec,dateRep,promoRep) VALUES (?,?,?)", [self.ui.comboBox.currentText(), self.ui.doubleSpinBox.value(), self.ui.dateTimeEdit.dateTime().toString('DD/MM/YYYY HH:MM')])
        except Exception as e:
            display.refreshLabel(self.ui.label_3, "Impossible d'ajouter cette représentation : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_3, "Ajout de représenation réussie!")