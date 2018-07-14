def importDataToExcel(filing, xlRange):
  print(filing)
  arr = [
    [
      filing.date,
      None,
      None,
      None,
      None,
      None,
      None
    ],
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

  for datum in filing.data:
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
  xlRange.value = arr