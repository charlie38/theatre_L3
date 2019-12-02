
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

        # on initialise comboBox de l'onglet Insérer
        self.ui.comboBox.addItem('')

        cursor = self.data.cursor()
        result = cursor.execute("SELECT DISTINCT nomSpec FROM LesSpectacles")
        for i in result:
            self.ui.comboBox.addItem(str(i[0]))

        # on initialise comboBox_2 de l'onglet Supprimer
        self.ui.comboBox_2.addItem('')

        cursor = self.data.cursor()
        result = cursor.execute("SELECT DISTINCT nomSpec FROM LesSpectacles")
        for i in result:
            self.ui.comboBox_2.addItem(str(i[0]))

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

    def refreshSupp(self):
        display.refreshLabel(self.ui.label_5, "")

        # on récupère le numéro du spectacle concerné
        if not self.ui.comboBox_2.currentText():
            self.ui.tableWidget.setRowCount(0)
            display.refreshLabel(self.ui.label_5, "Veuillez sélectionner un spectacle")
        else:
            cursor = self.data.cursor()
            cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?", [self.ui.comboBox_2.currentText()])
            numSpec = cursor.fetchone()
            binding = numSpec[0]

            try:
                cursor = self.data.cursor()
                result = cursor.execute("SELECT dateRep, promoRep FROM LesRepresentations_base WHERE noSpec = ?",[binding])
            except Exception as e:
                self.ui.tableWidget.setRowCount(0)
                display.refreshLabel(self.ui.label_5, "Impossible d'afficher les représentations : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.tableWidget, result)
                display.refreshLabel(self.ui.label_5, "Cliquez sur la représentation à supprimer")
                if i == 0:
                    display.refreshLabel(self.ui.label_5, "Il n'y a pas de représentations pour ce spectacle")

    def SuppRep(self):
        if not self.ui.comboBox_2.currentText():
            display.refreshLabel(self.ui.label_5, "Veuillez sélectionner un spectacle")
        else:
            if self.ui.tableWidget.rowCount() == 0:
                display.refreshLabel(self.ui.label_5, "Il n'y a pas de représentations pour ce spectacle")
            else:
                # on récupère le numéro du spectacle concerné
                cursor = self.data.cursor()
                cursor.execute("SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?", [self.ui.comboBox_2.currentText()])
                numSpec = cursor.fetchone()
                binding = numSpec[0]

                bindings = []
                for i in range(self.ui.tableWidget.columnCount()):
                    bindings.append(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(),i).text())
                bindings.insert(0,binding)

                try:
                    cursor = self.data.cursor()
                    cursor.execute("DELETE FROM LesRepresentations_base WHERE (noSpec = ? AND dateRep = ?)", [bindings[0],bindings[1]])
                except Exception as e:
                    display.refreshLabel(self.ui.label_5, "Échec suppression : " + repr(e))
                else:
                    display.refreshLabel(self.ui.label_5, "Représentation supprimée!")
                    self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow())
                    if self.ui.tableWidget.rowCount() == 0:
                        display.refreshLabel(self.ui.label_5, "Représentation supprimée! Il n'y a plus de représentations pour ce spectacle")
                    self.data.commit()
