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
from tabulate import tabulate   # for table
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats


import stats_team3 as st
import multilinear_regression as mlr
import data_load as load
import file_upload as upload
from ac_classes import IndivModel as imodel
from ac_classes import BiDataModel as bdmodel
from ac_classes import MultiDataModel as mdmodel
from nonlinear_regression import NonLinearRegression as nlr
from anova import main as anova_main

# Create instance
win = tk.Tk()   

# Add a title       
win.title("AnalyticsCal")

global csvList,x, y,X,Y,data,multi_data
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
    global multi_df
    file = fd.askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')]) # gets the filename as string
    if file:
        file_name = file.name
    print(file_name)
    csvHeader, csvList = upload.preprocess_csv(file_name)
    if len(csvHeader) > 2: # Multinomial
        multi_df = pd.read_csv(file_name)
        print(multi_df[~multi_df.applymap(np.isreal).all(1)])
        null_columns=multi_df.columns[multi_df.isnull().any()]
        print(multi_df[multi_df.isnull().any(axis=1)][null_columns].head())
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

mighty3 = ttk.LabelFrame(tab1,text='Prediction')
mighty3.grid(column=0,row=2,padx=2,pady=1)

# Add big textbox
text_h= 35
text_w = 90
textBox = tk.Text(mighty1, height = text_h, width = text_w,wrap=tk.WORD)
textBox.grid(column=0, row=5, sticky=tk.N+tk.S)

def create_data_list():
    global x,y,X,Y, data, multi_data
    if csvList != []:
        if len(csvHeader) <= 2:
            x = [float(i) for i in csvList[0]]
            y = [float(i) for i in csvList[-1]]
            # Create classes
            X = imodel(x)
            Y = imodel(y)
            data = bdmodel(X, Y)
            create_instance()
        elif len(csvHeader) > 2:
            X = []
            for idx,i in enumerate(csvList):
                if idx != 0:
                    temp = [float(j) for j in i]
                    X.append(temp)
            y = [float(i) for i in csvList[0]]
            Y = imodel(y)
            multi_data = mdmodel(X, Y.values)
            create_instance()
            
    else:
        print('No Data :(')

# to create instance immediately after fetching data
def create_instance():
    global X, Y, data, multi_data
    if len(csvHeader) <=2 :
        X.mean()
        Y.mean()
        X.var()
        Y.var()
        data.corr_coeff()
        data.nlr_coef()
        data.anova()
        data.models()
    else:
        multi_data.x_stats()
        multi_data.y_stats()
        multi_data.linear_regression_coeff()
        
def round_off_list(my_list, precision):
    return [round(_, precision) for _ in my_list]

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

