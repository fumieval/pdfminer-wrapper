import math

def interleave_32(n):
  n = (n | (n << 8)) & 0x00ff00ff
  n = (n | (n << 4)) & 0x0f0f0f0f
  n = (n | (n << 2)) & 0x33333333
  return (n | (n << 1)) & 0x55555555

class MortonIndex:
  def __init__(self, value, level=0):
    self.value = value
    self.level = level

  def __repr__(self):
    return f"MortonIndex({self.value}, {self.level})"

  def to_index(self):
    return self.value + (4 ** self.level - 1) // 3

  @staticmethod
  def from_xy(level: int, x: int, y: int):
    return MortonIndex(interleave_32(x) | (interleave_32(y) << 1), level)
  
  def to_xy(self):
    x = 0
    y = 0
    index = self.value
    for i in range(16):
      x |= (index & 1) << i
      index >>= 1
      y |= (index & 1) << i
      index >>= 1
    return x, y
  
  @staticmethod
  def from_bbox(level: int, bbox):
    return MortonIndex.from_xy(level, bbox.x0, bbox.y0) & MortonIndex.from_xy(level, bbox.x1, bbox.y1)

  def __and__(self, other):
    xor = self.value ^ other.value

    for i in range(self.level - 1, -1, -1):
      if (xor >> 2 * i) & 3 != 0:
        return MortonIndex(self.value >> 2 * (i + 1), self.level - i - 1)
    
    return self

  def children(self, level):
    stack = [self]
    while stack:
      index = stack.pop()
      yield index
      if index.level == level:
        continue
      else:
        for i in range(4):
          stack.append(MortonIndex(index.value << 2 | i, index.level + 1))

class BoundingBox:
  def __init__(self, x0, y0, x1, y1):
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1
  def __repr__(self):
    return f"BoundingBox({self.x0}, {self.y0}, {self.x1}, {self.y1})"

class Collider:
  def transform(self, bbox):
    x0 = math.floor((bbox[0] - self.bbox[0]) * self.scaleX)
    y0 = math.floor((bbox[1] - self.bbox[1]) * self.scaleY)
    x1 = math.floor((bbox[2] - self.bbox[0]) * self.scaleX)
    y1 = math.floor((bbox[3] - self.bbox[1]) * self.scaleY)
    return BoundingBox(x0, y0, x1, y1)

  def __init__(self, bbox, depth=4):
    self.bbox = bbox
    self.depth = depth
    size = 2 ** depth
    self.scaleX = size / (bbox[2] - bbox[0])
    self.scaleY = size / (bbox[3] - bbox[1])

    self.objects = [None] * ((4 ** (1 + depth) - 1) // 3)

  def add(self, bbox):
    index = MortonIndex.from_bbox(self.depth, self.transform(bbox))
    idx = index.to_index()
    if self.objects[idx] is None:
      self.objects[idx] = [bbox]
    else:
      self.objects[idx].append(bbox)

  def find(self, bbox):
    index = MortonIndex.from_bbox(self.depth, self.transform(bbox))
    for parent in index.children(self.depth):
      idx = parent.to_index()
      if self.objects[idx] is not None:
        for other in self.objects[idx]:
          if intersects(bbox, other):
            yield other

def intersects(a, b):
  return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]
