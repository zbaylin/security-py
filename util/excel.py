def importDataToExcel(data, workbook):
  wbRange = workbook.app.selection
  arr = [
    [
      "Issuer Name",
      "Class Title",
      "CUSIP",
      "Ticker/Symbol",
      "Value",
      "Discretion",
      "Type"
    ]
  ]

  for datum in data:
    arr.append(
      [
        datum.issuerName,
        datum.classTitle,
        datum.cusip,
        datum.ticker,
        datum.value,
        datum.discretion,
        datum.investmentType
      ]
    )
  wbRange.value = arr