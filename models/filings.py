from util import parse, convert

import lxml.etree as etree
import requests


class Filing:
  def __init__(self, cik, date, type, accessionNumber, number):
    self.cik = parse.parseCIK(cik)
    self.date = date
    self.type = type
    self.accessionNumber = parse.parseNumString(accessionNumber)
    self.number = parse.parseNumString(number)


class ThirteenFHR(Filing):
  class Data:
    def __init__(
      self,
      issuerName,
      classTitle,
      cusip,
      value,
      discretion,
      investmentType,
      votingAuthority
    ):
      self.issuerName = issuerName
      self.classTitle = classTitle
      self.cusip = cusip
      self.ticker = convert.cusipToTicker(cusip)
      self.value = value
      self.discretion = discretion
      self.investmentType = investmentType
      self.votingAuthority = votingAuthority

  def __init__(self, cik, date, type, accessionNumber, number):
    super().__init__(cik, date, type, accessionNumber, number)
    self.data = []

  def getData(self):
    r = requests.get(
      "https://www.sec.gov/Archives/edgar/data/" +
      self.cik +
      "/" +
      self.accessionNumber +
      "/" +
      "infotable.xml"
    )

    tree = etree.fromstring(r.content)

    for node in tree.findall("infoTable", tree.nsmap):
      self.data.append(
        ThirteenFHR.Data(
          node.find("nameOfIssuer", node.nsmap).text,
          node.find("titleOfClass", node.nsmap).text,
          node.find("cusip", node.nsmap).text,
          node.find("value", node.nsmap).text,
          node.find("shrsOrPrnAmt/sshPrnamtType", node.nsmap).text,
          node.find("investmentDiscretion", node.nsmap).text,
          {
            "sole": node.find("votingAuthority/Sole", node.nsmap).text,
            "shared": node.find("votingAuthority/Shared", node.nsmap).text,
            "none": node.find("votingAuthority/None", node.nsmap).text,
          }
        )
      )
    