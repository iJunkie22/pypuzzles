# coding: utf-8
from __future__ import print_function
import cStringIO

__author__ = 'ethan'


class PaperGrid(object):
    c_rows = 9
    c_cols = 9
    _content = None

    @property
    def content(self):
        if self._content is None:
            return self.filler_content()
        else:
            return self._content

    @classmethod
    def filler_content(cls, filler="?"):
        return [[filler for row in xrange(cls.c_rows)] for col in xrange(cls.c_cols)]

    def print_grid(self):
        grid_str = ""
        grid_lists = self.content

        for row_n in xrange(self.c_rows):
            row_str = " ".join([str(grid_lists[col_n][row_n]) for col_n in xrange(self.c_cols)]) + "\n"
            grid_str += row_str

        print(grid_str)
        return grid_str

    def hide_slot(self, row_n, col_n, replacement=" "):
        self._content[row_n][col_n] = replacement

    def html_out(self):
        grid_lists = self.content
        html = cStringIO.StringIO()
        html.write('''<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
      td {
        font-size: 24pt;
        border: 1px solid black;
        width: 1.2em;
        height: 1.2em;
        text-align: center;
      }
      table {
        border-left: 3px solid black;
        border-top: 3px solid black;
        border-collapse: collapse;
      }
      .hard-r {
        border-right-width: 3px;
      }
      .hard-t {
        border-bottom-width: 3px;
      }
      </style>
  </head>
  <body>
    <code>
    <table>''')
        for row_n in xrange(self.c_rows):
            hard_r = False
            hard_t = False
            hard_t = (row_n + 1) % 3 == 0
            hard_t_str = 'hard-t' if hard_t else ''
            html.write('<tr>')
            for col_n in xrange(self.c_cols):
                hard_r = (col_n + 1) % 3 == 0
                hard_r_str = 'hard-r' if hard_r else ''

                classes_str = 'class="' + hard_t_str + ' ' + hard_r_str + '"'
                if not hard_r and not hard_t:
                    classes_str = ''

                html.write('<td {}>{}</td>\n'.format(classes_str, grid_lists[col_n][row_n]))

            html.write('</tr>\n')
        html.write('''</table>
    </code>
  </body>

</html>
''')
        out_str = html.getvalue()
        html.close()
        return out_str


pg1 = PaperGrid()
pg1.print_grid()
