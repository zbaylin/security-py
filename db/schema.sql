CREATE TABLE "fails_to_deliver" (
  id            INTEGER    PRIMARY KEY,
  cusip         TEXT       NOT NULL,
  ticker        TEXT       NOT NULL,
  description   TEXT       NOT NULL
);

CREATE TABLE "files" (
  filename TEXT     NOT NULL,
  scanned  INTEGER  NOT NULL
); 