# Modified Button statistics Function
def click_stats(textBox):
    global X,Y, data,multi_data
    precision = 2
    if len(csvHeader) <= 2:
        
        textBox.delete(1.0, tk.END) # clear anything previously present
        """
        textBox.insert(tk.INSERT, 'x_bar ='+ str(round(X.mean, precision))+'\n')
        textBox.insert(tk.INSERT, 'x_var ='+ str(round(X.var,precision))+'\n')
        textBox.insert(tk.INSERT, 'x_standard_dev ='+ str(round(math.sqrt(X.var), precision))+'\n')
        textBox.insert(tk.INSERT, 'y_bar ='+ str(round(Y.mean, precision))+'\n')
        textBox.insert(tk.INSERT, 'y_var ='+ str(round(Y.var, precision))+'\n')
        textBox.insert(tk.INSERT, 'y_standard_dev ='+ str(round(math.sqrt(Y.var),precision))+'\n')
        #textBox.insert(tk.INSERT, 'Cov(x, y) ='+ str(data.cov())+'\n')
        textBox.insert(tk.INSERT, 'Correlation coeeficient ='+ str(round(data.corr_coeff, precision))+'\n')
        """
        table=[["Mean",round(X.mean, precision),round(Y.mean, precision)],["Variance",round(X.var,precision),round(Y.var, precision)],["Std.Deviation",round(math.sqrt(X.var), precision),round(math.sqrt(Y.var),precision)],["Corel Coeff(X,Y)",round(data.corr_coeff, precision)]]
        headers= ["","X","Y"]
        textBox.insert(tk.INSERT,tabulate(table,headers,tablefmt="fancy_grid", floatfmt=".2f")) # decimal precision 2

        if data.corr_coeff < data.threshold:
            _stats_msgBox()
    else:
        """
        textBox.delete(1.0, tk.END) # clear anything previously present
        textBox.insert(tk.INSERT, 'X_mean = '+ str(round_off_list(multi_data.x_mean,precision))+'\n')
        textBox.insert(tk.INSERT, 'x_var ='+ str(round_off_list(multi_data.x_var, precision))+'\n')
        textBox.insert(tk.INSERT, 'x_standard_dev ='+ str(round_off_list(multi_data.x_std_dev, precision))+'\n')
        textBox.insert(tk.INSERT, 'y_bar ='+ str(round(multi_data.y_mean,precision))+'\n')
        textBox.insert(tk.INSERT, 'y_var ='+ str(round(multi_data.y_var, precision))+'\n')
        textBox.insert(tk.INSERT, 'y_standard_dev ='+ str(round(multi_data.y_std_dev,precision))+'\n')
        """
        # Create list for table
        mean_table = ["Mean"]
        mean_table.extend(round_off_list(multi_data.x_mean,precision))
        mean_table.append(round(multi_data.y_mean,precision))

        variance_table = ["Variance"]
        variance_table.extend(round_off_list(multi_data.x_var, precision))
        variance_table.append(round(multi_data.y_var, precision))

        std_dev_table = ["Std.Deviation"]
        std_dev_table.extend(round_off_list(multi_data.x_std_dev, precision))
        std_dev_table.append(round(multi_data.y_std_dev,precision))

        #correlation_coeff_table = ["Correlation Coeffecient"]
        headers = [""]
        headers.extend(csvHeader[1:])
        headers.append(csvHeader[0])

        table = []
        table.append(mean_table)
        table.append(variance_table)
        table.append(std_dev_table)

        textBox.delete(1.0, tk.END) # clear anything previously present
        textBox.insert(tk.INSERT,tabulate(table,headers,tablefmt="fancy_grid", floatfmt=".2f"))
        
        
        #textBox.insert(tk.INSERT, 'Cov(x, y) ='+ str(data.cov())+'\n')
        #textBox.insert(tk.INSERT, 'Correlation coeeficient ='+ str(round(data.corr_coeff, precision))+'\n')
        #if data.corr_coeff < data.threshold:
        #    _stats_msgBox()
        


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
    global X, Y,multi_data, multi_df
    if len(csvHeader) <= 2:
        plt.scatter(X.values, Y.values,alpha=1)					
        plt.title('Scatter plot of x and y')					
        plt.xlabel('x')					
        plt.ylabel('y')
        plt.tight_layout()
        plt.show()
    else:
        """
        jet=plt.get_cmap('jet')
        for i in multi_data.x:
            plt.scatter(i, multi_data.y , alpha = 1)
        """
        #Piarplot Data Visualization, type this code and see the output
        #sns.set(style="white")
        colors = ['red','green', 'blue', 'orange','purple']
        #labels1 = [0,1,2,3,4]
        #labels = []
        #for i in range(len(multi_data.y)):
        #    labels.append(labels1[i % 5])
        
        #g = pd.plotting.scatter_matrix(multi_df, figsize=(10,10), marker = 'o', hist_kwds = {'bins': 10}, s = 60, alpha = 0.8,cmap=matplotlib.colors.ListedColormap(colors),c = labels)
        g = pd.plotting.scatter_matrix(multi_df, figsize=(10,10), marker = 'o', hist_kwds = {'bins': 10}, s = 60, alpha = 0.8)
        plt.suptitle('Scatter Matrix')
        #plt.tight_layout()
        #plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=-1.0)
        plt.show()
        #sns.pairplot(multi_df, diag_kind ='kde')
# Add button for plot
plot = ttk.Button(mighty, text="Plot", command=click_plot, width = mighty_width)   
plot.grid(column=0, row=1, sticky='W')

