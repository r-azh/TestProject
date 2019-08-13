import tempfile
import pyexcel as pyexcel
import xlsxwriter
__author__ = 'R.Azh'

workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

with open("input.txt") as input_fd:
    lines = input_fd.readlines()

age_and_names = {}

for line in lines:
    name, age = line.strip().split(",")

    if not age in age_and_names:
        age_and_names[age] = []

    age_and_names[age].append(name)

print(age_and_names)

for key in sorted(age_and_names):
    print("Age: {}, Names Count: {}, Names: {}".format(key, len(age_and_names[key]), ",".join(age_and_names[key])))

row = 0
col = 0

for key in sorted(age_and_names):#.keys():
    row += 1
    worksheet.write(row, col, key)

    for item in age_and_names[key]:
        worksheet.write(row, col+1, len(age_and_names[key]))
        worksheet.write(row, col+1, item)
        row += 1

for item in sorted(age_and_names):
    print(item)

cell_format = workbook.add_format({'bold': True, 'italic': True})
# worksheet.write(0, 0, 'Hello', cell_format)
# worksheet.freeze_panes(row, 0)  # Freeze the row.
worksheet.write_row(row, col, ['Age', 'Name'], cell_format)
for key in sorted(age_and_names):#.keys():
    row += 1
    worksheet.write(row, col, key)
    worksheet.write(row, col+1, ",".join(age_and_names[key]))
    print(age_and_names[key])
workbook.close()

print('################### with temp file ###############################')
excel_content = None
with tempfile.NamedTemporaryFile(delete=True) as tmp:
    print(tmp.name)
    workbook = xlsxwriter.Workbook(tmp.name)
    worksheet = workbook.add_worksheet()
    row = 0
    for key in sorted(age_and_names):
        worksheet.write(row, col, key)
        worksheet.write(row, col+1, ",".join(age_and_names[key]))
        row += 1
    workbook.close()
    excel_content = tmp.read()
print(excel_content)
# f = pyexcel.load_from_dict(age_and_names)
# d = pyexcel.Sheet(age_and_names)
# print(f)
# print(d)
#
# with open("input.xlsx", 'wb') as file:
#     file.write(d)

