# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CadasterImportDockWidget
                                 A QGIS plugin
 Imports XML files from russian state land register
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-02-03
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Kirill Kotelevsky
        email                : thaid@yandex.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import absolute_import

import os

from qgis import gui
from qgis.core import QgsSettings, Qgis
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, QCoreApplication

from .cadaster_import_utils import logMessage

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'cadaster_import_dockwidget_base.ui'))


class CadasterImportDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(CadasterImportDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.selectFileWidget.setFilter('*.xml')
    
    def on_batchImportRadioButton_toggled(self):
        _translate = QCoreApplication.translate
        self.selectFileLabel.setText(_translate("CadasterImportDockWidgetBase", "Выберите папку"))
        self.selectFileWidget.setStorageMode(gui.QgsFileWidget.GetDirectory)
    
    def on_importFileRadioButton_toggled(self):
        _translate = QCoreApplication.translate
        self.selectFileLabel.setText(_translate("CadasterImportDockWidgetBase", "Выберите файл"))
        self.selectFileWidget.setStorageMode(gui.QgsFileWidget.GetFile)
        self.selectFileWidget.setFilter('*.xml')
    
    def on_withoutTransformCheck_stateChanged(self):
        if self.withoutTransformCheck.isChecked():
            self.importProjectionLabel.setVisible(False)
            self.importProjectionSelectionWidget.setVisible(False)
        else:
            self.importProjectionLabel.setVisible(True)
            self.importProjectionSelectionWidget.setVisible(True)
    
    def on_importToDB_toggled(self):
        self.dbFrame.setVisible(True)
    
    def on_impotToLayer_toggled(self):
        self.dbFrame.setVisible(False)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def on_selectFileWidget_fileChanged(self):
        self.analizeButton.setEnabled(True)
        self.importButton.setEnabled(True)

    def on_analizeButton_clicked(self):
        from .parser_1 import Parser
        if self.selectFileWidget.filePath():
          with open(self.selectFileWidget.filePath(), encoding="utf8") as f:
              type = Parser.getFileType(f)
              self.info.setText(type['name'])
