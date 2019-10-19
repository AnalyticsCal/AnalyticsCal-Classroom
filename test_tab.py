#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Text
from tkinter import filedialog as fd

import os

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
    database function has to be called here instead of the one in line 36
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
mighty1.grid(column=1, row=0, padx=8, pady=4)

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
    else:
        print('No Data :(')



# Modified Button statistics Function
def click_stats(textBox):
    global X,Y, data
    textBox.insert(tk.INSERT, 'x_bar ='+ str(X.mean())+'\n')
    textBox.insert(tk.INSERT, 'x_var ='+ str(X.var())+'\n')
    textBox.insert(tk.INSERT, 'y_bar ='+ str(Y.mean())+'\n')
    textBox.insert(tk.INSERT, 'y_var ='+ str(round(Y.var(), 4))+'\n')
    #textBox.insert(tk.INSERT, 'Cov(x, y) ='+ str(data.cov())+'\n')
    textBox.insert(tk.INSERT, 'Correlation coeeficient ='+ str(round(data.corr_coeff(), 4))+'\n')
    

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

# Modified Button Click Function
def click_nlr():
    global X,Y, data
    regression = nlr(X.values,Y.values)
    coefficient = regression.polynomial(int(number_chosen.get()))
    
    textBox.delete(1.0, tk.END)
    textBox.insert(tk.INSERT, str(coefficient))
    
# Add button for ANOVA
polynomial_regression = ttk.Button(mighty, text="Polynomial Regression", command=click_nlr)   
polynomial_regression.grid(column=0, row=3, sticky='W')

number = tk.StringVar()
number_chosen = ttk.Combobox(mighty, width=12, textvariable=number, state='readonly')
number_chosen['values'] = (1, 2, 3, 4,5, 6)
number_chosen.grid(column=1, row=3)
number_chosen.current(0)

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

name_entered.focus()      # Place cursor into name Entry
#======================
# Start GUI
#======================
win.mainloop()
