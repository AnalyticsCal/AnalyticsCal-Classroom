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
#import Partial_Correlation_Coeff_XYZ as pcc_xyz
import multilinear_regression as mlr
import data_load as load
import file_upload as upload
from ac_classes import IndivModel as imodel
from ac_classes import BiDataModel as bdmodel
from ac_classes import MultiDataModel as mdmodel
from nonlinear_regression import NonLinearRegression as nlr
from anova import main as anova_main
from anova_CI import AnovaConfidenceInterval
from anova_class import Anova as Anova_class

# Create instance
win = tk.Tk()   

# Add a title       
win.title("AnalyticsCal")

global csvList,x, y,X,Y,data,multi_data,Y_predicted,is_simple_linear_equations
global csvHeader
global file_name
is_simple_linear_equations=False
#-------------------------------------------------------------------------Plots

def reg_plot(x_plot,y_plot,y_predicted, equation_str, title, x_label, y_label, color = None):
    plt.clf()
    raw_plot = plt.scatter(x_plot, y_plot, color = 'b')
    predict_plot, = plt.plot(x_plot,y_predicted , '-',color = color)
    plt.title(title)					
    plt.xlabel(x_label)					
    plt.ylabel(y_label)
    plt.legend((raw_plot, predict_plot),('Observed Data', 'Prediction equation = ' + equation_str),loc=(-0.05,-0.20), scatterpoints=1, ncol=3, fontsize=8)
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
    database function has to be called here 
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

#-----------------------------------------------------------------------Team2 -Outlier
def median(a, l, r): 
    n1 = r - l + 1
    n1 = (n1 + 1)/ 2 - 1; 
    return int(n1 + l) 

def get_outLiers(x1):
    n=len(x1)  
    x1.sort() 
    mid_index = median(x1, 0, n) 
    Q1 = x1[median(x1, 0, mid_index)] 
    Q3 = x1[median(x1, mid_index + 1, n)] 
    IQR= Q3 - Q1
    Lower_bound = Q1 -(1.5 * IQR) 
    Upper_bound = Q3 +(1.5 * IQR) 
    print(Lower_bound,Upper_bound)
    outlier_list = list(filter(lambda i: float(i) >Upper_bound or float(i)<Lower_bound, x1))
    return outlier_list

def display_outliers():
    global data
    #data.x.values = [1,58,639,2,3,100000,5]
    #data.y.values = [1,58,69,8,5,899999,84]
    outlier_list_x = get_outLiers(copy.deepcopy(data.x.values))
    data.outlier_x = outlier_list_x
    outlier_list_y = get_outLiers(copy.deepcopy(data.y.values))
    data.outlier_y = outlier_list_y
    textBox.delete(1.0, tk.END)
    #textBox.insert(tk.INSERT, 'Outliers for x'+ str(data.outlier_x)+'\n')
    display_list_out = list(zip(data.outlier_x, data.outlier_y))
    if display_list_out != []:
        textBox.insert(tk.INSERT, 'Outliers are '+ str(display_list_out)+'\n')
    else:
        """No outliers"""
        ...
#-----------------------------------------------------------------------team 3
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
mighty2.grid(column = 0, row=1, padx=10, pady=2)
#mighty2.grid_columnconfigure(0, weight=1)

mighty3 = ttk.LabelFrame(tab1,text='Prediction')
mighty3.grid(column=0,row=2,padx=15,pady=4)

# Add big textbox
text_h= 35
text_w = 95
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
        data.pred_model()
        data.outliers()
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
        display_outliers()
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

        #pcc_table = ["Partial \n Correlation\n Coeff ryx,"]
        #pcc_table.append(pcc_xyz.PartialcorrelationCoefficientXY_Z(multi_data.x[0]))

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
Statistics.grid(column=0, row=0, sticky='W', padx = 10,pady = 2)
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
plot.grid(column=0, row=1, sticky='W', padx = 10,pady = 2)

