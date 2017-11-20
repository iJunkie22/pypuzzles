# coding: utf-8
from __future__ import print_function
import random
import cStringIO
import datetime
import ui

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

    def hide_slot(self, row_n, col_n, replacement='<input type="text" size="1" pattern="[0-9]*"></input>'):
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
      input {
			max-width: 1em;
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


class SudokuPuzzle(object):
    def __init__(self):
        self.paper_grid = PaperGrid()
        self.grid = self.paper_grid.filler_content(None)

    def get_row(self, row_n):
        return [self.grid[col_n][row_n] for col_n in xrange(9)]

    def get_col(self, col_n):
        return [self.grid[col_n][row_n] for row_n in xrange(9)]

    @staticmethod
    def extract_set(col_or_row):
        return set([i for i in col_or_row if i])

    @staticmethod
    def set_complement(extracted_set):
        return set(xrange(1, 10)) - extracted_set

    @staticmethod
    def pick_from_set(valid_set):
        return random.choice(list(valid_set))

    @staticmethod
    def get_subgrid_coords(row_n, col_n):
        grid_x = (col_n // 3) * 3
        grid_y = (row_n // 3) * 3
        return [(x, y) for x in xrange(grid_x, grid_x + 3) for y in xrange(grid_y, grid_y + 3)]

    def get_subgrid(self, row_n, col_n):
        return [self.grid[x][y] for (x, y) in self.get_subgrid_coords(row_n, col_n)]

    def get_valid_set(self, row_n, col_n):
        sl1 = self.get_row(row_n)
        sl2 = self.get_col(col_n)
        sl3 = self.get_subgrid(row_n, col_n)
        slots = sl1 + sl2 + sl3

        #if row_n == col_n:
        #    slots += [self.grid[x3][x3] for x3 in xrange(0, 9)]

        #if row_n == 8 - col_n:
        #    slots += [self.grid[8 - x3][x3] for x3 in xrange(0, 9)]

        slots_set = self.extract_set(slots)
        if len(slots_set) == 9:
            pass
        return self.set_complement(slots_set)

    def fill_slot(self, row_n, col_n):
        choices = list(self.get_valid_set(row_n, col_n))
        self.grid[col_n][row_n] = random.choice(choices)

    def fill_grid(self):
        slot_coords = [(y1, x1) for x1 in xrange(0, 9) for y1 in xrange(0, 9)]
        testing = False
        tries = 0
        if testing:
            diag1 = [(x3, x3) for x3 in xrange(0, 9)]
            diag2 = [(8 - x3, x3) for x3 in xrange(0, 9)]
            diags = diag1 + diag2
            trash = []
            trash_indexes = []
            for diagcoor in diags:
                trash.append(slot_coords[(diagcoor[0] * 9) + diagcoor[1]])
            for trash_item in trash:
                for i, slot_coord in enumerate(slot_coords):
                    if slot_coord[0] == trash_item[0] and slot_coord[1] == trash_item[1]:
                        trash_indexes.append(i)

            trash_indexes = sorted(trash_indexes, reverse=True)
            for i2 in trash_indexes:
                del slot_coords[i2]

            slot_coords = slot_coords + diags
        success = False

        while success == False:
            tries += 1
            try:
                for y2, x2 in slot_coords:
                    self.fill_slot(y2, x2)
                #assert len(list(set([self.grid[x3][x3] for x3 in xrange(0, 9)]))) == 9
                #assert len(list(set([self.grid[8 - x3][x3] for x3 in xrange(0, 9)]))) == 9
                success = True
            except IndexError:
                self.grid = self.paper_grid.filler_content(None)
                success = False
            except AssertionError:
                self.grid = self.paper_grid.filler_content(None)
                success = False
        print("took", tries, "tries")

    def push_content(self):
        self.paper_grid._content = self.grid

    def hide_random_slot(self):
        x = random.choice(xrange(0, 9))
        y = random.choice(xrange(0, 9))
        self.paper_grid.hide_slot(y, x)

    def hide_n_slots(self, slot_count):
        for s_i in xrange(0, slot_count):
            self.hide_random_slot()


def to_file(puz):
	with open(datetime.datetime.now().isoformat() + '.html', 'w') as fd1:
		fd1.write(puz.paper_grid.html_out())
		
def to_webview(puz):
	wv = ui.WebView()
	wv.load_html(puz.paper_grid.html_out())
	wv.present()
	
def to_textview(puz):
	tv = ui.TextView()
	tv.text = puz.paper_grid.html_out()
	tv.present()
	
sp1 = SudokuPuzzle()
sp1.fill_grid()
sp1.push_content()
sp1.paper_grid.print_grid()
sp1_html = sp1.paper_grid.html_out()
# print(sp1_html)
sp1.hide_n_slots(40)

to_textview(sp1)
