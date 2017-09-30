import csv
import gspread
import os
import string

from oauth2client.service_account import ServiceAccountCredentials

# set the path to open the csv to upload
dir_path = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(dir_path, 'data')

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(dir_path, 'client_secret.json'), scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("whiskey_biz").sheet1

# clear the sheet
sheet.clear()

file_path = os.path.join(data_dir, 'whiskey_business.csv')

# load data into a list of lists
csv_cells = []
with open(file_path, 'r') as f:
    for line in f:
        csv_cells.append(list(line.split(',')))

# select the range of cells to update in the sheet
n_rows = len(csv_cells)
n_cols = len(csv_cells[0])
column = string.ascii_uppercase[n_cols - 1]
ws_range = "A1:{}{}".format(column, n_rows)

# get the cells to update
cell_list = sheet.range(ws_range)
for cell in cell_list:
    val = csv_cells[cell.row - 1][cell.col - 1].strip()
    cell.value = val

# bulk update the cells
sheet.update_cells(cell_list)