# Multi plot
"""
fig = create_plot()

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack()
"""
#----------------------------------------------------------------------Linear Regression
def click_linear_regression():
    global X,Y, data,Y_predicted,is_simple_linear_equations,coeff,coeff_m
    is_simple_linear_equations = True
    roundoff = 2
    precision = roundoff
    if len(csvHeader) > 2:
        global multi_data
        print("This is MultiRegression")
        coeff = mlr.multi_linear_regression(copy.deepcopy(multi_data.x), copy.deepcopy(multi_data.y))
        equation_str = stats_display(round_off_list(coeff, precision))
        Y_predicted = form_eqn_mlr(copy.deepcopy(coeff))
        coeff_m = coeff
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT,"The linear regression Equation is\n " + equation_str)
        #textBox.tag_add("one", "1.0", "1.8")
        #textBox.tag_config("one", background="yellow"_norm)

    else:
        global reg_order
        reg_order =1 
        coeff = mlr.multi_linear_regression([X.values], Y.values)
        
        data.linear['coeff'] = [round(coeff[i], precision) for i in range(len(coeff))]
        equation_str = stats_display(round_off_list(coeff, precision))
        
        Y_predicted = form_eqn_mlr(copy.deepcopy(coeff))
        textBox.delete(1.0, tk.END)
        print(equation_str)
        textBox.insert(tk.INSERT,"The linear regression Equation is\n " + equation_str)
        #textBox.tag_add("one", "1.0", "1.8")
        #textBox.tag_config("one", background="yellow"_norm)
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
        title= "predicted vs observed"					
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
    global Y_predicted
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
        str_1 = '\n'.join(list(chunkstring(equation_str, 14)))
        data.linear['eqn'] = str_1
        title= "Predicted vs Observed"					
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
linear_Regression.grid(column=0, row=2, sticky='W', padx = 10,pady = 2)

#-----------------------------------------------------------------------Non Linear Regerssion

##Polynomail Regression

# Poly_reg:Modified Button Click Function
def click_nlr_poly():
    global Y_predicted,is_simple_linear_equations
    is_simple_linear_equations=False
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
        title= "Predicted vs Observed"					
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
polynomial_regression = ttk.Button(mighty2, text="Polynomial Regression", command=click_nlr_poly,width = 26)   
polynomial_regression.grid(column=0, row=0, sticky='W',padx = 9,pady =3 )

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

sinusoidal_regression = ttk.Button(mighty2, text="Sinusoidal Regression", command=click_nlr_sin,width = 26)   
sinusoidal_regression.grid(column=0, row=1, sticky='W',padx=10,pady = 2)
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
        textBox.insert(tk.INSERT, coefficient_str[0]+'e^'+coefficient_str[1]+'x')
    else:
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, "Exponential Regression works for bivariate data only\n")

exponential_regression = ttk.Button(mighty2, text="Exponential Regression", command=click_nlr_exp,width = 26)   
exponential_regression.grid(column=0, row=2, sticky='W',padx = 10,pady = 2)

## Exponential Transformation

def click_nlr_exp_trf():
    global X,Y, data
    if len(csvHeader) <=2:
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # For printing subscript
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        regression = nlr(X.values,Y.values)
        #print('regression = ',regression)
        coefficient = regression.exponentialTransformation(1)
        if(math.isnan(coefficient[0])):
            coefficient_str = "The exponential model is not a right fit for this data"
            print(coefficient_str)
            #print('coeff = ', coefficient)
        else:
            coefficient_str = [str(i) for i in coefficient ]
        #print(coefficient_str)
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, coefficient_str[0]+'e^'+coefficient_str[1]+'x')
    else:
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, "Exponential Transformation implemented for bivariate data only\n")
        
