import pprint

from util import db
from models import company


if __name__ == "__main__":
  pp = pprint.PrettyPrinter(indent=2)
  db.initDB()

  companyList = company.searchCompanies(input("Please enter a company name: "))

  print("\n\nSelect a company from the list")
  for i, companyItem in enumerate(companyList):
    print(i, companyItem.name)
  companyItem = companyList[int(input("Company number: "))]
  companyItem.getFilings()