# -*- coding: utf8 -*-
import matplotlib
import tkinter as tk
import numpy as np
import ctypes
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk
#fonts
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
#add subplot for figure
fig = Figure( dpi = 75)
a = fig.add_subplot(111)
a.set_title('Signal')
a.set_xlabel('Time (s)')
a.grid(True)
a.grid(color='0.5', linestyle='--', linewidth=1)

graphics_1 = ['X3', 'X2', 'X1', 'U', 'X', 'Y', 'Z']
graphics_2 = ['X3', 'X2', 'X1', 'U', 'Z']
plots_1st = {}
plots_2nd = {}
for i in graphics_1: plots_1st[i] = [0]
for i in graphics_2: plots_2nd[i] = [0]
t = [[0]]

# math functions
def f1(e2, r): return float(e2 * 5 + 2.5 * r)

def f2(e1): return float(e1 / 188)

def f3(u, y): return float((940 * u - y) / 2)

def f4(s): return float(s)

def f5(y, z, s): return float(15 * y - 3 * z - s)

def f6(u, x1, x2): return float(470 * u - 0.5 * x1 - x2)
#principal function
def Calculate(time, step):
    #getting values
    try:
        time_float = float(time.get())
        s = float(step.get())
    except ValueError:
        ctypes.windll.user32.MessageBoxW(None, 'Time simulation or step calculation\nHas not a valid input value!', 'Warning', 0)
        return

    # init values for all signals
    first_sys = [[1.0], [0], [0], [0], [0], [0], [0]]
    regulator = [[0], [0], [0]]
    error_sys = [[0], [0], [0]]
    help_sys = [[0], [0]]
    second_sys = [[0], [0], [0], [0]]

    for i in range(int(time_float/s)):
        # first System
        error_sys[2].append(first_sys[0][i] - first_sys[6][i])
        regulator[0].append(error_sys[2][i + 1] / 12)
        regulator[1].append(regulator[1][i] + s * (error_sys[2][i + 1] + error_sys[2][i]) / 8)
        regulator[2].append((error_sys[2][i + 1] - error_sys[2][i]) / (12 * s))
        first_sys[1].append(regulator[0][i + 1] + regulator[1][i + 1] + regulator[2][i + 1])

        error_sys[1].append(first_sys[1][i + 1] - first_sys[5][i])
        kr1 = s * error_sys[1][i]
        kr2 = s * (error_sys[1][i] + kr1 / 2)
        kr3 = s * (error_sys[1][i] + kr2 / 2)
        kr4 = s * (error_sys[1][i] + kr3)
        help_sys[0].append(help_sys[0][i] + (kr1 + 2 * kr2 + 2 * kr3 + kr4) / 6)
        first_sys[2].append(f1(error_sys[1][i + 1], help_sys[0][i + 1]))
        error_sys[0].append(first_sys[2][i + 1] - 940 * first_sys[3][i])

        ku1 = s * f2(error_sys[0][i])
        ku2 = s * f2(error_sys[0][i] + ku1 / 2)
        ku3 = s * f2(error_sys[0][i] + ku2 / 2)
        ku4 = s * f2(error_sys[0][i] + ku3)
        first_sys[3].append(first_sys[3][i] + (ku1 + 2 * ku2 + 2 * ku3 + ku4) / 6)
        first_sys[4].append(940 * first_sys[3][i + 1])

        ky1 = s * f3(first_sys[3][i], first_sys[5][i])
        ky2 = s * f3((first_sys[3][i] + first_sys[3][i + 1]) / 2, first_sys[5][i] + ky1 / 2)
        ky3 = s * f3((first_sys[3][i] + first_sys[3][i + 1]) / 2, first_sys[5][i] + ky2 / 2)
        ky4 = s * f3(first_sys[3][i + 1], first_sys[5][i] + ky3)
        first_sys[5].append(first_sys[5][i] + (ky1 + 2 * ky2 + 2 * ky3 + ky4) / 6)

        kz1 = s * f4(help_sys[1][i])
        kz2 = s * f4(help_sys[1][i] + kz1 / 2)
        kz3 = s * f4(help_sys[1][i] + kz2 / 2)
        kz4 = s * f4(help_sys[1][i] + kz3)
        first_sys[6].append(first_sys[6][i] + (kz1 + 2 * kz2 + 2 * kz3 + kz4) / 6)

        ks1 = s * f5(first_sys[5][i], first_sys[6][i], help_sys[1][i])
        ks2 = s * f5((first_sys[5][i] + first_sys[5][i + 1]) / 2, (first_sys[6][i] + first_sys[6][i + 1]) / 2, help_sys[1][i] + ks1 / 2)
        ks3 = s * f5((first_sys[5][i] + first_sys[5][i + 1]) / 2, (first_sys[6][i] + first_sys[6][i + 1]) / 2, help_sys[1][i] + ks2 / 2)
        ks4 = s * f5(first_sys[5][i + 1], first_sys[6][i + 1], help_sys[1][i] + ks3)
        help_sys[1].append(help_sys[1][i] + (ks1 + 2 * ks2 + 2 * ks3 + ks4) / 6)
        first_sys[0].append(first_sys[0][i])

        # 2nd System
        second_sys[0].append(float(0.00257) - 0.0135 * second_sys[1][i] + 0.00247 * second_sys[2][i] - 0.00154 * second_sys[3][i])
        ka01 = s * f6(second_sys[0][i + 1], second_sys[1][i], second_sys[2][i])
        ka02 = s * second_sys[3][i]
        ka03 = s * f5(second_sys[1][i], second_sys[2][i], second_sys[3][i])

        ka11 = s * f6((second_sys[0][i] + second_sys[0][i + 1]) / 2, second_sys[1][i] + ka01 / 2, second_sys[2][i] + ka02 / 2)
        ka12 = s * (second_sys[3][i] + ka03 / 2)
        ka13 = s * f5(second_sys[1][i] + ka01 / 2, second_sys[2][i] + ka02 / 2, second_sys[3][i] + ka03 / 2)

        ka21 = s * f6((second_sys[0][i] + second_sys[0][i + 1]) / 2, second_sys[1][i] + ka11 / 2, second_sys[2][i] + ka12 / 2)
        ka22 = s * (second_sys[3][i] + ka13 / 2)
        ka23 = s * f5(second_sys[1][i] + ka11 / 2, second_sys[2][i] + ka12 / 2, second_sys[3][i] + ka13 / 2)

        ka31 = s * f6(second_sys[0][i + 1], second_sys[1][i] + ka21, second_sys[2][i] + ka22)
        ka32 = s * (second_sys[3][i] + ka23)
        ka33 = s * f5(second_sys[1][i] + ka21, second_sys[2][i] + ka22, second_sys[3][i] + ka23)

        second_sys[1].append(second_sys[1][i] + (ka01 + 2 * ka11 + 2 * ka21 + ka31) / 6)
        second_sys[2].append(second_sys[2][i] + (ka02 + 2 * ka12 + 2 * ka22 + ka32) / 6)
        second_sys[3].append(second_sys[3][i] + (ka03 + 2 * ka13 + 2 * ka23 + ka33) / 6)

    plots_2nd['X3'] = np.array(second_sys[3]).astype(float)
    plots_2nd['X2'] = np.array(second_sys[2]).astype(float)
    plots_2nd['X1'] = np.array(second_sys[1]).astype(float)
    plots_2nd['U'] = np.array(second_sys[0]).astype(float)
    plots_2nd['Z'] = np.array(second_sys[2]).astype(float)

    plots_1st['X3'] = np.array(first_sys[0]).astype(float)
    plots_1st['X2'] = np.array(first_sys[1]).astype(float)
    plots_1st['X1'] = np.array(first_sys[2]).astype(float)
    plots_1st['U'] = np.array(first_sys[3]).astype(float)
    plots_1st['X'] = np.array(first_sys[4]).astype(float)
    plots_1st['Y'] = np.array(first_sys[5]).astype(float)
    plots_1st['Z'] = np.array(first_sys[6]).astype(float)
    # fixing time for each list
    t[0] = np.arange(0.0, time_float, s)
    if len(t[0]) == len(plots_2nd['Z']) or len(t[0]) == len(plots_1st['Y']):
        t[0] = np.arange(0.0, time_float, s)
    elif len(t[0]) > len(plots_2nd['Z']) or len(t[0]) > len(plots_1st['Y']):
        t[0] = np.arange(0.0, time_float - s, s)
    else:
        t[0] = np.arange(0.0, time_float + s, s)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Automatic Control System Simulation")
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu_bar = tk.Menu(container)
        file_menu = tk.Menu(menu_bar, tearoff=0, bg='white')
        file_menu.add_command(label="Configure plot", command=lambda: self.config_plot(frame))
        file_menu.add_command(label="Exit", command=exit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        tk.Tk.config(self, menu=menu_bar, bg='white')

        frame = Gui(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def config_plot(self, frame):
        frame.toolbar.configure_subplots()


class Gui(tk.Frame):
    def plot_fig(self, result, label):
        a.cla()
        a.set_title("Signal " + label)
        a.set_xlabel('Time (s)')
        a.grid(True)
        a.grid(color='0.5', linestyle='--', linewidth=1)
        a.plot(t[0], result, label=label)
        a.legend()
        self.canvas.draw()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white', width=400, height=400)

        frame = tk.Frame(self, width=120, height=100, bg='white')
        frame.pack(side='top')
        label = tk.Label(frame, text='Calculation data', bg='white', font=LARGE_FONT)
        label.grid()
        label = tk.Label(frame, text='Time simulation', bg='white', font=NORM_FONT)
        label.grid(row=1, column=0)
        time = ttk.Entry(frame, width=10)
        time.grid(row=1, column=1)
        label = tk.Label(frame, text='Calculation step', bg='white', font=NORM_FONT)
        label.grid(row=2, column=0)
        step = ttk.Entry(frame, width=10)
        step.grid(row=2, column=1)

        button = ttk.Button(frame, text='Compute', command=lambda: Calculate(time, step))
        button.grid()

        frame = tk.Frame(self, bg='white', width=120, height=100)
        frame.pack(side='top')
        label = tk.Label(frame, text='Subordinate regulation system', bg='white', font=LARGE_FONT)
        label.pack(side='top')
        for key in plots_1st:
            button = ttk.Button(frame, text=key, command=lambda key=key: self.plot_fig(plots_1st[key], key))
            button.pack(side='left')

        frame = tk.Frame(self, bg='white', width=120, height=100)
        frame.pack(side='top')
        label = tk.Label(frame, text='Modal control system', bg='white', font=LARGE_FONT)
        label.pack(side='top')
        for key in plots_2nd:
            button = ttk.Button(frame, text=key, command=lambda key=key: self.plot_fig(plots_2nd[key], key))
            button.pack(side='left')

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

app = Application()
app.geometry("800x600")
app.mainloop()