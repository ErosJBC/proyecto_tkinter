from tkinter import *
import pandas as pd

class File:
    df_file = None
    file_name = None
    sheet_name = None

    def __init__(self, file_name, sheet_name=None):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.df_file = self.read_file(self.file_name, self.sheet_name)

    def get_df_file(self):
        return self.df_file

    def set_df_file(self, df):
        self.df_file = df

    def add_new_row(self, row):
        df_new = pd.DataFrame(row, columns=self.df_file.columns.values.tolist())
        self.df_file = self.df_file.append(df_new, ignore_index=True)

    def read_file(self, file, name_sheet):
        df = pd.read_excel(file, sheet_name=name_sheet)
        return df

    def write_file(self):
        self.df_file.to_excel(self.file_name, sheet_name=self.sheet_name, index=False)

class Bonus:
    goal_per_day = 1610.0
    total_kg_packing = None
    total_boxes = None
    capacity_boxes = None
    type_packing = None
    type_caliber = None
    list_total_kg = None
    list_percentage_by_caliber = None
    list_rate_caliber = None
    list_bonus_caliber = None
    bonus_total = None

    def __init__(self, type_packing, caliber, total_boxes, capacity_boxes):
        self.type_packing = type_packing
        self.type_caliber = caliber
        self.total_boxes = total_boxes
        self.capacity_boxes = capacity_boxes
        self.calculate_total_kg_packing()
        self.calculate_percentage_by_caliber()
        self.calculate_rate_caliber()
        self.calculate_bonus()

    def get_bonus_total(self):
        return self.bonus_total

    def get_type_packing(self):
        return self.type_packing

    def get_type_caliber(self):
        return ','.join([str(caliber) for caliber in self.type_caliber])

    def get_total_boxes(self):
        return self.total_boxes

    def get_capacity_boxes(self):
        return self.capacity_boxes

    def get_total_kg(self):
        return sum(self.list_total_kg)

    def get_percentage_by_caliber(self):
        return self.list_percentage_by_caliber

    def get_rate_caliber(self):
        return self.list_rate_caliber

    def get_bonus_caliber(self):
        return self.list_bonus_caliber

    def calculate_total_kg_packing(self):
        self.list_total_kg = []
        for index in range(0, len(self.type_caliber)):
            self.list_total_kg.append(self.total_boxes[index] * self.capacity_boxes[index])

    def calculate_percentage_by_caliber(self):
        self.total_kg_packing = sum(self.list_total_kg)
        self.list_percentage_by_caliber = []
        for index in range(0, len(self.list_total_kg)):
            self.list_percentage_by_caliber.append(round(self.list_total_kg[index]/self.total_kg_packing, 2))

    def calculate_rate_caliber(self):
        pack = Packing()
        df_pack = pack.generate_list_packing()
        df_pack = df_pack[df_pack['VARIEDAD'].str.contains(self.type_packing) & df_pack['CALIBRE'].isin(self.type_caliber)]
        self.list_rate_caliber = []
        for caliber in self.type_caliber:
            self.list_rate_caliber.append(float(df_pack[df_pack['CALIBRE'] == caliber]['BONIFICACION']))

    def calculate_bonus(self):
        excess_kilograms = self.total_kg_packing - self.goal_per_day
        self.list_bonus_caliber = []
        for index in range(0, len(self.type_caliber)):
            self.list_bonus_caliber.append(round(self.list_percentage_by_caliber[index] * excess_kilograms * self.list_rate_caliber[index], 2))
        self.bonus_total = round(sum(self.list_bonus_caliber), 2)

class Employee:
    id_employee = None
    name_employee = None
    last_name_employee = None

    def __init__(self, id, name, last_name):
        self.id_employee = id
        self.name_employee = name
        self.last_name_employee = last_name

    def get_id_employee(self):
        return self.id_employee

    def get_name_employee(self):
        return self.name_employee

    def get_last_name_employee(self):
        return self.last_name_employee

class Packing:
    df_packing = None
    type_packing = None
    size_packing = None

    def __init__(self):
        self.df_packing = self.generate_list_packing()
        self.type_packing = list(self.df_packing['VARIEDAD'].unique())

    def get_df_packing(self):
        return self.df_packing

    def get_type_packing(self):
        return self.type_packing

    def generate_list_packing(self):
        file_caliber = File('databases/Calibre.xlsx', 'calibre')
        result_df = file_caliber.get_df_file()
        return result_df

class RegisterEmployee:
    def __init__(self, employee, bonus):
        self.DNI = employee.get_id_employee()
        self.last_name = employee.get_last_name_employee()
        self.name = employee.get_name_employee()
        self.working_hours = 8.00
        self.effective_hours = 5.03
        self.kg_packing = bonus.get_total_kg()
        self.type_packing = bonus.get_type_packing()
        self.type_caliber = bonus.get_type_caliber()
        self.bonus_total = bonus.get_bonus_total()

    def save_register_employee(self):
        file_bonus_employee = File('databases/BonificacionEmpleados.xlsx', 'Bonificacion')
        list_employee = [(self.DNI, self.last_name, self.name, self.working_hours, self.effective_hours,
                          self.kg_packing, self.type_packing, self.type_caliber, self.bonus_total)]

        file_bonus_employee.add_new_row(list_employee)
        file_bonus_employee.write_file()

class ListEmployee:
    df_employees = None

    def __init__(self):
        self.df_employees = self.generate_list_employees()

    def get_df_employess(self):
        return self.df_employees

    def generate_list_employees(self):
        df_employees = File('databases/BonificacionEmpleados.xlsx', 'Bonificacion')
        result_df = df_employees.get_df_file()
        return result_df

class StatisticsEmployee:

    df_statistics = None

    def __init__(self):
        self.df_statistics = File('databases/BonificacionEmpleados.xlsx', 'Bonificacion').get_df_file()

    def generate_statistics_employees(self):
        df_employees = self.df_statistics.filter(['Apellidos', 'Nombres', 'Kilogramos Empacados'])
        list_employees = list(df_employees['Apellidos'] + " " + df_employees['Nombres'])
        list_kg_packing = list(df_employees['Kilogramos Empacados'])

        return list_employees, list_kg_packing

    def generate_statistics_type_caliber(self, type_packing):
        df_employees = self.df_statistics.filter(['Variedad', 'Calibre'])
        df_caliber = df_employees[df_employees['Variedad'] == type_packing]
        dict_caliber = {}
        for index, row in df_caliber.iterrows():
            for r in row['Calibre'].split(','):
                key = str(r.strip())
                if key not in dict_caliber: dict_caliber[key] = 1
                else: dict_caliber[key] += 1
        list_type_caliber = list(dict_caliber.keys())
        list_quantity_caliber = list(dict_caliber.values())

        return list_type_caliber, list_quantity_caliber

class Dashboard:
    pass