import re


def parseNumString(numberString):
  parsed = ""
  for element in re.findall(r"\d+", numberString):
    parsed += element
  return parsed


def parseCIK(cik):
  return re.sub(r'^0+', "", cik)