exponential_transformation = ttk.Button(mighty2, text="Exponential Transformation", command=click_nlr_exp_trf,width = 26)   
exponential_transformation.grid(column=0, row=3, sticky='W', padx = 10,pady = 2)



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
    global Y_predicted,coeff
    precision = 2
    
    if len(csvHeader) <= 2:
        anova_dict = anova_main(X.values, Y.values,data.poly_coeff)
        anova_class_2 = Anova_class(Y.values, Y_predicted, len(csvHeader))
        data.msr = anova_dict['msr']
        data.mse = anova_dict['mse']
        data.ssr = anova_dict['ssr']
        data.sse = anova_dict['sse']
        data.f = anova_dict['f']
        data.p = anova_dict['p']
        
        data.model_confidence=anova_class_2.model_confidence
        if(is_simple_linear_equations):
            anova_CI=AnovaConfidenceInterval(X.values,Y.values,Y_predicted,len(csvHeader))
            ci_rtn=anova_CI.cal_CI_tm_tc(95)
            data.t_m=ci_rtn["tm"]
            data.t_c=ci_rtn["tc"]
            textBox.insert(tk.INSERT, "\n\n Confidence Interval:\n")
            ci_table=[
                        ["m",str(round(coeff[1] - data.t_m,4)),str(round(coeff[1] + data.t_m,4))],
                        ["c",str(round(coeff[0] - data.t_c,4)),str(round(coeff[0] + data.t_c,4))]
                    ]
            textBox.insert(tk.INSERT,tabulate(ci_table,["Coeffient","min","max"],tablefmt="fancy_grid", floatfmt=".2f"))


        
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
        table=[["msr",data.msr],["mse",data.mse],["ssr",data.ssr],["sse",data.sse],["f",data.f],["p",data.p],["Model Confidence",data.model_confidence]]
        headers= ["ANOVA","Values"]
        textBox.insert(tk.INSERT,tabulate(table,headers,tablefmt="fancy_grid",floatfmt=".2f"))

        if(is_simple_linear_equations):
            textBox.insert(tk.INSERT, "\n\n Confidence Interval:\n")
            ci_table=[
                        ["m",str(round(coeff[1] - data.t_m,4)),str(round(coeff[1] + data.t_m,4))],
                        ["c",str(round(coeff[0] - data.t_c,4)),str(round(coeff[0] + data.t_c,4))]
                    ]
            textBox.insert(tk.INSERT,tabulate(ci_table,["Coeffient","min","max"],tablefmt="fancy_grid", floatfmt=".2f"))

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
        anova_class_2 = Anova_class(Y.values, Y_predicted, len(csvHeader))
        multi_data.msr = anova_class_2.msr
        multi_data.mse = anova_class_2.mse
        multi_data.ssr = anova_class_2.ssr
        multi_data.sse = anova_class_2.sse
        multi_data.f = anova_class_2.f
        multi_data.p = anova_class_2.p
        multi_data.model_confidence=anova_class_2.model_confidence

        textBox.insert(tk.INSERT,"\n\n\n Anova Values: \n")
        table=[ ["Regression",anova_class_2.ssr_drg_of_freedom,round(anova_class_2.ssr,4),round(anova_class_2.msr,4),round(anova_class_2.f,4),str(round(anova_class_2.p,4))],
                ["Error",anova_class_2.sse_dgr_pf_freedom,round(anova_class_2.sse,4),round(anova_class_2.mse,4),None,None],
                ["Total",anova_class_2.sse_dgr_pf_freedom+anova_class_2.ssr_drg_of_freedom,round(anova_class_2.sse + anova_class_2.ssr,4),None,None,None]
            ]
        table.append([])
        textBox.insert(tk.INSERT,tabulate(table,['Source','df','SS','MS','F','P'],tablefmt="fancy_grid", floatfmt=".2f")) 
        textBox.insert(tk.INSERT, "\n")
        
        
    

# Add button for ANOVA
anova = ttk.Button(mighty, text="ANOVA", command=click_anova,width = mighty_width)   
anova.grid(column=0, row=4, sticky='W', padx = 10,pady = 2)

#------------------------------------------------------------------------------Comparison

