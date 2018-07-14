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
      self.result = e
      self.networkState.emit(NetworkState.error)
      pass


class GetFilingsThread(QtCore.QThread):
  networkState = QtCore.Signal(str)
  result = ""

  def __init__(self, parent, companyItem, index=0):
    super(GetFilingsThread, self).__init__(parent)
    self.company = companyItem
    self.index = index
    self.networkState.emit(NetworkState.idle)

  def run(self):
    self.networkState.emit(NetworkState.active)
    try:
      self.company.getFilings()
      self.result = self.company
      self.networkState.emit(NetworkState.done)
      pass
    except Exception as e:
      self.result = e
      self.networkState.emit(NetworkState.error)
      pass


class GetFilingDataThread(QtCore.QThread):
  networkState = QtCore.Signal(dict)
  result = ""

  def __init__(self, parent, filing, index=0):
    super(GetFilingDataThread, self).__init__(parent)
    self.filing = filing
    self.index = index
    self.networkState.emit(
      {
        "state": NetworkState,
        "thread": self
      }
    )
  
  def run(self):
    self.networkState.emit(
      {
        "state": NetworkState.active,
        "thread": self
      }
    )
    try:
      self.filing.getData()
      self.result = self.filing
      self.networkState.emit(
        {
          "state": NetworkState.done,
          "thread": self
        }
      )
      pass
    except Exception as e:
      print(e)
      self.result = e
      self.networkState.emit(
        {
          "state": NetworkState.error,
          "thread": self
        }
      )
    