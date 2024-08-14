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
        had_strikethrough = False

        for char, obj in textmap.tuples:
          if char == "\n":
            if had_underline:
              page_text += "</u>"
            if had_strikethrough:
              page_text += "~~"
            yield page_text + "\n"
            page_text = ""
            had_underline = False
            had_strikethrough = False
            continue

          has_underline = False
          has_strikethrough = False
          if obj is not None:
            bb = obj_to_bbox(obj)
            for target in collider.find(bb):
              relativePosition = (target[1] - bb[1]) / (bb[3] - bb[1])
              if relativePosition > 0.8:
                has_underline = True
              else:
                has_strikethrough = True
          if has_underline and not had_underline:
            page_text += "<u>"
          if had_underline and not has_underline:
            page_text += "</u>"
          if has_strikethrough != had_strikethrough:
            page_text += "~~"
          had_underline = has_underline
          had_strikethrough = has_strikethrough

          page_text += char

        if had_underline:
          page_text += "</u>"
        if had_strikethrough:
          page_text += "~~"

        yield page_text + "\n"

    pdf.close()
