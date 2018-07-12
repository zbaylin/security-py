import config_store as config
import sqlite3
import glob
import csv


def initDB():
  config.dbconn = sqlite3.connect("db/data.db")
  config.db = config.dbconn.cursor()
  scanFails()


def scanFails():
  for file in glob.glob("assets/f2d/*.txt"):
    result = config.db.execute("SELECT * FROM files WHERE filename = ?", (file,))
    if result.fetchone() is None:
      importFail(file)


def importFail(filename):
  csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
  rows = []
  with open(filename, "r") as file:
    for row in csv.DictReader(file, dialect="piper"):
      rows.append(
        (
          row["CUSIP"],
          row["SYMBOL"],
          row["DESCRIPTION"]
        )
      )
  config.db.executemany(
    "INSERT INTO fails_to_deliver (cusip, ticker, description) VALUES (?, ?, ?)",
    rows
  )
  config.db.execute(
    "INSERT INTO files (filename, scanned) VALUES (?, ?)",
    (filename, 1)
  )

  config.dbconn.commit()