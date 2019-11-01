#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Text
from tkinter import filedialog as fd
from tkinter import messagebox as msg

import os
import math
import copy
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



import stats_team3 as st
import data_load as load
import file_upload as upload
from ac_classes import IndivModel as imodel
from ac_classes import DataModel as dmodel
from nonlinear_regression import NonLinearRegression as nlr
from anova import main as anova_main

# Create instance
win = tk.Tk()   

# Add a title       
win.title("AnalyticsCal")

global csvList,x, y,X,Y,data
global csvHeader
global file_name

#-------------------------------------------------------------------------Plots

def reg_plot(x_plot,y_plot,y_predicted, equation_str, title, x_label, y_label, color = None):
    plt.clf()
    raw_plot = plt.scatter(x_plot, y_plot, color = 'b')
    predict_plot, = plt.plot(x_plot,y_predicted , '-',color = color)
    plt.title(title)					
    plt.xlabel(x_label)					
    plt.ylabel(y_label)
    plt.legend((raw_plot, predict_plot),('Raw Data', 'Prediction equation = ' + equation_str),loc=(-0.05,-0.20), scatterpoints=1, ncol=3, fontsize=8)
    plt.tight_layout()
    plt.show()
    
    
#--------------------------------------------------------------------------
csvList = []
#--------------------------------------------------------------------------
# Menu
# Open file

def open_file():
    global csvList
    global file_name
    global csvHeader
    file = fd.askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')]) # gets the filename as string
    if file:
        file_name = file.name
    print(file_name)
    csvHeader, csvList = upload.preprocess_csv(file_name)
    create_data_list() # creates a separate 
    """
    database function has to be called here instead of the one in line 66
    """
    #csvList = load.load_csv_file(file_name)

# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit() 
    
# Creating a Menu Bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

# Add menu items
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command = open_file)
#file_menu.add_separator()
file_menu.add_command(label="Recent Files")
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add another Menu to the Menu Bar and an item
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
basic_statistics = []

tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='Normal Analysis')      # Add the tab
tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='Time Series Analysis')      # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make visible

# LabelFrame using tab1 as the parent - for basic data Analysis
mighty = ttk.LabelFrame(tab1, text=' Basic Data Analysis')
mighty.grid(column=0, row=0, padx=8, pady=4)

# LabelFrame using tab1 as the parent - for output console
mighty1 = ttk.LabelFrame(tab1, text=' Output Console')
mighty1.grid(column=1, row=0,sticky=tk.N+tk.S, padx=8, pady=4, columnspan=3, rowspan = 6)

mighty2 = ttk.LabelFrame(tab1, text=' Non Linear Regression ')
mighty2.grid(column = 0, row=1, padx=2, pady=1)
#mighty2.grid_columnconfigure(0, weight=1)

# Add big textbox
text_h= 12
text_w = 30
textBox = tk.Text(mighty1, height = text_h, width = text_w,wrap=tk.WORD)
textBox.grid(column=0, row=5, sticky=tk.N+tk.S)

def create_data_list():
    global x,y,X,Y, data
    if csvList != []:
        x = [float(i) for i in csvList[0]]
        y = [float(i) for i in csvList[1]]
        # Create classes
        X = imodel(x)
        Y = imodel(y)
        data = dmodel(X, Y)
        create_instance()
    else:
        print('No Data :(')

# to create instance immediately after fetching data
def create_instance():
    global X, Y, data

    X.mean()
    Y.mean()
    X.var()
    Y.var()
    data.corr_coeff()
    data.nlr_coef()
    data.anova()
    


