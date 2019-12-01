
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
            cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?", [self.ui.comboBox.currentText()])
            numSpec = cursor.fetchone()
            cursor.execute("INSERT INTO LesRepresentations_base(noSpec,dateRep,promoRep) VALUES (?,?,?)", [numSpec[0], self.ui.dateTimeEdit.dateTime().toString('dd/MM/yyyy hh:mm'), self.ui.doubleSpinBox.value()])
        except TypeError:
            display.refreshLabel(self.ui.label_3, "Échec de l'ajout : veuillez choisir un spectacle!")
        except sqlite3.IntegrityError:
            display.refreshLabel(self.ui.label_3, "Échec de l'ajout : cette représentation existe déjà!")
        except Exception as e:
                display.refreshLabel(self.ui.label_3, "Impossible d'ajouter cette représentation : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_3, "Ajout de représentation réussie!")
            self.data.commit()