def table_highlight (is_clear = True,max_f_table = None):

    if(is_clear):
        bg_color_norm = "white"
        bg_color_eqn = bg_color_norm
        max_f_table = 0
        #.tag_remove(tagName, index1, index2=None) remove tag
        textBox.tag_delete("1,1", "2.12", "2.29")
        textBox.tag_delete("1,2", "3.12", "3.29")
        textBox.tag_delete("1,3", "4.12", "4.29")
        textBox.tag_delete("1,4", "5.12", "5.29")
        textBox.tag_delete("1,5", "6.12", "6.29")
        textBox.tag_delete("1,6", "7.12", "7.29")
        textBox.tag_delete("1,7", "8.12", "8.29")
        textBox.tag_delete("1,8", "9.12", "9.29")
        textBox.tag_delete("1,9", "10.12", "10.29")
        textBox.tag_delete("1,10", "11.12", "11.29")

        textBox.tag_delete("two,1", "2.30", "2.49")
        textBox.tag_delete("two,2", "3.30", "3.49")
        textBox.tag_delete("two,3", "4.30", "4.49")
        textBox.tag_delete("two,4", "5.30", "5.49")
        textBox.tag_delete("two,5", "6.30", "6.49")
        textBox.tag_delete("two,6", "7.30", "7.49")
        textBox.tag_delete("two,7", "8.30", "8.49")
        textBox.tag_delete("two,8", "9.30", "9.49")
        textBox.tag_delete("two,9", "10.30", "10.49")
        textBox.tag_delete("two,10", "11.30", "11.49")
        #textBox.tag_delete("one,11", "13.12", "2.32")

        textBox.tag_delete("3,1", "2.50", "2.68")
        textBox.tag_delete("3,2", "3.50", "3.68")
        textBox.tag_delete("3,3", "4.50", "4.68")
        textBox.tag_delete("3,4", "5.50", "5.68")
        textBox.tag_delete("3,5", "6.50", "6.68")
        textBox.tag_delete("3,6", "7.50", "7.68")
        textBox.tag_delete("3,7", "8.50", "8.68")
        textBox.tag_delete("3,8", "9.50", "9.68")
        textBox.tag_delete("3,9", "10.50", "10.68")
        textBox.tag_delete("3,10", "11.50", "11.68")

        textBox.tag_delete("4,1", "2.69", "2.89")
        textBox.tag_delete("4,2", "3.69", "3.89")
        textBox.tag_delete("4,3", "4.69", "4.89")
        textBox.tag_delete("4,4", "5.69", "5.89")
        textBox.tag_delete("4,5", "6.69", "6.89")
        textBox.tag_delete("4,6", "7.69", "7.89")
        textBox.tag_delete("4,7", "8.69", "8.89")
        textBox.tag_delete("4,8", "9.69", "9.89")
        textBox.tag_delete("4,9", "10.69", "10.89")
        textBox.tag_delete("4,10", "11.69", "11.89")
        print("removed tag")

    else:
        bg_color_norm = "yellow"
        bg_color_eqn = "red"
    
        textBox.tag_add("1,1", "2.12", "2.29")
        textBox.tag_add("1,2", "3.12", "3.29")
        textBox.tag_add("1,3", "4.12", "4.29")
        textBox.tag_add("1,4", "5.12", "5.29")
        textBox.tag_add("1,5", "6.12", "6.29")
        textBox.tag_add("1,6", "7.12", "7.29")
        textBox.tag_add("1,7", "8.12", "8.29")
        textBox.tag_add("1,8", "9.12", "9.29")
        textBox.tag_add("1,9", "10.12", "10.29")
        textBox.tag_add("1,10", "11.12", "11.29")

        textBox.tag_add("two,1", "2.30", "2.49")
        textBox.tag_add("two,2", "3.30", "3.49")
        textBox.tag_add("two,3", "4.30", "4.49")
        textBox.tag_add("two,4", "5.30", "5.49")
        textBox.tag_add("two,5", "6.30", "6.49")
        textBox.tag_add("two,6", "7.30", "7.49")
        textBox.tag_add("two,7", "8.30", "8.49")
        textBox.tag_add("two,8", "9.30", "9.49")
        textBox.tag_add("two,9", "10.30", "10.49")
        textBox.tag_add("two,10", "11.30", "11.49")
        #textBox.tag_add("one,11", "13.12", "2.32")

        textBox.tag_add("3,1", "2.50", "2.68")
        textBox.tag_add("3,2", "3.50", "3.68")
        textBox.tag_add("3,3", "4.50", "4.68")
        textBox.tag_add("3,4", "5.50", "5.68")
        textBox.tag_add("3,5", "6.50", "6.68")
        textBox.tag_add("3,6", "7.50", "7.68")
        textBox.tag_add("3,7", "8.50", "8.68")
        textBox.tag_add("3,8", "9.50", "9.68")
        textBox.tag_add("3,9", "10.50", "10.68")
        textBox.tag_add("3,10", "11.50", "11.68")

        textBox.tag_add("4,1", "2.69", "2.89")
        textBox.tag_add("4,2", "3.69", "3.89")
        textBox.tag_add("4,3", "4.69", "4.89")
        textBox.tag_add("4,4", "5.69", "5.89")
        textBox.tag_add("4,5", "6.69", "6.89")
        textBox.tag_add("4,6", "7.69", "7.89")
        textBox.tag_add("4,7", "8.69", "8.89")
        textBox.tag_add("4,8", "9.69", "9.89")
        textBox.tag_add("4,9", "10.69", "10.89")
        textBox.tag_add("4,10", "11.69", "11.89")

        if(max_f_table == 1):
            data.pred_model = data.linear['coeff']
            data.pred_eqn = data.linear['eqn']
            textBox.tag_config("1,1", background=bg_color_norm)
            textBox.tag_config("1,2", background=bg_color_norm)
            textBox.tag_config("1,3", background=bg_color_norm)
            textBox.tag_config("1,4", background=bg_color_eqn)
            textBox.tag_config("1,5", background=bg_color_eqn)
            textBox.tag_config("1,6", background=bg_color_eqn)
            textBox.tag_config("1,7", background=bg_color_norm)
            textBox.tag_config("1,8", background=bg_color_norm)
            textBox.tag_config("1,9", background=bg_color_norm)
            textBox.tag_config("1,10", background=bg_color_norm)

            
        elif(max_f_table == 2):
            data.pred_model = data.poly_2['coeff']
            data.pred_eqn = data.poly_2['eqn']
            textBox.tag_config("two,1", background=bg_color_norm)
            textBox.tag_config("two,2", background=bg_color_norm)
            textBox.tag_config("two,3", background=bg_color_norm)
            textBox.tag_config("two,4", background=bg_color_eqn)
            textBox.tag_config("two,5", background=bg_color_eqn)
            textBox.tag_config("two,6", background=bg_color_eqn)
            textBox.tag_config("two,7", background=bg_color_norm)
            textBox.tag_config("two,8", background=bg_color_norm)
            textBox.tag_config("two,9", background=bg_color_norm)
            textBox.tag_config("two,10", background=bg_color_norm)
            
        elif(max_f_table == 3):
            data.pred_model = data.poly_3['coeff']
            data.pred_eqn = data.poly_3['eqn']
            textBox.tag_config("3,1", background=bg_color_norm)
            textBox.tag_config("3,2", background=bg_color_norm)
            textBox.tag_config("3,3", background=bg_color_norm)
            textBox.tag_config("3,4", background=bg_color_eqn)
            textBox.tag_config("3,5", background=bg_color_eqn)
            textBox.tag_config("3,6", background=bg_color_eqn)
            textBox.tag_config("3,7", background=bg_color_norm)
            textBox.tag_config("3,8", background=bg_color_norm)
            textBox.tag_config("3,9", background=bg_color_norm)
            textBox.tag_config("3,10", background=bg_color_norm)

            
        elif(max_f_table == 4):
            data.pred_model = data.poly_4['coeff']
            data.pred_eqn = data.poly_4['eqn']
            textBox.tag_config("4,1", background=bg_color_norm)
            textBox.tag_config("4,2", background=bg_color_norm)
            textBox.tag_config("4,3", background=bg_color_norm)
            textBox.tag_config("4,4", background=bg_color_norm)
            textBox.tag_config("4,5", background=bg_color_norm)
            textBox.tag_config("4,6", background=bg_color_norm)
            textBox.tag_config("4,7", background=bg_color_norm)
            textBox.tag_config("4,8", background=bg_color_norm)
            textBox.tag_config("4,9", background=bg_color_norm)
            textBox.tag_config("4,10", background=bg_color_norm)
            textBox.tag_config("four,two", background=bg_color_norm)
        #textBox.tag_add("one", "1.0", "1.8")
        #textBox.tag_config("one", background=`_norm)

