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
    plt.legend((raw_plot, predict_plot),('Raw Data', 'Prediction equation = ' + equation_str),loc=(-0.05,-0.12), scatterpoints=1, ncol=3, fontsize=8)
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
mighty1.grid(column=1, row=0,sticky="E", padx=8, pady=4)

mighty2 = ttk.LabelFrame(tab1, text=' Non Linear Regression ')
mighty2.grid(column = 0, row=1, padx=8, pady=4)
#mighty2.grid_columnconfigure(0, weight=1)

# Add big textbox
text_h= 8
text_w = 30
textBox = tk.Text(mighty1, height = text_h, width = text_w,wrap=tk.WORD)
textBox.grid(column=0, row=5, sticky='E', columnspan=3)

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
    plt.scatter(X_log, Y_log,)
    plt.title('Scatter plot of log_y & log_x')					
    plt.xlabel('x_log')					
    plt.ylabel('y_log')					
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
# Add button to output basic statistics
Statistics = ttk.Button(mighty, text="Statistics", command= lambda : click_stats(textBox), width = 20)   
Statistics.grid(column=0, row=0, sticky='W')

# Modified Button Click Function
def click_me(): 
    action.configure(text='Hello ' + name.get() + ' ' + 
                     number_chosen.get())
# Add button for ANOVA
plot = ttk.Button(mighty, text="Plot", command=click_me, width = 20)   
plot.grid(column=0, row=1, sticky='W')


# Add button to Regression
linear_Regression = ttk.Button(mighty, text="Linear Regression", command=click_me,width = 20)   
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
        
    textBox.delete(1.0, tk.END)
    textBox.insert(tk.INSERT, equation_str)
    raw_plot = plt.scatter(X.values, Y.values, color = 'r')
    #plt.plot(X.values, round (coeff_list[0] + (coeff_list[1]*X.values) + (coeff_list[2]*(X.values**2))+ (coeff_list[3]*(X.values**3)), 4),'-')
    predict_plot = plt.plot(X.values, Y_predicted, '-')
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
# Add button for ANOVA
anova = ttk.Button(mighty, text="ANOVA", command=click_me,width = 20)   
anova.grid(column=0, row=4, sticky='W')
"""

# Modified Button Click Function
def click_me(): 
    action.configure(text='Hello ' + name.get() + ' ' + 
                     number_chosen.get())

# Adding a Textbox Entry widget
name = tk.StringVar()
name_entered = ttk.Entry(mighty, width=12, textvariable=name)
name_entered.grid(column=0, row=1, sticky='W')               # align left/West

# Adding a Button
action = ttk.Button(mighty, text="Click Me!", command=click_me)   
action.grid(column=2, row=1)                                

# Creating three checkbuttons
ttk.Label(mighty, text="Choose a number:").grid(column=1, row=0)
number = tk.StringVar()
number_chosen = ttk.Combobox(mighty, width=12, textvariable=number, state='readonly')
number_chosen['values'] = (1, 2, 4, 42, 100)
number_chosen.grid(column=1, row=1)
number_chosen.current(0)

chVarDis = tk.IntVar()
check1 = tk.Checkbutton(mighty, text="Disabled", variable=chVarDis, state='disabled')
check1.select()
check1.grid(column=0, row=4, sticky=tk.W)                   

chVarUn = tk.IntVar()
check2 = tk.Checkbutton(mighty, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W)                   

chVarEn = tk.IntVar()
check3 = tk.Checkbutton(mighty, text="Enabled", variable=chVarEn)
check3.deselect()
check3.grid(column=2, row=4, sticky=tk.W)                     

# GUI Callback function 
def checkCallback(*ignoredArgs):
    # only enable one checkbutton
    if chVarUn.get(): check3.configure(state='disabled')
    else:             check3.configure(state='normal')
    if chVarEn.get(): check2.configure(state='disabled')
    else:             check2.configure(state='normal') 

# trace the state of the two checkbuttons
chVarUn.trace('w', lambda unused0, unused1, unused2 : checkCallback())    
chVarEn.trace('w', lambda unused0, unused1, unused2 : checkCallback())   


# Using a scrolled Text control    
scrol_w  = 30
scrol_h  =  3
scr = scrolledtext.ScrolledText(mighty, width=scrol_w, height=scrol_h, wrap=tk.WORD)
scr.grid(column=0, row=5, sticky='WE', columnspan=3)                    


# First, we change our Radiobutton global variables into a list
colors = ["Blue", "Gold", "Red"]   

# We have also changed the callback function to be zero-based, using the list 
# instead of module-level global variables 
# Radiobutton Callback
def radCall():
    radSel=radVar.get()
    if   radSel == 0: win.configure(background=colors[0])  # zero-based
    elif radSel == 1: win.configure(background=colors[1])  # using list
    elif radSel == 2: win.configure(background=colors[2])

# create three Radiobuttons using one variable
radVar = tk.IntVar()

# Next we are selecting a non-existing index value for radVar
radVar.set(99)                                 
 
# Now we are creating all three Radiobutton widgets within one loop
for col in range(3):                             
    curRad = tk.Radiobutton(mighty, text=colors[col], variable=radVar, 
                            value=col, command=radCall)          
    curRad.grid(column=col, row=5, sticky=tk.W)             # row=5 ... SURPRISE!

# Create a container to hold labels
buttons_frame = ttk.LabelFrame(mighty, text=' Labels in a Frame ')
buttons_frame.grid(column=0, row=7)        
 
# Place labels into the container element
ttk.Label(buttons_frame, text="Label1").grid(column=0, row=0, sticky=tk.W)
ttk.Label(buttons_frame, text="Label2").grid(column=1, row=0, sticky=tk.W)
ttk.Label(buttons_frame, text="Label3").grid(column=2, row=0, sticky=tk.W)
"""

#name_entered.focus()      # Place cursor into name Entry
#======================
# Start GUI
#======================
win.mainloop()
