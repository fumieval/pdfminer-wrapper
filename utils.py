# https://medium.com/@rishab_dugar/pdf-extraction-retrieving-text-and-tables-together-using-python-1d23727e337f

import pdfplumber
import quadtree
from pdfplumber.utils import *

def to_markdown(pdf: pdfplumber.pdf):
    for page in pdf.pages:
        filtered_page = page
        chars = filtered_page.chars

        textmap = chars_to_textmap(chars, layout=True)
        collider = quadtree.Collider(page.bbox)
        for obj in page.lines:
          collider.add(obj_to_bbox(obj))

        # detect underlines
        page_text = ""
        had_underline = False
        for char, obj in textmap.tuples:
          if char == "\n":
            yield page_text + "\n"
            page_text = ""
            continue
          has_underline = False
          if obj is not None:
            bb = obj_to_bbox(obj)
            for target in collider.find(bb):
              has_underline = True
              break
          if has_underline and not had_underline:
            page_text += "<u>"
          if had_underline and not has_underline:
            page_text += "</u>"
          page_text += char
          had_underline = has_underline
        if had_underline:
          page_text += "</u>"

        yield page_text + "\n"

    pdf.close()
