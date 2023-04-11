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


def treeViewHandler(GUI, mySerial):
    GUI.loading_label = tk.Label(GUI, text="Loading...")
    GUI.loading_label.grid(row=0, column=1, padx=(20, 0), pady=(50, 30), sticky="nsew")
    GUI.loading_label.lift()
    GUI.update()
    # Set the command data received flag to an empty string and wait for 2 seconds
    mySerial.commandDataReceived = ""
    time.sleep(2)
    # Set the command in progress flag to False and print the command data received
    mySerial.commandInProgress = False
    print(mySerial.commandDataReceived)

    # Delete all items in the treeview
    GUI.treeview.delete(*GUI.treeview.get_children())

    # Initialize a counter
    count = 1

    # Split the command data received by newline character
    command_data_lines = mySerial.commandDataReceived.splitlines()

    GUI.send_command_button.configure(state="disabled")
    GUI.loadTreeBtn.configure(state="disabled")
    GUI.send_command_button1.configure(state="disabled")
    GUI.clearTextBox1.configure(state="disabled")

    # Loop through each entry in the command data received
    for command_line in command_data_lines:
        GUI.manageRunningTextBox(False)
        # Split each entry by comma character
        entry_fields = command_line.split(",")
        # If there are at least 4 elements in the entry
        if len(entry_fields) >= 4:
            # Create a new string by combining the first and fifth elements
            entry_text = entry_fields[0] + " " + entry_fields[4] + '\n'

            # Insert a new item in the tree view with the new string and increment the counter
            parent_id = GUI.treeview.insert('', 'end', count, text=entry_text)
            count += 1
            
            #Function in serial_connection
            mySerial.commandDataReceived = ""
            mySerial.commandInProgress = True
          
            input_str = "dd " +  entry_fields[0] + "\r\n"
            mySerial.write(input_str.encode())
            time.sleep(0.25)
            
            # Repeat Below
            position = mySerial.commandDataReceived.find("2nd:")

            sector = mySerial.commandDataReceived[position+4:position+7]
  
            
            # Insert a new child item under the current item and increment the counter
            child_id = GUI.treeview.insert(parent_id, 'end', count, text="Sector: "+sector)
            count += 1

            # Print the fifth element
            print(entry_fields[4])

            # Repeat Below
            position = mySerial.commandDataReceived.find("Anal:")

            anal = mySerial.commandDataReceived[position+5:position+9]
  
            
            # Insert a new child item under the current item and increment the counter
            child_id = GUI.treeview.insert(parent_id, 'end', count, text="Channels: "+anal)
            count += 1

            # Print the fifth element
            print(entry_fields[4])

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
            
            child_id = GUI.treeview.insert(parent_id, 'end', count, text="Sector State: " + str(dSectorState))
            count +=1
            print(dSectorState)
            
    GUI.manageRunningTextBox(True)

    GUI.loading_label.destroy()

     # Disable buttons
    GUI.send_command_button.configure(state="normal")
    GUI.loadTreeBtn.configure(state="normal")
    GUI.send_command_button1.configure(state="normal")
    GUI.clearTextBox1.configure(state="normal")
    # Wait for 2 seconds
    time.sleep(2)

     