def compare_plot():
    return ...

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

        headers = ["Linear       \n Model", "Polynomial     \n Degree 2", "Polynomial    \n Degree 3","Polynomial      \n Degree 4"]
        #headers.extend(csvHeader[1:])
        #headers.append(csvHeader[0])


        textBox.delete(1.0, tk.END) # clear anything previously present
        textBox.insert(tk.INSERT,tabulate(table,headers,tablefmt="fancy_grid", floatfmt=".2f"))

        max_f_table = f_table.index(max(f_table[1:]))

        table_highlight(is_clear = False, max_f_table = max_f_table)

        print(f_table)
        model_choice = ["","Linear Model", "Polynomial model of order 2","Polynomial model of order 3",
                        "Polynomial model of order 4"]
        textBox.insert(tk.INSERT,"\n CONCLUSION: \n" + model_choice[max_f_table] + " : ("+\
                       eqn_table[max_f_table].replace('\n','')+ " ) " + " is better fit for given data.\n" +\
                       model_choice[max_f_table] + " : (" + eqn_table[max_f_table].replace('\n','')+\
                       " )"+ " is chosen for Prediction")
        
        predict_model = ["",'linear','poly_2','poly_3', 'poly_4']
        print("Max_f_table",max_f_table)
    """
            if(max_f_table == 1):
                data.pred_model = data.linear['coeff']
                data.pred_eqn = data.linear['eqn']
            elif(max_f_table == 2):
                data.pred_model = data.poly_2['coeff']
                data.pred_eqn = data.poly_2['eqn']
            elif(max_f_table == 3):
                data.pred_model = data.poly_3['coeff']
                data.pred_eqn = data.poly_3['eqn']
            elif(max_f_table == 4):
                data.pred_model = data.poly_4['coeff']
                data.pred_eqn = data.poly_4['eqn']
           
            else:
            ...
    """
