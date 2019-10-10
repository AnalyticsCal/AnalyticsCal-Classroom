#Importing Libraries
from tkinter import *
from tkinter.ttk import *

#Initializing File Upload
from tkinter.filedialog import askopenfile
root = Tk()
root.geometry('200x100')

#Defination
def open_file():
    file = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
    if file is not None:
        content = file.read()
        print(content)

#Button
btn = Button(root, text='Open', command=lambda: open_file())
btn.pack(side=TOP, pady=10)

mainloop()