# Multi plot
"""
fig = create_plot()

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack()
"""
#----------------------------------------------------------------------Linear Regression
def click_linear_regression():
    global X,Y, data
    roundoff = 2
    precision = roundoff
    if len(csvHeader) > 2:
        global multi_data
        print("This is MultiRegression")
        coeff = mlr.multi_linear_regression(copy.deepcopy(multi_data.x), copy.deepcopy(multi_data.y))
        equation_str = stats_display(round_off_list(coeff, precision))
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, equation_str)
        

    else:
        global reg_order
        reg_order =1 
        coeff = mlr.multi_linear_regression([X.values], Y.values)
        data.linear['coeff'] = [round(coeff[i], precision) for i in range(len(coeff))]
        equation_str = stats_display(round_off_list(coeff, precision))
        textBox.delete(1.0, tk.END)
        print(equation_str)
        textBox.insert(tk.INSERT, equation_str)
        """coeff_list =copy.deepcopy(coeff)
        Y_predicted = form_eqn(copy.deepcopy(coeff))
        coefficient_str = ''
        n = len(coeff)
        for i in range(len(coeff)):
            if(coeff[n - i -1] > 0):
                coefficient_str += '+'
                
            coefficient_str += str(round(coeff[n - i - 1], roundoff))
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
        data.poly_coeff = [round(coeff[i], roundoff) for i in range(n)]
            
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, equation_str)
        """
        title= "predicted vs actual"					
        x_label= 'X'					
        y_label= 'Y'
        reg_plot(X.values, Y.values, Y_predicted, equation_str, title, x_label, y_label, 'g')
        plt.show()
        
"""
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
"""
def stats_display(coeff):
    global csvHeader
    global multi_data,textBox
    roundoff = 2
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # For printing subscript
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    if len(csvHeader) > 2:
        #textBox.delete(1.0, tk.END)
        #textBox.insert(tk.INSERT, 'str(coeff)' + 'str(coeff)')
        coeff_list =copy.deepcopy(coeff)
        Y_predicted = form_eqn_mlr(coeff_list)
        coefficient_str = ''
        n = len(coeff)
        for i in range(len(coeff)):
        
            if i > 0:
                if coeff[i] > 0:
                    coefficient_str += '+'
                coefficient_str += str(coeff[i]) 
                # note subscript unicode 3 is printed as 1
                if i != 3:
                    coefficient_str += 'x' + str(i).translate(SUB) + ' '
                else:
                    coefficient_str += 'x' + '3 '
            else:
                coefficient_str += str(coeff[i]) + ' '
        equation_str = coefficient_str
        if(equation_str[0] == '+'):
            temp = list(equation_str)
            del(temp[0])
            equation_str = "".join(temp)
        multi_data.lin_reg_coeff = []
        multi_data.lin_reg_coeff  = [round(coeff[i], roundoff) for i in range(n)]
        #print('hi',equation_str)
        return equation_str
        #textBox.delete(1.0, tk.END)
        #textBox.insert(tk.INSERT, equation_str)
    else:
        Y_predicted = form_eqn(copy.deepcopy(coeff))
        coefficient_str = ''
        n = len(coeff)
        for i in range(len(coeff)):
            if(coeff[n - i -1] > 0):
                coefficient_str += '+'
                
            coefficient_str += str(round(coeff[n - i - 1], roundoff))

            if(i == (n - 2)):
                coefficient_str += 'x '
            elif(i != (n - 1)):
                coefficient_str += 'x'+ str(n - i - 1).translate(SUP) +' '
            else:
                coefficient_str += str(n - i - 1)
        equation_str = coefficient_str

        if(equation_str[0] == '+'):# remove '+' sign in the first term
            temp = list(equation_str)
            del(temp[0])
            equation_str = "".join(temp)

        data.poly_coeff = []
        data.poly_coeff = [round(coeff[i],roundoff ) for i in range(n)]
            
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT,'The linear model is \n' + equation_str)
        data.linear['eqn'] = equation_str
        title= "predicted vs actual"					
        x_label= 'X'					
        y_label= 'Y'
        reg_plot(X.values, Y.values, Y_predicted, equation_str, title, x_label, y_label, 'g')
        plt.show()
        return equation_str
    

def form_eqn_mlr(coeff):
    global multi_data
    temp = []
    for i in range(len(multi_data.x[0])):
        temp.append(coeff[0]+ coeff[1]*multi_data.x[0][i] +coeff[2]*multi_data.x[1][i] + coeff[3]*multi_data.x[2][i])
    print('form_eqn_mlr',temp)
    return temp