comparison_button = ttk.Button(mighty, text="Compare Models", command=click_comparison,width = mighty_width)   
comparison_button.grid(column=0, row=5, sticky='W',padx = 10,pady = 2)

def click_clear():
    table_highlight()
    textBox.delete(1.0, tk.END)

clear_button = ttk.Button(tab1, text="CLEAR", command=click_clear,width = mighty_width)   
clear_button.grid(column=0, row=4, sticky='W',padx = 10,pady = 2)

#------------------------------------------------------------------------------------------------Prediction
lab=ttk.Label(mighty3,text="Enter Value for Prediction")
lab.grid(pady = 2,padx = 5)
E1=ttk.Entry(mighty3)
E1.grid(pady = 2,padx = 5)
var=tk.StringVar()

lab1=ttk.Label(mighty3,text="Enter MultiValue for Prediction")
lab1.grid(pady = 2,padx = 5)
E2=ttk.Entry(mighty3,textvariable=var)
E2.grid(pady = 2,padx = 5)

def predict_value():
    value=E1.get()
    global coeff_m
    v1=var.get()
    if value != '':
        coeff_list = copy.deepcopy(data.pred_model)
        
        for i in range(5 - len(coeff_list)):
            coeff_list.append(0.)
        print('Comapre_model:Coeff_list = ', coeff_list)
        pred_x=float(value)
        pred_ans = 0
        for idx,value in enumerate(coeff_list):
            exponent = idx
            base = pred_x
            pred_ans +=  value * (base**exponent)
        
        #pred_ans = [i * (pred_x **  for i in coeff_list]
        #pred_y= round (coeff_list[0] + (coeff_list[1]*pred_x) + ((coeff_list[2]*(pred_x**2))+ ((coeff_list[3]*(pred_x**3))+ ((coeff_list[4]*(pred_x**4))))), 2)
        pred_y = round(pred_ans,2)
        textBox.delete(1.0, tk.END)
        display_eqn= copy.deepcopy(data.pred_eqn)
        display_eqn.replace("\n","")
        textBox.insert(tk.INSERT,"The chosen model is "+'\n'+ display_eqn+ "\nPredicted value is:\n " + str(pred_y)  )

    elif v1 != '':
        v1 = v1.split()
        x1=float((v1[0]))
        x2=float((v1[1]))
        x3=float((v1[2]))
        pred_y_m = round(coeff_m[0]+ coeff_m[1]*x1 +coeff_m[2]*x2 + coeff_m[3]*x3, 4)
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.INSERT, 'predicted value is \n'+str(pred_y_m))

predict = ttk.Button(mighty3,text="Predict",command=predict_value,width= 26)
predict.grid(column=0,row=4,sticky='w',padx = 10,pady = 2)

#----------------------------------------------------------------------------------------------------TIMESERIES
"""
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
"""

# LabelFrame using tab2 as the parent - for Stationary
mighty_t1 = ttk.LabelFrame(tab2, text=' Stationarity')
mighty_t1.grid(column=0, row=1, padx=8, pady=2, sticky = 'N')

# LabelFrame using tab2 as the parent - for ARMA/ARIMA
mighty_t2 = ttk.LabelFrame(tab2, text= 'ARIMA')
mighty_t2.grid(column=0, row=2, padx=8, pady=2,sticky = 'N')

# LabelFrame using tab2 as the parent - for output console
mighty_t3 = ttk.LabelFrame(tab2, text=' Output Console')
mighty_t3.grid(column=1, row=0,sticky=tk.N+tk.S, padx=8, pady=4, rowspan = 6)

button_width = 15

global csvList_ts,file_name_ts,csvHeader_ts

