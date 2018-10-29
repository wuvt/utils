#!/bin/env python3

import csv
import sys

o = []
ELEMENTS_PER_ROW = 4

# Returns the "real length" of an array i.e. number of elements that actually
# have content. Used for differentiating between title rows and content rows
# (is that what they're called?)
def real_len(arr):
    l = 0
    for element in arr:
        if len(element) > 0:
            l += 1
    return l

# Add title row to the HTML doc
def add_title_row(row):
    o.append("<tr>")
    epr_str = str(ELEMENTS_PER_ROW)
    o.append(f"<td colspan=\"{epr_str}\"><b>{row[0]}</b>")
    o.append("</tr>")

# Add content row to the HTML doc
def add_content_row(row):
    o.append("<tr>")
    for i in range(0, ELEMENTS_PER_ROW):
        o.append(f"<td>{row[i]}</td>")
    o.append("</tr>")

# HTML to be written at the start of the doc
def init_html():
    #o.append("<style>")
    #o.append("table, th, td {")
    #o.append("  border: 1px solid black;")
    #o.append("  border-collapse: collapse;")
    #o.append("}")
    #o.append("</style>")
    o.append("<table table class=\"tracklist\" id=\"radiothon-schedule\">")

# HTML to be written at the end of the doc
def end_html():
    o.append("</table>")

init_html()

with open(sys.argv[1]) as file:
    c = csv.reader(file)
    for row in c:
        # Check the length of the current row to determine if we have a
        # title or content row. If there's only one real element in the row,
        # we know it's a title row, otherwise it's a content row.
        if real_len(row) == 1:
            add_title_row(row)
        else:
            add_content_row(row)

# HTML at the end of the doc
end_html()

out = sys.argv[1] + ".html"
with open(out, "w") as file:
    for _ in o:
        file.write(_)