# Add button to Regression
linear_Regression = ttk.Button(mighty, text="Linear Regression", command=click_linear_regression,width = mighty_width)   
linear_Regression.grid(column=0, row=2, sticky='W')

#-----------------------------------------------------------------------Non Linear Regerssion

##Polynomail Regression

# Poly_reg:Modified Button Click Function
def click_nlr_poly():
    if len(csvHeader) <= 2:
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # For printing subscript
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        global X,Y, data
        precision = 2
        regression = nlr(X.values,Y.values)
        global reg_order
        reg_order = int(number_chosen_poly.get())
        coefficient = regression.polynomial(reg_order)
        coeff_list =copy.deepcopy(coefficient)
        Y_predicted = form_eqn(copy.deepcopy(coefficient))
        coefficient_str = ''
        n = len(coefficient)
        for i in range(len(coefficient)):
            if(coefficient[n - i -1] > 0):
                coefficient_str += '+'
                
            coefficient_str += str(round(coefficient[n - i - 1], precision))
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
        #data.poly_coeff = [round(coefficient[n - i - 1], precision) for i in range(n)]
        data.poly_coeff = [round(coefficient[i], precision) for i in range(n)]
            
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, equation_str)
        if reg_order == 2:
            str_2 = '\n'.join(list(chunkstring(equation_str, 14)))
            data.poly_2['eqn'] = str_2 # 12 harcoded for this textbox width = 90
            data.poly_2['coeff'] = [round(coefficient[i], precision) for i in range(n)]
        elif reg_order == 3:
            str_3 = '\n'.join(list(chunkstring(equation_str, 14)))
            data.poly_3['eqn'] = str_3
            data.poly_3['coeff'] = [round(coefficient[i], precision) for i in range(n)]
        elif reg_order == 4:
            str_4 = '\n'.join(list(chunkstring(equation_str, 14)))
            data.poly_4['eqn'] = str_4
            data.poly_4['coeff'] = [round(coefficient[i], precision) for i in range(n)]
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
    else:
        global multi_data
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, "Polynomial Regression works for bivariate data only\n")
        
    
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
    if len(csvHeader) <= 2:
        regression = nlr(X.values,Y.values)
        #print(int(number_chosen_sin.get()))
        #coefficient = regression.sinusoidal(int(number_chosen_sin.get()))
        coefficient = regression.sinusoidal(4)
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, str(coefficient))
    else:
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, "Sinusoidal Regression works for bivariate data only\n")

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
    if len(csvHeader) <=2:
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
    else:
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, "Exponential Regression works for bivariate data only\n")

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
    global X,Y,data,reg_order
    precision = 2
    if len(csvHeader) <= 2:
        anova_dict = anova_main(X.values, Y.values,data.poly_coeff)
        data.msr = anova_dict['msr']
        data.mse = anova_dict['mse']
        data.ssr = anova_dict['ssr']
        data.sse = anova_dict['sse']
        data.f = anova_dict['f']
        data.p = anova_dict['p']
        textBox.delete(1.0, tk.END)
        """
        textBox.insert(tk.INSERT, 'ANOVA'+ '\n')
        textBox.insert(tk.INSERT, 'msr = '+ str(round(data.msr, 4)) + '\n')
        textBox.insert(tk.INSERT, 'mse = '+ str(round(data.mse, 4))+ '\n')
        textBox.insert(tk.INSERT, 'ssr = '+ str(round(data.ssr, 4)) + '\n')
        textBox.insert(tk.INSERT, 'sse = '+ str(round(data.sse,4)) + '\n')
        textBox.insert(tk.INSERT, 'f = '+ str(round(data.f, 4))  + '\n')
        textBox.insert(tk.INSERT, 'p = '+ str(round(data.p,4)) + '\n')
        """
        table=[["msr",data.msr],["mse",data.mse],["ssr",data.ssr],["sse",data.sse],["f",data.f],["p",data.p]]
        headers= ["ANOVA","Values"]
        textBox.insert(tk.INSERT,tabulate(table,headers,tablefmt="fancy_grid",floatfmt=".2f"))

        if reg_order == 2:
            #str_2 = '\n'.join(list(chunkstring(equation_str, 12)))
            data.poly_2['f'] = round(data.f, precision)  
            data.poly_2['p'] = round(data.p, precision) 
        elif reg_order == 3:
            #str_3 = '\n'.join(list(chunkstring(equation_str, 12)))
            data.poly_3['f'] = round(data.f, precision)  
            data.poly_3['p'] = round(data.p, precision) 
        
        elif reg_order == 4:
            #str_4 = '\n'.join(list(chunkstring(equation_str, 14)))
            data.poly_4['f'] = round(data.f, precision)    
            data.poly_4['p'] = round(data.p, precision) 

        elif reg_order == 1:
            data.linear['f'] = round(data.f, precision)  
            data.linear['p'] = round(data.p, precision) 
        
    else:
        # Add the code for multiple linear regression
        
        ...
    

