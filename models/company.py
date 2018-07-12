import requests
import lxml.etree as etree
from models import filings


class Company:
  def __init__(self, cik, name, filings=[]):
    self.cik = cik
    self.name = name
    self.filings = filings

  def getFilings(self):
    payload = {
      "action": "getcompany",
      "CIK": self.cik,
      "output": "atom"
    }
    r = requests.get(
      "https://www.sec.gov/cgi-bin/browse-edgar",
      params=payload
    )
    tree = etree.fromstring(r.content)
    for entry in tree.findall("entry", tree.nsmap):
      switcher = {
        "13F-HR": filings.ThirteenFHR(
          self.cik,
          entry.find("content/filing-date", entry.nsmap).text,
          entry.find("content/filing-type", entry.nsmap).text,
          entry.find("content/accession-nunber", entry.nsmap).text,
          entry.find("content/file-number", entry.nsmap).text,
        ),
      }
      self.filings.append(
        switcher.get(
          entry.find("content/filing-type", entry.nsmap).text,
          filings.Filing(
            self.cik,
            entry.find("content/filing-date", entry.nsmap).text,
            entry.find("content/filing-type", entry.nsmap).text,
            entry.find("content/accession-nunber", entry.nsmap).text,
            entry.find("content/file-number", entry.nsmap).text,
          )
        )
      )
