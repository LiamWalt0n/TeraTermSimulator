import time
import serial_connection
import GUI
import customtkinter
import command_handler
import tkinter
from tkinter import Menu, Tk, ttk
from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import tkinter.messagebox
import customtkinter
import threading
from logging import root
import threading
import time
import GUI
import serial_connection
import serial
import serial.tools.list_ports


def treeViewHandler(GUI, mySerial):
    mySerial.commandDataReceived = ""
    time.sleep(2)
    mySerial.commandInProgress = False
    print(mySerial.commandDataReceived)

    #if not GUI.treeview.get_children():
    #    GUI.treeview.insert('', 'end', text='dummy')
    count = 1
    lala = mySerial.commandDataReceived.splitlines()
    for anEntry in lala:
        hehe = anEntry.split(",")
        if len(hehe) >= 4:
            hehe2 = hehe[0] + " " + hehe[4] + '\n'
            hehe3 = GUI.treeview.insert('','end', count, text=hehe2)
            count += 1
            GUI.treeview.insert(hehe3,'end', count, text="Nick was ere")
            count += 1
            # gui  add to textbox & textboxtreeview 
            print(hehe[4])
    time.sleep(2)