# Modified Button statistics Function
def click_stats(textBox):
    global X,Y, data
    textBox.delete(1.0, tk.END) # clear anything previously present
    textBox.insert(tk.INSERT, 'x_bar ='+ str(X.mean)+'\n')
    textBox.insert(tk.INSERT, 'x_var ='+ str(round(X.var,4))+'\n')
    textBox.insert(tk.INSERT, 'x_standard_dev ='+ str(round(math.sqrt(X.var), 4))+'\n')
    textBox.insert(tk.INSERT, 'y_bar ='+ str(Y.mean)+'\n')
    textBox.insert(tk.INSERT, 'y_var ='+ str(round(Y.var, 4))+'\n')
    textBox.insert(tk.INSERT, 'y_standard_dev ='+ str(round(math.sqrt(Y.var),4))+'\n')
    #textBox.insert(tk.INSERT, 'Cov(x, y) ='+ str(data.cov())+'\n')
    textBox.insert(tk.INSERT, 'Correlation coeeficient ='+ str(round(data.corr_coeff, 4))+'\n')
    if data.corr_coeff < data.threshold:
        _stats_msgBox()


# stats_msgBox: Alert the user when corr_coeff < threshold
def _stats_msgBox():
    answer = msg.askyesno('AnalyticsCal Alert'," It appears that the data is not linear. \n Do you wish to take log transforms?")
    if answer == True:
        print("Yes take Log")
        log_plot()
    else:
        print("No don't!")
        

def log_plot():
    global X, Y, data
    X_log = [math.log(i) for i in X.values]
    Y_log = [math.log(i) for i in Y.values]
    print(X_log)
    print(Y_log)
    fig, (ax1, ax2) = plt.subplots(2)
    #fig.suptitle('Raw plot vs Log plots')
    ax1.scatter(X_log, Y_log,color = 'r')
    ax1.set_title('Scatter plot of log_y & log_x')					
    ax1.set(xlabel='Log(X)', ylabel='Log(Y)')
    ax2.scatter(X.values, Y.values)
    #plt.scatter(X_log, Y_log,)
    ax2.set_title('Scatter plot of Y & X')
    ax2.set(xlabel='X', ylabel='Y')
    #plt.xlabel('x')					
    #plt.ylabel('y')
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.show()
    """
    fig = Figure(figsize=(12, 8), facecolor = 'white')
    axis1 = fig.add_subplot(211)
    axis2 = fig.add_subplot(212)
    axis1.plot(X_log,Y_log)
    axis1.set_xlabel('log(X)')
    axis1.set_ylabel('log(Y)')
    axis1.grid(linestyle='-.')
    axis2.plot(X.values,Y.values)
    axis2.set_xlabel('X')
    axis2.set_ylabel('Y')
    axis2.grid(linestyle='-.')
    
    global root
    root = tk.Tk()  
    root.withdraw() 
    root.protocol('WM_DELETE_WINDOW', _destroyWindow)    
#-------------------------------------------------------------- 
    canvas = FigureCanvasTkAgg(fig, master=root) 
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1) 
#-------------------------------------------------------------- 
    root.update() 
    root.deiconify() 
    root.mainloop() 

def _destroyWindow():
    global root
    root.quit() 
    root.destroy()  

"""
mighty_width = 26
# Add button to output basic statistics
Statistics = ttk.Button(mighty, text="Statistics", command= lambda : click_stats(textBox), width = mighty_width)   
Statistics.grid(column=0, row=0, sticky='W')
#----------------------------------------------------------------------Basic Plot
# Modified Button Click Plot
def click_plot():
    global X, Y
    plt.scatter(X.values, Y.values,alpha=1)					
    plt.title('Scatter plot of x and y')					
    plt.xlabel('x')					
    plt.ylabel('y')
    plt.tight_layout()
    plt.show()