def click_upload_data_ts():
    global csvList_ts,file_name_ts,csvHeader_ts
    global values_list_ts, header_list_ts
    #global multi_df
    file_ts = fd.askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')]) # gets the filename as string
    if file_ts:
        file_name_ts = file_ts.name
    print(file_name_ts)
    csvHeader_ts, csvList_ts = upload.preprocess_csv(file_name_ts)
    #values_list_ts = [[float(j) for j in i] for i in csvList_ts] # i is the element of csvList_ts -- which itself is a list, j is the member of i(j is the member\
                                                                # of list present in csvList_ts)
    values_list_ts = [list(map(float, i)) for i in csvList_ts] # convert all the elements of csvList into floats
    #values_list_ts = list(map(float,csvList_ts))
    header_list_ts = copy.deepcopy(csvHeader_ts)

upload_data_ts = ttk.Button(tab2, text="Load Data", command= lambda: click_upload_data_ts(), width = button_width,compound=tk.LEFT)
#upload_data_ts.pack(side = tk.LEFT)
#upload_data_ts.place(x=0,y=1) 
upload_data_ts.grid(column=0, row=0, padx=22, pady=2,sticky='W')

def click_seasonal_diff():
    #lags = int(tk.simpledialog.askstring('Lags', 'Enter the number of lags:'))
    lags = tk.simpledialog.askstring('Lags', 'Enter the number of lags:') # removed int

    if lags == None:# user clicked  cancel
        print('Seas_diff None')
    else:# user has input and clicked 'OK'
        print('Seas_diff lags',int(lags))
    print('seas_diff lags=',lags)
    ...
button_width = 20
seasonal_diff = ttk.Button(mighty_t1, text="Seasonal Difference", command= lambda : click_seasonal_diff(), width = button_width)
#seasonal_diff.config(justify=tk.LEFT)
seasonal_diff.grid(column=0, row=0, sticky='W',padx = 15,pady =3)

def click_normal_diff():
    lags = tk.simpledialog.askstring('Lags', 'Enter the number of lags:')
    if lags == None:
        print('Seas_diff None')
    else:
        print('Seas_diff lags',int(lags))
    ...

normal_diff = ttk.Button(mighty_t1, text="Normal Difference", command= lambda : click_normal_diff(), width = button_width)   
normal_diff.grid(column=0, row=1, sticky='W',padx = 15,pady =3)

def click_auto_regression():
    #lags = int(tk.simpledialog.askstring('Lags', 'Enter the number of lags:'))
    lags = tk.simpledialog.askstring('Lags', 'Enter the number of lags:') # removed int

    if lags == None:# user clicked  cancel
        print('Seas_diff None')
    else:# user has input and clicked 'OK'
        print('Seas_diff lags',int(lags))
    print('seas_diff lags=',lags)
    ...
button_width = 18

auto_regression = ttk.Button(mighty_t2, text="Auto Regression", command= lambda : click_auto_regression(), width = button_width)
auto_regression.grid(column=0, row=0, sticky='W',padx = 22,pady =3)

def click_moving_average():
    #lags = int(tk.simpledialog.askstring('Lags', 'Enter the number of lags:'))
    lags = tk.simpledialog.askstring('Lags', 'Enter the number of lags:') # removed int

    if lags == None:# user clicked  cancel
        print('User clicked None')
    else:# user has input and clicked 'OK'
        print('Seas_diff lags',int(lags))
    print('User has input something lags=',lags)
    ...

moving_average = ttk.Button(mighty_t2, text="Moving Average", command= lambda : click_moving_average(), width = button_width)
moving_average.grid(column=0, row=1, sticky='W',padx = 22,pady =3)

def click_predictions():
    print('click_predictions')
    ...

predictions = ttk.Button(tab2, text="Predictions", command= lambda : click_predictions(), width = 15)
predictions.grid(column=0, row=3, sticky='W' + 'N' ,padx = 22,pady =2)


def click_reset_data():
    print('click_reset_data')
    ...

reset_data_ts = ttk.Button(tab2, text="Reset to Original Data", command= lambda : click_reset_data(), width = 25)
reset_data_ts.grid(column=0, row=4, sticky='W' + 'N',padx = 22,pady =2)



# Add big textbox for time series
text_h= 35
text_w = 90
textBox_t1 = tk.Text(mighty_t3, height = text_h, width = text_w,wrap=tk.WORD)
textBox_t1.grid(column=0, row=5, sticky=tk.N+tk.S)

#name_entered.focus()      # Place cursor into name Entry
#======================
# Start GUI
#======================
win.mainloop()
