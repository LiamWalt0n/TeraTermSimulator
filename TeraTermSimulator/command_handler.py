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

    # Loop through each entry in the command data received
    for command_line in command_data_lines:
        # Split each entry by comma character
        entry_fields = command_line.split(",")
        # If there are at least 4 elements in the entry
        if len(entry_fields) >= 4:
            # Create a new string by combining the first and fifth elements
            entry_text = entry_fields[0] + " " + entry_fields[4] + '\n'
            # Insert a new item in the tree view with the new string and increment the counter
            parent_id = GUI.treeview.insert('', 'end', count, text=entry_text)
            count += 1
            # Insert a new child item under the current item and increment the counter
            child_id = GUI.treeview.insert(parent_id, 'end', count, text="Test")
            count += 1
            # Print the fifth element
            print(entry_fields[4])

    # Wait for 2 seconds
    time.sleep(2)