# Add button for plot
plot = ttk.Button(mighty, text="Plot", command=click_plot, width = mighty_width)   
plot.grid(column=0, row=1, sticky='W')
#----------------------------------------------------------------------Linear Regression
def click_linear_regression():
    global X,Y, data
    regression = nlr(X.values,Y.values)
    coefficient = regression.polynomial(1)
    coeff_list =copy.deepcopy(coefficient)
    Y_predicted = form_eqn(copy.deepcopy(coefficient))
    coefficient_str = ''
    n = len(coefficient)
    for i in range(len(coefficient)):
        if(coefficient[n - i -1] > 0):
            coefficient_str += '+'
            
        coefficient_str += str(round(coefficient[n - i - 1], 4))
        if(i == (n - 2)):
            coefficient_str += 'x '
        elif(i != (n - 1)):
            coefficient_str += 'x'+ str(n - i - 1).translate(SUP) +' '

        else:
            coefficient_str += str(n - i - 1)
    equation_str = str(coefficient_str)
    if(equation_str[0] == '+'):
        temp = list(equation_str)
        del(temp[0])
        equation_str = "".join(temp)
    data.poly_coeff = []
    data.poly_coeff = [round(coefficient[n - i - 1], 4) for i in range(n)]
        
    textBox.delete(1.0, tk.END)
    textBox.insert(tk.INSERT, equation_str)
    title= "predicted vs actual"					
    x_label= 'X'					
    y_label= 'Y'
    reg_plot(X.values, Y.values, Y_predicted, equation_str, title, x_label, y_label, 'g')
    plt.show()

# Add button to Regression
linear_Regression = ttk.Button(mighty, text="Linear Regression", command=click_linear_regression,width = mighty_width)   
linear_Regression.grid(column=0, row=2, sticky='W')

#-----------------------------------------------------------------------Non Linear Regerssion

##Polynomail Regression

# Poly_reg:Modified Button Click Function
def click_nlr_poly():
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # For printing subscript
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    global X,Y, data
    regression = nlr(X.values,Y.values)
    coefficient = regression.polynomial(int(number_chosen_poly.get()))
    coeff_list =copy.deepcopy(coefficient)
    Y_predicted = form_eqn(copy.deepcopy(coefficient))
    coefficient_str = ''
    n = len(coefficient)
    for i in range(len(coefficient)):
        if(coefficient[n - i -1] > 0):
            coefficient_str += '+'
            
        coefficient_str += str(round(coefficient[n - i - 1], 4))
        if(i == (n - 2)):
            coefficient_str += 'x '
        elif(i != (n - 1)):
            coefficient_str += 'x'+ str(n - i - 1).translate(SUP) +' '

        else:
            coefficient_str += str(n - i - 1)
    equation_str = str(coefficient_str)
    if(equation_str[0] == '+'):
        temp = list(equation_str)
        del(temp[0])
        equation_str = "".join(temp)
    data.poly_coeff = []
    data.poly_coeff = [round(coefficient[n - i - 1], 4) for i in range(n)]
        
    textBox.delete(1.0, tk.END)
    textBox.insert(tk.INSERT, equation_str)
    #raw_plot = plt.scatter(X.values, Y.values, color = 'r')
    #plt.plot(X.values, round (coeff_list[0] + (coeff_list[1]*X.values) + (coeff_list[2]*(X.values**2))+ (coeff_list[3]*(X.values**3)), 4),'-')
    #predict_plot = plt.plot(X.values, Y_predicted, '-')
    title= "predicted vs actual"					
    x_label= 'X'					
    y_label= 'Y'
    #plt.legend((raw_plot, predict_plot),('Raw Data', 'Predicted'),scatterpoints=1, ncol=3, fontsize=8)
    #plt.legend([red_dot, (red_dot, white_cross)], ["Attr A", "Attr A+B"])
    reg_plot(X.values, Y.values, Y_predicted, equation_str, title, x_label, y_label, 'r')
    plt.show()
    
# Add button for nonlinear_regression
polynomial_regression = ttk.Button(mighty2, text="Polynomial Regression", command=click_nlr_poly)   
polynomial_regression.grid(column=0, row=0, sticky='W')

# Order for polynomial_reg
number_poly = tk.IntVar()
number_chosen_poly = ttk.Combobox(mighty2, width=3, textvariable=number_poly, state='readonly')
number_chosen_poly['values'] = (1, 2, 3, 4)
number_chosen_poly.grid(column=1, row=0)
number_chosen_poly.current(0)

