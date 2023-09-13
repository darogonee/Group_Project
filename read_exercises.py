from openpyxl import load_workbook
import json

workbook = load_workbook(filename="exercises.xlsx")
sheet = workbook.active
exercise_dict = {}
for value in sheet.iter_rows(min_row=1,min_col=2, max_col=272, max_row=1,values_only=True):
    print(value)



muscle_group = sheet["B"]
exercise = sheet["C"]
level = sheet["D"]
ulc = sheet["E"]
pp = sheet["F"]
modality = sheet["G"]
joint = sheet["H"]
equipment = sheet["I"]



# {exercise_id: {"muscle_group":muscle_group, "exercise":exercise, "level"}}

