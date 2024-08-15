# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['APITestCase::test_example 1'] = '''Example                                     file:///Users/fumieval/herp/middleware/pdfminer-wrapper/te...


      Bold Text Italic Text <u>Underlined</u> <u>Text</u> ~~Strikethrough~~ ~~Text~~ <u>Underlined</u>


      Heading      1


      Heading  2


      Heading 3

      Paragraph 1

      Paragraph 2

      Paragraph 3

        • Unordered List Item 1
        • Unordered List Item 2

        • Unordered List Item 3

        1. Ordered List Item 1
        2. Ordered List Item 2
        3. Ordered List Item 3

      Table Header 1 Table Header 2 Table Header 3

      Table Data 1 Table Data 2 Table Data 3
      Table Data 4 Table Data 5 Table Data 6



      <u>Link</u>

           Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec nunc nec libero
           ultricies ultricies. Nullam nec nunc nec libero ultricies ultricies. Nullam nec nunc


      #include int main() { printf("Hello, World!\\n"); return 0; }

          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec nunc nec libero ultricies
          ultricies. Nullam nec nunc nec libero ultricies ultricies. Nullam nec nunc














1 / 1                                                                   2024/08/14, 20:24'''

snapshots['APITestCase::test_small 1'] = '''small                                       file:///Users/fumieval/herp/middleware/pdfminer-wrapper/te...


      <u>Underline</u>
      ~~Strikethrough~~

      ~~<u>Underline</u>~~ ~~<u>and</u>~~ ~~<u>Strikethrou</u>g<u>h</u>~~
      <u>Strikethrou</u>g<u>h</u> ~~<u>in</u>~~ <u>Underline</u>
      ~~Underline~~ ~~<u>in</u>~~ ~~Strikethrough~~
      ~~<u>Underline&Strikethrou</u>g<u>h</u>~~ <u>then</u> <u>underline</u>
      ~~<u>Strikethrou</u>g<u>h&Underline</u>~~ ~~then~~ ~~strikethrough~~
      <u>Underline</u> ~~<u>then</u>~~ ~~<u>Strikethrou</u>g<u>h&Underline</u>~~
      ~~Strikethrough~~ ~~<u>then</u>~~ ~~<u>Underline&Strikethrou</u>g<u>h</u>~~















































1 / 1                                                                    2024/08/15, 0:54'''