# Add button for ANOVA
anova = ttk.Button(mighty, text="ANOVA", command=click_anova,width = mighty_width)   
anova.grid(column=0, row=4, sticky='W')

#------------------------------------------------------------------------------Comparison

def click_comparison():
    if len(csvHeader) <= 2:

        eqn_table = ["Equation"]
        eqn_table.append(data.linear['eqn'])
        eqn_table.append(data.poly_2['eqn'])
        eqn_table.append(data.poly_3['eqn'])
        eqn_table.append(data.poly_4['eqn'])

        f_table = ["f"]
        f_table.append(data.linear['f'])
        f_table.append(data.poly_2['f'])
        f_table.append(data.poly_3['f'])
        f_table.append(data.poly_4['f'])

        p_table = ["p"]
        p_table.append(data.linear['p'])
        p_table.append(data.poly_2['p'])
        p_table.append(data.poly_3['p'])
        p_table.append(data.poly_4['p'])

        table = []
        table.append(eqn_table)
        table.append(f_table)
        table.append(p_table)

        headers = ["Linear \n Model", "Polynomial \n Degree 2", "Polynomial \n Degree 3","Polynomial \n Degree 4"]
        #headers.extend(csvHeader[1:])
        #headers.append(csvHeader[0])


        textBox.delete(1.0, tk.END) # clear anything previously present
        textBox.insert(tk.INSERT,tabulate(table,headers,tablefmt="fancy_grid", floatfmt=".2f"))

        print(f_table)
        model_choice = ["","Linear Model", "Polynomial model of order 2","Polynomial model of order 3",
                        "Polynomial model of order 4"]
        textBox.insert(tk.INSERT,"\n CONCLUSION: \n" + model_choice[f_table.index(max(f_table[1:]))] + " : ("+\
                       eqn_table[f_table.index(max(f_table[1:]))].replace('\n','')+ " ) " + " is better fit for given data.\n" +\
                       model_choice[f_table.index(max(f_table[1:]))] + " : (" + eqn_table[f_table.index(max(f_table[1:]))].replace('\n','')+\
                       " )"+ " is chosen for Prediction")
        
        predict_model = ["",'linear','poly_2','poly_3', 'poly_4']
        if(f_table.index(max(f_table[1:])) == 1):
            data.pred_model = data.linear['coeff']
        elif(f_table.index(max(f_table[1:])) == 2):
            data.pred_model = data.poly_2['coeff']
        elif(f_table.index(max(f_table[1:])) == 3):
            data.pred_model = data.poly_3['coeff']
        elif(f_table.index(max(f_table[1:])) == 4):
            data.pred_model = data.poly_4['coeff']
        
    else:
        ...

comparison_button = ttk.Button(mighty, text="Compare Models", command=click_comparison,width = mighty_width)   
comparison_button.grid(column=0, row=5, sticky='W')

#------------------------------------------------------------------------------------------------Prediction
lab=ttk.Label(mighty3,text="Enter Value for Prediction")
lab.grid()
E1=ttk.Entry(mighty3)
E1.grid()
var=tk.StringVar()
"""
lab1=ttk.Label(mighty3,text="Enter MultiValue for Prediction")
lab1.grid()
E2=ttk.Entry(mighty3,textvariable=var)
E2.grid()
"""
def predict_value():
    value=E1.get()
    v1=var.get()
    if value != '':
        coeff_list = copy.deepcopy(data.pred_model)
        pred_x=float(value)
        pred_y= round (coeff_list[0] + (coeff_list[1]*pred_x) + (coeff_list[2]*(pred_x**2))+ (coeff_list[3]*(pred_x**3)), 2)
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, str(pred_y))

