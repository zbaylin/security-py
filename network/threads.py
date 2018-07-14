from PySide2 import QtCore
from models import company


class ThreadState:
  idle = "idle"
  done = "done"
  error = "error"


class NetworkState(ThreadState):
  active = "active"
  

class CompanySearchThread(QtCore.QThread):
  networkState = QtCore.Signal(str)
  result = ""

  def __init__(self, parent, searchTerm):
    super(CompanySearchThread, self).__init__(parent)
    self.searchTerm = searchTerm
    self.networkState.emit(NetworkState.idle)

  def run(self):
    self.networkState.emit(NetworkState.active)
    try:
      self.result = company.searchCompanies(self.searchTerm)
      self.networkState.emit(NetworkState.done)
      pass
    except Exception as e:
      print(456)
      self.result = e
      self.networkState.emit(NetworkState.error)
      pass


class GetFilingsThread(QtCore.QThread):
  networkState = QtCore.Signal(str)
  result = ""

  def __init__(self, parent, companyItem):
    super(GetFilingsThread, self).__init__(parent)
    self.company = companyItem
    self.networkState.emit(NetworkState.idle)

  def run(self):
    self.networkState.emit(NetworkState.active)
    try:
      self.company.getFilings()
      self.result = self.company.filings
      self.networkState.emit(NetworkState.done)
      pass
    except Exception as e:
      self.result = e
      self.networkState.emit(NetworkState.error)
      pass


class GetFilingDataThread(QtCore.QThread):
  networkState = QtCore.Signal(str)
  result = ""

  def __init__(self, parent, filing):
    super(GetFilingDataThread, self).__init__(parent)
    self.filing = filing
    self.networkState.emit(NetworkState.idle)
  
  def run(self):
    self.networkState.emit(NetworkState.active)
    try:
      self.filing.getData()
      self.result = self.filing.data
      self.networkState.emit(NetworkState.done)
      pass
    except Exception as e:
      print(e)
      self.result = e
      self.networkState.emit(NetworkState.error)
    