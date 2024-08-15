# https://medium.com/@rishab_dugar/pdf-extraction-retrieving-text-and-tables-together-using-python-1d23727e337f

import pdfplumber
import quadtree
from pdfplumber.utils import *

class FormatBuffer:
  def __init__(self):
    self.has_underline = False
    self.has_strikethrough = False
    self.text = ""
  def push(self, chunk, has_underline, has_strikethrough):
    if not self.has_strikethrough and has_strikethrough:
      self.text += "~~"
    if not self.has_underline and has_underline:
      self.text += "<u>"
    if self.has_underline and not has_underline:
      self.text += "</u>"
    if self.has_strikethrough and not has_strikethrough:
      self.text += "~~"
    self.text += chunk
    self.has_underline = has_underline
    self.has_strikethrough = has_strikethrough
  def flush(self):
    if self.has_underline:
      self.text += "</u>"
    if self.has_strikethrough:
      self.text += "~~"
    result = self.text
    self.text = ""
    self.has_underline = False
    self.has_strikethrough = False
    return result

def detect_underline_and_strikethrough(collider, obj):
  has_underline = False
  has_strikethrough = False
  if obj is not None:
    bb = obj_to_bbox(obj)
    for target in collider.find(bb):
      ratio = (target[1] - bb[1]) / (bb[3] - bb[1])
      if ratio > 0.8:
        has_underline = True
      else:
        has_strikethrough = True
  return has_underline, has_strikethrough

def page_to_markdown(page):
  chars = page.chars

  textmap = chars_to_textmap(chars, layout=True)

  # Gather all lines in the page
  collider = quadtree.Collider(page.bbox)
  for obj in page.lines:
    collider.add(obj_to_bbox(obj))

  buffer = FormatBuffer()

  for char, obj in textmap.tuples:
    if char == "\n":
      yield buffer.flush() + "\n"
      continue
    has_u, has_s = detect_underline_and_strikethrough(collider, obj)
    buffer.push(char, has_u, has_s)

  yield buffer.flush()

def to_markdown_stream(pdf: pdfplumber.pdf):
  for page in pdf.pages:
    for line in page_to_markdown(page):
      yield line

def file_to_markdown(file):
  with pdfplumber.open(file) as pdf:
    return "".join(to_markdown_stream(pdf))