predict = ttk.Button(mighty3,text="Predict",command=predict_value,width= 26)
predict.grid(column=0,row=2,sticky='w')

#----------------------------------------------------------------------------------------------------TIMESERIES
# LabelFrame using tab2 as the parent - for Time series plot
mighty_t1 = ttk.LabelFrame(tab2, text=' PLOT')
mighty_t1.grid(column=0, row=0, padx=8, pady=4)

# LabelFrame using tab2 as the parent - for ARMA/ARIMA
mighty_t2 = ttk.LabelFrame(tab2, text=' ARMA/ARIMA')
mighty_t2.grid(column=0, row=1, padx=8, pady=4)

# LabelFrame using tab2 as the parent - for ARIMA
#mighty_t3 = ttk.LabelFrame(tab2, text=' ARIMA')
#mighty_t3.grid(column=0, row=2, padx=8, pady=4)

# LabelFrame using tab2 as the parent - for output console
mighty_t3 = ttk.LabelFrame(tab2, text=' Output Console')
mighty_t3.grid(column=1, row=0,sticky=tk.N+tk.S, padx=8, pady=4, columnspan=3, rowspan = 6)

def click_Line_Plot():
    ...
mighty_width = 18
# Add buttons for RAW Line Plot
Line_Plot = ttk.Button(mighty_t1, text="Line Plot", command= lambda : click_Line_Plot(), width = mighty_width)   
Line_Plot.grid(column=0, row=0, sticky='W')

def click_ACF_Plot():
    ...
mighty_width = 18
# Add buttons for ACF Bar Plot
ACF_Plot = ttk.Button(mighty_t1, text="ACF Plot", command= lambda : click_ACF_Plot(), width = mighty_width)   
ACF_Plot.grid(column=0, row=1, sticky='W')

def ARMA():
    ...
# Textbox to input seanonal difference value
ttk.Label(mighty_t2, text="N:  ").grid(column=0, row=0)

# Adding a Text box Entry widget
N_Value = tk.StringVar()
N_Value_entered = ttk.Entry(mighty_t2, width=8, textvariable=N_Value)
N_Value_entered.grid(column=1, row=0)

# Textbox to input P value
ttk.Label(mighty_t2, text="P:  ").grid(column=0, row=1)

# Adding a Text box Entry widget
P_Value = tk.StringVar()
P_Value_entered = ttk.Entry(mighty_t2, width=8, textvariable=P_Value)
P_Value_entered.grid(column=1, row=1)

# Textbox to input D value
ttk.Label(mighty_t2, text="D:  ").grid(column=0, row=2)

# Adding a Text box Entry widget
D_Value = tk.StringVar()
D_Value_entered = ttk.Entry(mighty_t2, width=8, textvariable=D_Value)
D_Value_entered.grid(column=1, row=2)

# Textbox to input Q value
ttk.Label(mighty_t2, text="Q:  ").grid(column=0, row=3)

# Adding a Text box Entry widget
Q_Value = tk.StringVar()
Q_Value_entered = ttk.Entry(mighty_t2, width=8, textvariable=Q_Value)
Q_Value_entered.grid(column=1, row=3)

#Adding a button to submit the values
def click_Calculate_ARMA():
    ...
#mighty_width = 18
# Add button for ARMA
Calculate_ARMA = ttk.Button(mighty_t2, text="ARMA", command= lambda : click_Calculate_ARMA(), width = 8)   
Calculate_ARMA.grid(column=0, row=4, sticky='W')

def click_Calculate_ARIMA():
    ...
#mighty_width = 18
# Add button for ARIMA
Calculate_ARIMA = ttk.Button(mighty_t2, text="ARIMA", command= lambda : click_Calculate_ARIMA(), width = 8)   
Calculate_ARIMA.grid(column=1, row=4, sticky='W')

# Add big textbox for time series
text_h= 35
text_w = 75
textBox_t1 = tk.Text(mighty_t3, height = text_h, width = text_w,wrap=tk.WORD)
textBox_t1.grid(column=0, row=5, sticky=tk.N+tk.S)

#name_entered.focus()      # Place cursor into name Entry
#======================
# Start GUI
#======================
win.mainloop()
