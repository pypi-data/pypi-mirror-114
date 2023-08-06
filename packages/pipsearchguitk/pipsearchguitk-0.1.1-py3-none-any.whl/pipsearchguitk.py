import tkinter as tk 
from tkinter import ttk

from tkinter import *

import subprocess
import sys

import time

def pipsearchguitk():
    root = tk.Tk()
    root.title('Pip package search')
    root.geometry('600x200')
    root.resizable(0,0)


    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0].upper() for r in reqs.split()]

    def hide_label():
        notif.config(text="")


    def search_package():
        i_name = name.get().upper()

        if str(i_name) in installed_packages:
            notif.config(fg="green",text="Package available")
            notif.after(3000,hide_label)
        elif len(i_name) == 0:
            notif.config(fg="red",text="Type in something bitch")
            notif.after(3000,hide_label)
        else:
            notif.config(fg="red",text="Package unavailble")
            notif.after(3000,hide_label)


    name = StringVar()

    #Labels
    pkg_name = Label(root,text="Enter the package name: ",bg="#E8D579")
    pkg_name.grid(row=1,column=0,pady=10,padx=10)

    #entry
    pkg_name_entry_box = Entry(root, textvariable = name, exportselection = 2, width = 40 , bg = "lightgreen")
    pkg_name_entry_box.grid(row=1,column=1,pady=10,padx=10)

    #Search
    pkg_search_btn = Button(root, text="Search",command=search_package,width=20,bg="#05E8E0")
    pkg_search_btn.grid(row=2,column=0,pady=10,padx=10) 

    notif = Label(root, font = ('Calibri',12))
    notif.grid(row=6,sticky=N)


    root.mainloop()

pipsearchguitk()