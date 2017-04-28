import xlwt3 as xlwt
from datetime import datetime

# w = xlwt.Workbook()
# ws = w.add_sheet('xlwt was here')
# w.save('/Users/hayden/Desktop/另一个影赛/mini.xls')


# style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
# style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, 'A')
ws.write(1, 0, 'B')
ws.write(0, 1, 'C')
ws.write(1, 1, 'D')

wb.save('/Users/hayden/Desktop/另一个影赛/example.xls')