# Eqn for poly regression
def form_eqn(coeff_list):
    global X
    n = len(coeff_list)
    len_diff = 4 - n
    for _ in range(len_diff):
        coeff_list.append(0)
    print("coeff_list aft:",coeff_list)
    eqn = [round (coeff_list[0] + (coeff_list[1]*x) + (coeff_list[2]*(x**2))+ (coeff_list[3]*(x**3)), 4) for x in X.values]
    print(eqn)
    return eqn
## Sinusoidal Regression

def click_nlr_sin():
    global X,Y, data
    regression = nlr(X.values,Y.values)
    #print(int(number_chosen_sin.get()))
    #coefficient = regression.sinusoidal(int(number_chosen_sin.get()))
    coefficient = regression.sinusoidal(4)
    textBox.delete(1.0, tk.END)
    textBox.insert(tk.INSERT, str(coefficient))

sinusoidal_regression = ttk.Button(mighty2, text="Sinusoidal Regression", command=click_nlr_sin,width = 20)   
sinusoidal_regression.grid(column=0, row=1, sticky='W')
"""
# Order for sinusoidal_reg
number_sin = tk.StringVar()
number_chosen_sin = ttk.Combobox(mighty2, width=3, textvariable=number_sin, state='readonly')
number_chosen_sin['values'] = (1, 2, 3, 4)
number_chosen_sin.grid(column=1, row=1)
number_chosen_sin.current(0)
"""
## Exponential Regression
def click_nlr_exp():
    global X,Y, data
    regression = nlr(X.values,Y.values)
    #print('regression = ',regression)
    coefficient = regression.exponential(2)
    if(math.isnan(coefficient[0])):
        coefficient_str = "The exponential model is not a right fit for this data"
        print(coefficient_str)
        #print('coeff = ', coefficient)
    else:
        coefficient_str = [str(i) for i in coefficient ]
    #print(coefficient_str)
    textBox.delete(1.0, tk.END)
    textBox.insert(tk.INSERT, coefficient_str)

exponential_regression = ttk.Button(mighty2, text="Exponential Regression", command=click_nlr_exp)   
exponential_regression.grid(column=0, row=2, sticky='W')


""" To be implemented
# Order for exponential_reg
number_exp = tk.IntVar()
number_chosen_exp = ttk.Combobox(mighty2, width=3, textvariable=number_exp, state='readonly')
number_chosen_exp['values'] = (1, 2)
number_chosen_exp.grid(column=1, row=2)
number_chosen_exp.current(0)
"""
#--------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------ANOVA

def click_anova():
    global X,Y,data
    anova_dict = anova_main(X.values, Y.values,data.poly_coeff)
    data.msr = anova_dict['msr']
    data.mse = anova_dict['mse']
    data.ssr = anova_dict['ssr']
    data.sse = anova_dict['sse']
    data.f = anova_dict['f']
    data.p = anova_dict['p']
    textBox.delete(1.0, tk.END)
    textBox.insert(tk.INSERT, 'ANOVA'+ '\n')
    textBox.insert(tk.INSERT, 'msr = '+ str(round(data.msr, 4)) + '\n')
    textBox.insert(tk.INSERT, 'mse = '+ str(round(data.mse, 4))+ '\n')
    textBox.insert(tk.INSERT, 'ssr = '+ str(round(data.ssr, 4)) + '\n')
    textBox.insert(tk.INSERT, 'sse = '+ str(round(data.sse,4)) + '\n')
    textBox.insert(tk.INSERT, 'p = '+ str(round(data.p,4)) + '\n')
    textBox.insert(tk.INSERT, 'f = '+ str(round(data.f, 4))  + '\n')

# Add button for ANOVA
anova = ttk.Button(mighty, text="ANOVA", command=click_anova,width = mighty_width)   
anova.grid(column=0, row=4, sticky='W')

#name_entered.focus()      # Place cursor into name Entry
#======================
# Start GUI
#======================
win.mainloop()
