import pprint

import requests
from lxml import etree
from util import db
from models.company import Company


def searchCompanies(searchTerm):
  payload = {
    "company": searchTerm,
    "output": "atom"
  }
  r = requests.get("https://www.sec.gov/cgi-bin/browse-edgar", params=payload)
  tree = etree.fromstring(r.content)

  companyList = []
  for company in tree.findall("entry/content/company-info", tree.nsmap):
    companyItem = Company(
      company.find("cik", company.nsmap).text,
      company.find("name", company.nsmap).text
    )
    companyList.append(companyItem)

  return companyList


if __name__ == "__main__":
  pp = pprint.PrettyPrinter(indent=2)
  db.initDB()

  companyList = searchCompanies(input("Please enter a company name: "))

  print("\n\nSelect a company from the list")
  for i, company in enumerate(companyList):
    print(i, company.name)
  company = companyList[int(input("Company number: "))]
  company.getFilings()

  company.filings[0].getData()
  for datum in company.filings[0].data:
    pp.pprint(vars(datum))