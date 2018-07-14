import sys
import os
import argparse

import xlwings as xw
from PySide2 import QtGui, QtWidgets, QtCore

from MainWindow import Ui_MainWindow
from search import Ui_searchWidget

from network import threads
from util import db, excel
import config_store as config


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.setupUi(self)
    self.show()


class SearchWidget(QtWidgets.QWidget, Ui_searchWidget):
  def __init__(self):
    super(SearchWidget, self).__init__()
    self.setupUi(self)
    self.nextButton.clicked.connect(self.navigationHandler)
    self.prevButton.clicked.connect(self.navigationHandler)
  
  def navigationHandler(self):
    currentWidget = self.stackedWidget.currentWidget()
    if self.sender().objectName() == "nextButton":
      def searchPage():
        self.companySearchThread = threads.CompanySearchThread(
          self,
          self.searchField.text()
        )
        self.companySearchThread.networkState.connect(self.searchSubmitHandler)
        self.companySearchThread.start()

      def companyResultsPage():
        companyListItem = self.companyList.currentItem()
        companyItem = companyListItem.data(QtCore.Qt.UserRole)
        self.getFilingsThread = threads.GetFilingsThread(self, companyItem)
        self.getFilingsThread.networkState.connect(self.getFilingsHelper)
        self.getFilingsThread.start()
      
      def filingsResultPage():
        filingListItems = self.filingsList.selectedItems()
        print(filingListItems)
        for i, filingListItem in enumerate(filingListItems):
          filing = filingListItem.data(QtCore.Qt.UserRole)
          self.getFilingDataThread = threads.GetFilingDataThread(
            self,
            filing,
            i
          )
          self.getFilingDataThread.networkState.connect(
            self.getFilingDataHandler
          )
          self.getFilingDataThread.start()

      exec(currentWidget.objectName() + "()")
    else:
      def searchPage():
        None

      def companyResultsPage():
        self.stackedWidget.setCurrentWidget(self.searchPage)

      def filingsResultPage():
        self.stackedWidget.setCurrentWidget(self.companyResultPage)
      
      exec(currentWidget.objectName() + "()")
  
  @QtCore.Slot(str)
  def searchSubmitHandler(self, e):
    def idle():
      None
    
    def active():
      self.welcomeLabel.setText("Loading...")
    
    def done():
      self.welcomeLabel.setText(
        "Search completed successfully!"
      )
      for companyItem in self.companySearchThread.result:
        item = QtWidgets.QListWidgetItem(self.companyList)
        item.setData(QtCore.Qt.UserRole, companyItem)
        item.setText(companyItem.name)
      self.stackedWidget.setCurrentWidget(self.companyResultsPage)      
    
    exec(e + "()")
  
  @QtCore.Slot(str)
  def getFilingsHelper(self, e):
    def idle():
      None
    
    def active():
      self.companySearchResultsLabel.setText("Loading")
    
    def done():
      self.companySearchResultsLabel.setText("Filings downloaded successfully!")
      for filing in self.getFilingsThread.result.filings:
        print(filing)
        item = QtWidgets.QListWidgetItem(self.filingsList)
        item.setData(QtCore.Qt.UserRole, filing)
        item.setText(
          filing.type +
          ": " +
          filing.date
        )
        self.stackedWidget.setCurrentWidget(self.filingsResultPage)

    def error():
      print(self.getFilingsThread.result)
      self.companySearchResultsLabel.setText(self.getFilingsThread.result)

    exec(e + "()")

  @QtCore.Slot(str)
  def getFilingDataHandler(self, e):
    def idle():
      None
    
    def active():
      self.filingsResultsLabel.setText("Downloading data...")
    
    def done():
      row = wb.app.selection.row
      column = wb.app.selection.column + (e["thread"].index * 7)
      xlRange = xw.sheets.active.range(row, column)
      excel.importDataToExcel(
        e["thread"].result,
        xlRange
      )
      self.filingsResultsLabel.setText("Done importing!")
    
    def error():
      print(self.getFilingDataThread.result)
    
    exec(e["state"] + "()")


if __name__ == "__main__":
  config.dir_path = os.path.dirname(os.path.realpath(__file__))
  
  parser = argparse.ArgumentParser()
  parser.add_argument("workbook")
  args = parser.parse_args()

  db.initDB()

  wb = xw.Book(args.workbook)

  app = QtWidgets.QApplication.instance()
  if app is None:
    app = QtWidgets.QApplication(sys.argv)
  
  mainWindow = MainWindow()
  with open(config.dir_path + "/style/material-blue.qss", "r") as stylesheet:
    mainWindow.setStyleSheet(stylesheet.read())

  searchWidget = SearchWidget()
  mainWindow.setCentralWidget(searchWidget)
  ret = app.exec_()
  app.quit()
  wb.close()
  sys.exit(ret)