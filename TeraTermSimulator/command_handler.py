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
import tkinter as tk
import helperClasses

def treeViewHandler(GUI, mySerial):
    GUI.arraylist = []
    GUI.loading_label = tk.Label(GUI, text="Loading...")
    GUI.loading_label.grid(row=0, column=1, padx=(20, 0), pady=(50, 30), sticky="nsew")
    GUI.loading_label.lift()
    GUI.update()
    
    mySerial.commandDataReceived = ""
    time.sleep(2)
    
    mySerial.commandInProgress = False
    print(mySerial.commandDataReceived)

    GUI.treeview.delete(*GUI.treeview.get_children())

    count = 1
    child_data_list = []
    child_data_counter = 0  # Add this line

    command_data_lines = mySerial.commandDataReceived.splitlines()

    GUI.send_command_button.configure(state="disabled")
    GUI.loadTreeBtn.configure(state="disabled")
    GUI.send_command_button1.configure(state="disabled")
    GUI.clearTextBox1.configure(state="disabled")

    for command_line in command_data_lines:
        GUI.manageRunningTextBox(False)
        
        entry_fields = command_line.split(",")
        
        if len(entry_fields) >= 4:
            entry_text = entry_fields[0] + " " + entry_fields[4] + '\n'

            parent_id = GUI.treeview.insert('', 'end', count, text=entry_text)
            count += 1
            
            mySerial.commandDataReceived = ""
            mySerial.commandInProgress = True
          
            input_str = "dd " +  entry_fields[0] + "\r\n"
            mySerial.write(input_str.encode())
            time.sleep(0.25)
            
            position = mySerial.commandDataReceived.find("2nd:")
            sector = mySerial.commandDataReceived[position+4:position+7]
            child_id = GUI.treeview.insert(parent_id, 'end', count, text="Sector: "+sector)
            count += 1

            position = mySerial.commandDataReceived.find("Anal:")
            anal = mySerial.commandDataReceived[position+5:position+9]
            child_id = GUI.treeview.insert(parent_id, 'end', count, text="Channels: "+anal)
            count += 1

            dSectorState = mySerial.commandDataReceived[26]

            try:
                dSectorState = int(mySerial.commandDataReceived[26])
            except ValueError:
                dSectorState = ""

            if dSectorState == 0:
                dSectorState = "N/A"
            elif dSectorState == 250:
                dSectorState = "Off"
            elif dSectorState == 251:
                dSectorState = 1
            elif dSectorState == 252:
                dSectorState = 2
            elif dSectorState == 253:
                dSectorState = 3
            elif dSectorState == 254:
                dSectorState = 4

            child_data_list.append({'child_id': child_data_counter, 'sector': sector, 'anal': anal, 'sector_state': dSectorState})  # Update this line
            print(f"Added sector state {dSectorState} to child_data_list, current list length: {len(child_data_list)}")
            child_data_counter += 1  # Add this line

            child_id = GUI.treeview.insert(parent_id, 'end', count, text="Sector State: " + str(dSectorState))
            count +=1

    GUI.manageRunningTextBox(True)

    GUI.loading_label.destroy()

    child_list = {
        'entry_text': entry_text,
        'child_data_list': child_data_list
    }
    GUI.arraylist.append(child_list)

    GUI.send_command_button.configure(state="normal")
    GUI.loadTreeBtn.configure(state="normal")
    GUI.send_command_button1.configure(state="normal")
    GUI.clearTextBox1.configure(state="normal")

    # Wait for 2 seconds
    time.sleep(2)

    print(GUI.arraylist)

     
