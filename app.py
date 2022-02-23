import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from class_system import *

class Application(Frame):
    btnRegisterEmployee = None
    btnListEmployees = None
    btnStatisticsEmployee = None
    btnDashboard = None
    btnQuit = None

    def __init__(self, master=None):
        super().__init__(master, width=840, height=400)
        self.master = master
        self.pack()
        self.create_nav_frame()
        self.create_main_frame()

    def onClickDashboard(self):
        self.frame_dashboard()

    def onClickRegisterEmployee(self):
        self.frame_register_employee()
        self.btnSaveEmployee.config(command=self.onClickSaveEmployee)
        self.btnCancelEmployee.config(command=self.onClickDashboard)

    def onClickSaveEmployee(self):
        id_employee = self.txtDNIEmployee.get()
        last_name_employee = self.txtLastNameEmployee.get()
        name_employee = self.txtNameEmployee.get()
        type_packing = self.comboOptionPacking.get()
        type_caliber = [int(caliber) if caliber.isdigit() else caliber for caliber in str(self.txtTypeCaliber.get()).split(',')]
        quantity_boxes = [int(quantity) for quantity in str(self.txtQuantityBoxes.get()).split(',')]
        capacity_boxes = [int(capacity) for capacity in str(self.txtCapacityBoxes.get()).split(',')]

        register_employee = RegisterEmployee(Employee(id_employee, name_employee, last_name_employee),
                                             Bonus(type_packing, type_caliber, quantity_boxes, capacity_boxes))

        register_employee.save_register_employee()
        self.txtDNIEmployee.delete(0, 'end')
        self.txtLastNameEmployee.delete(0, 'end')
        self.txtNameEmployee.delete(0, 'end')
        self.comboOptionPacking.delete(0, 'end')
        self.txtTypeCaliber.delete(0, 'end')
        self.txtQuantityBoxes.delete(0, 'end')
        self.txtCapacityBoxes.delete(0, 'end')
        result = messagebox.showinfo(message="Empleado registrado con éxito!", title="Confirmación de Registro")
        if result == 'ok': self.onClickListEmployees()

    def onClickListEmployees(self):
        self.frame_list_employees()
        self.list_employees = ListEmployee()
        self.result_list = self.list_employees.get_df_employess()
        for index, row in self.result_list.iterrows():
            dni = "00000000" + str(row['DNI'])
            self.tableEmployees.insert("", END, text=(index + 1), values=(dni[len(dni)-8:len(dni)], row['Apellidos'], row['Nombres'], row['Horas de Jornada'], row['Kilogramos Empacados'], row['Variedad'], row['Calibre'], row['Bono']))

    def onClickStatisticsEmployee(self):
        self.frame_statistics_employee()

    def onClickQuit(self):
        self.btnQuit = exit()
        return self.btnQuit

    def create_nav_frame(self):
        frameMain = Frame(self, bg="#BFDAFF")
        frameMain.place(x=0, y=0, width=200, height=400)

        self.btnDashboard = Button(frameMain, text="Dashboard", bg="#00365C", fg="white", command=self.onClickDashboard)
        self.btnDashboard.place(x=20, y=30, width=160, height=30)

        self.btnRegisterEmployee = Button(frameMain, text="Registrar Empleado", bg="#00365C", fg="white", command=self.onClickRegisterEmployee)
        self.btnRegisterEmployee.place(x=20, y=80, width=160, height=30)

        self.btnListEmployees = Button(frameMain, text="Listar Empleados", bg="#00365C", fg="white", command=self.onClickListEmployees)
        self.btnListEmployees.place(x=20, y=130, width=160, height=30)

        self.btnStatisticsEmployee = Button(frameMain, text="Estadísticas", bg="#00365C", fg="white", command=self.onClickStatisticsEmployee)
        self.btnStatisticsEmployee.place(x=20, y=180, width=160, height=30)

        self.btnQuit = Button(frameMain, text="Salir", bg="#00365C", fg="white", command=self.onClickQuit)
        self.btnQuit.place(x=20, y=230, width=160, height=30)

    def create_main_frame(self):
        self.framePanel = Frame(self, bg="#CCCDD4")
        self.framePanel.place(x=200, y=0, width=640, height=400)
        self.frame_dashboard()

    def frame_dashboard(self):
        frameDashboard = Frame(self.framePanel, bg="#A9AAB0")
        frameDashboard.place(x=10, y=10, width=620, height=380)

    def frame_register_employee(self):
        frameRegister = Frame(self.framePanel, bg="#A9AAB0")
        frameRegister.place(x=10, y=10, width=620, height=380)

        option_type_packing = Packing()

        labelDNIEmployee = Label(frameRegister, text="DNI del Empleado: ")
        labelDNIEmployee.place(x=20, y=20)
        self.txtDNIEmployee = Entry(frameRegister)
        self.txtDNIEmployee.place(x=160, y=18, width=250, height=25)

        labelLastNameEmployee = Label(frameRegister, text="Apellidos del Empleado: ")
        labelLastNameEmployee.place(x=20, y=60)
        self.txtLastNameEmployee = Entry(frameRegister)
        self.txtLastNameEmployee.place(x=160, y=58, width=250, height=25)

        labelNameEmployee = Label(frameRegister, text="Nombres del Empleado: ")
        labelNameEmployee.place(x=20, y=100)
        self.txtNameEmployee = Entry(frameRegister)
        self.txtNameEmployee.place(x=160, y=98, width=250, height=25)

        labelPackingEmployee = Label(frameRegister, text="Elija la variedad: ")
        labelPackingEmployee.place(x=20, y=140)
        self.comboOptionPacking = Combobox(frameRegister, values=option_type_packing.get_type_packing(), state="readonly")
        self.comboOptionPacking.place(x=160, y=138, width=250, height=25)

        labelTypeCaliber = Label(frameRegister, text="Tipos de Calibre: ")
        labelTypeCaliber.place(x=20, y=180)
        self.txtTypeCaliber = Entry(frameRegister)
        self.txtTypeCaliber.place(x=160, y=178, width=250, height=25)

        labelQuantityBoxes = Label(frameRegister, text="Cantidad de Cajas: ")
        labelQuantityBoxes.place(x=20, y=220)
        self.txtQuantityBoxes = Entry(frameRegister)
        self.txtQuantityBoxes.place(x=160, y=218, width=250, height=25)

        labelCapacityBoxes = Label(frameRegister, text="Capacidad de Cajas: ")
        labelCapacityBoxes.place(x=20, y=260)
        self.txtCapacityBoxes = Entry(frameRegister)
        self.txtCapacityBoxes.place(x=160, y=258, width=250, height=25)

        self.btnSaveEmployee = Button(frameRegister, text="Guardar", bg="#1A554F", fg="white")
        self.btnSaveEmployee.place(x=450, y=30, width=120, height=30)

        self.btnCancelEmployee = Button(frameRegister, text="Cancelar", bg="#C02739", fg="white")
        self.btnCancelEmployee.place(x=450, y=70, width=120, height=30)

    def frame_list_employees(self):
        frameList = Frame(self.framePanel, bg="#A9AAB0")
        frameList.place(x=10, y=10, width=620, height=380)

        self.tableEmployees = ttk.Treeview(frameList, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))
        self.tableEmployees.column("#0", width=20)
        self.tableEmployees.column("col1", width=50, anchor=CENTER)
        self.tableEmployees.column("col2", width=85, anchor=CENTER)
        self.tableEmployees.column("col3", width=85, anchor=CENTER)
        self.tableEmployees.column("col4", width=40, anchor=CENTER)
        self.tableEmployees.column("col5", width=50, anchor=CENTER)
        self.tableEmployees.column("col6", width=45, anchor=CENTER)
        self.tableEmployees.column("col7", width=35, anchor=CENTER)
        self.tableEmployees.column("col8", width=35, anchor=CENTER)

        self.tableEmployees.heading("#0", text="N°", anchor=CENTER)
        self.tableEmployees.heading("col1", text="DNI", anchor=CENTER)
        self.tableEmployees.heading("col2", text="Apellidos", anchor=CENTER)
        self.tableEmployees.heading("col3", text="Nombres", anchor=CENTER)
        self.tableEmployees.heading("col4", text="Hrs. Trab.", anchor=CENTER)
        self.tableEmployees.heading("col5", text="Kg. Empacados", anchor=CENTER)
        self.tableEmployees.heading("col6", text="Variedad", anchor=CENTER)
        self.tableEmployees.heading("col7", text="Calibre", anchor=CENTER)
        self.tableEmployees.heading("col8", text="Bono", anchor=CENTER)

        self.tableEmployees.place(x=10, y=10, width=600, height=360)

    def frame_statistics_employee(self):

        def function(pct, all_values):
            absolute = int(np.round(pct/100.0 * np.sum(all_values)))
            return "{:.2f}%\n({:d})".format(pct, absolute)

        frameStatistics = Frame(self.framePanel, bg="#A9AAB0")
        frameStatistics.place(x=10, y=10, width=620, height=380)

        df_statistics = StatisticsEmployee()
        employees, total_kg = df_statistics.generate_statistics_employees()
        total_kg_mean = np.mean(total_kg)
        tango_calibre, quantity_tango_caliber = df_statistics.generate_statistics_type_caliber('TANGO')
        wmurcott_calibre, quantity_wmurcott_caliber = df_statistics.generate_statistics_type_caliber('W-M URCOTT')

        fig_employees, ax_employees = plt.subplots(figsize=(6.2, 3))
        ax_employees.barh(employees, total_kg)
        labels = ax_employees.get_xticklabels()
        plt.setp(labels, rotation=45, horizontalalignment='right')
        ax_employees.set(xlabel='Total Kg', ylabel='Empleados', title='Cantidad de Kg por Empleado')
        ax_employees.axvline(total_kg_mean, ls='--', color='r')
        fig_employees.subplots_adjust(left=0.1)
        plt.tight_layout()

        fig_tango, ax_tango = plt.subplots(figsize=(6.2, 3), subplot_kw=dict(aspect='equal'))
        wedges, texts, autotexts = ax_tango.pie(quantity_tango_caliber,
                                                autopct=lambda pct: function(pct, quantity_tango_caliber),
                                                textprops=dict(color='w'),
                                                explode=tuple([0.1 for i in range(0, len(quantity_tango_caliber))]),
                                                shadow=True)
        ax_tango.legend(wedges, tango_calibre,
                        title="Tipo calibre",
                        loc='center left',
                        bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight='bold')
        ax_tango.set_title("Variedad: Tango")

        # fig_wmurcott, ax_wmurcott = plt.subplots(figsize=(6.2, 3))

        canvas_employees = FigureCanvasTkAgg(fig_employees, master=frameStatistics)
        canvas_employees.draw()
        canvas_employees.get_tk_widget().pack()

        canvas_tango_caliber = FigureCanvasTkAgg(fig_tango, master=frameStatistics)
        canvas_tango_caliber.draw()
        canvas_tango_caliber.get_tk_widget().pack()

        # canvas_wmurcott_caliber = FigureCanvasTkAgg(fig_employees, master=frameStatistics)
        # canvas_wmurcott_caliber.draw()
        # canvas_wmurcott_caliber.get_tk_widget().pack()