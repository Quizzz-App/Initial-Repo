import xlsxwriter as xls

# newWorkbook= xls.Workbook('Test.xlsx')
# newWorkSheet= newWorkbook.add_worksheet('test')

# data= [
#     ['Name', 'Age', 'Country'],
#     ['John', 25, 'USA'],
#     ['Jane', 30, 'Canada'],
#     ['Mike', 28, 'UK']]
# col= 0

# for row_num, data_row in enumerate(data):
#     for col_num, data_cell in enumerate(data_row):
#         newWorkSheet.write(row_num, col_num, data_cell)
#     col += 1

# newWorkbook.close()

import openpyxl as xls

# create a new workbook
newWorkbook = xls.Workbook()

# get the active worksheet
newWorksheet = newWorkbook.active
newWorksheet.title= 'Test'

# add data

data= [
    ['Name', 'Age', 'Country'],
    ['John', 25, 'USA'],
    ['Jane', 30, 'Canada'],
    ['Mike', 28, 'UK']]

for row_num, data_row in enumerate(data, start=1):
    newWorksheet.append(data_row)

# save the workbook

newWorkbook.save('./test/Test.xlsx')




    # newWorksheet.write(1, 0, 'Name')
