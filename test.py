import pdfplumber
import utils
import sys

with pdfplumber.open(sys.argv[1]) as pdf:
  for page in utils.to_markdown(pdf):
    print(page)