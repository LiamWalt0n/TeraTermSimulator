from turtle import circle
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
from serial import Serial, SerialException
import serial
import TeraTermSimulator
import serial_connection
from customtkinter import CTkCanvas
import tkinter.messagebox as msgbox

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self, serial):
        super().__init__()

        result = msgbox.showwarning("Warning", "Make sure you connect to the serial comms via the toolbar")
        if result == "ok":
       
            self.mySerial = serial

        # configure window
        self.title("Vigilon Loop Device Simulator Tool")
        self.geometry(f"{800}x{325}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create toolbar
        menu = Menu(self)
        item = Menu(menu)
        option = Menu(self)
        about = Menu(self)
        setup = Menu(self)
        item.add_command(label='Clear', command=self.clearTextBox)
        item.add_command(label='Build')
        setup.add_command(label='Serial Port', command=self.openSerialPortWindow)
        option.add_command(label='Show Textbox', command=self.showTextboxWindow)
        option.add_command(label='Import')
        option.add_command(label='Exit', command=self.onExit)
        menu.add_cascade(label='File', menu=item)
        menu.add_cascade(label='Options', menu=option)
        menu.add_cascade(label='Setup', menu=setup)
        menu.add_cascade(label='About', menu=about)
        about.add_command(label='About Device Simulator', command=self.aboutDeviceSimulator)
        self.config(menu=menu)

        self.addToRunningFlag = True
        
        self.config(menu=menu)

        ## create sidebar frame with widgets
        self.serialCommsFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.serialCommsFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.serialCommsFrame.grid_rowconfigure(6, weight=1)

        ## Add a new label for Device ID
        #self.serialCommsLabel0 = customtkinter.CTkLabel(self.serialCommsFrame, text="Device ID: ")
        #self.serialCommsLabel0.grid(row=0, column=0, columnspan=1, padx=10, pady=5, sticky="")
        #self.serialCommsLabelValue0 = customtkinter.CTkLabel(self.serialCommsFrame, text="")
        #self.serialCommsLabelValue0.grid(row=1, column=0, columnspan=1, padx=10, pady=5, sticky="")

        # Update the rest of the labels
        self.serialCommsLabel = customtkinter.CTkLabel(self.serialCommsFrame, text="Device Type: ")
        self.serialCommsLabel.grid(row=1, column=0, columnspan=1, padx=10, pady=20, sticky="")
        self.serialCommsLabelValue1 = customtkinter.CTkLabel(self.serialCommsFrame, text="")
        self.serialCommsLabelValue1.grid(row=3, column=0, columnspan=1, padx=10, pady=5, sticky="")

        self.serialCommsLabel2 = customtkinter.CTkLabel(self.serialCommsFrame, text="Sector: ")
        self.serialCommsLabel2.grid(row=2, column=0, columnspan=1, padx=10, pady=20, sticky="")
        self.serialCommsLabelValue2 = customtkinter.CTkLabel(self.serialCommsFrame, text="")
        self.serialCommsLabelValue2.grid(row=5, column=0, columnspan=1, padx=10, pady=5, sticky="")

        self.serialCommsLabel3 = customtkinter.CTkLabel(self.serialCommsFrame, text="Sector State: ")
        self.serialCommsLabel3.grid(row=3, column=0, columnspan=1, padx=10, pady=20, sticky="")
        self.serialCommsLabelValue3 = customtkinter.CTkLabel(self.serialCommsFrame, text="")
        self.serialCommsLabelValue3.grid(row=7, column=0, columnspan=1, padx=10, pady=5, sticky="")

        self.serialCommsLabel4 = customtkinter.CTkLabel(self.serialCommsFrame, text="Channels: ")
        self.serialCommsLabel4.grid(row=4, column=0, columnspan=1, padx=10, pady=20, sticky="")
        self.serialCommsLabelValue4 = customtkinter.CTkLabel(self.serialCommsFrame, text="")
        self.serialCommsLabelValue4.grid(row=9, column=0, columnspan=1, padx=10, pady=5, sticky="")

       # TREE VIEW ADDED HERE
        self.treeview = ttk.Treeview(self, height=6)
        self.treeview.grid(row=0, column=1, columnspan=1, padx=(20, 0), pady=(50, 30), sticky="nsew")
        #self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)
        

        # Add a vertical scrollbar to the treeview
        vscroll = ttk.Scrollbar(self.treeview, orient="vertical", command=self.treeview.yview)
        vscroll.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=vscroll.set)

        # create tabview
        self.evenOptions = customtkinter.CTkTabview(self, width=250, height=100)
        self.evenOptions.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.evenOptions.add("Command Options")
        self.evenOptions.add("Trigger Fire")
        self.evenOptions.tab("Command Options").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.combobox_1 = customtkinter.CTkComboBox(self.evenOptions.tab("Command Options"),
                                                    values = [
"Set analogue for dev",
"Show analogue readings for device",
"Ramp analogue channel",
"Scale analogue channel",
"Show device <n> config",
"Dump eeprom of device",
"Dump",
"Show status of device",
"Show status of device (shortform)",
"Write eeprom to device",
"Check eeprom checksums of device",
"Show map",
"wiring split/join",
"Apply an offset to the reply time for device",
"Play analogue simulation to device",
"Add a new device",
"Delete all devices",
"Change a device",
"Open/Close Breaker",
"Lose a device",
"Restore a device",
"Execute commands from file",
"Load devices backup file",
"Save devices backup file",
"Save devices config file/output",
"Set debug level to n or save current to flash",
"Set the time"
])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.send_command_button = customtkinter.CTkButton(self.evenOptions.tab("Command Options"), text="Send Command",
                                                           command=self.comboBoxsendVariables)
        self.send_command_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.loadTreeBtn = customtkinter.CTkButton(self.evenOptions.tab("Command Options"), text="Load Tree", command=self.loadTree)
        self.loadTreeBtn.grid(row=4, column=0, padx=20, pady=(10, 10))
        
      # Trigger Fire Tab Options
        self.evenOptions.tab("Trigger Fire").grid_columnconfigure(0, weight=1)
        self.evenOptions.tab("Trigger Fire").grid_rowconfigure(0, weight=0)
        self.evenOptions.tab("Trigger Fire").grid_rowconfigure(1, weight=0)
        self.evenOptions.tab("Trigger Fire").grid_rowconfigure(2, weight=0)
        self.evenOptions.tab("Trigger Fire").grid_rowconfigure(3, weight=0)

        self.combobox_fire = customtkinter.CTkComboBox(self.evenOptions.tab("Trigger Fire"),
                                            values=["Real Fire","Optical Fire", "MCP"])
        self.combobox_fire.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.send_command_button1 = customtkinter.CTkButton(self.evenOptions.tab("Trigger Fire"), text="Send Command",
                                                   command=self.comboBoxsend2)
        self.send_command_button1.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        self.clearTextBox1 = customtkinter.CTkButton(self.evenOptions.tab("Trigger Fire"), text="Stop Fire",
                                                           command=self.stopFire)
        self.clearTextBox1.grid(row=3, column=0, padx=20, pady=(10, 10))
       
      # create uioptions frame
        self.combobox_1.set("command list")
        self.combobox_fire.set("fire list")

    #def on_treeview_select(self, event):
    #    selected_item = self.treeview.selection()  # Get the currently selected item
    #    print(f"Selected item: {selected_item}")

    #    if selected_item:
    #        item_text = self.treeview.item(selected_item, "text")
    #        print(f"Item text: {item_text}")

    #        if " " in item_text:
    #            device_type = item_text.split(" ")[0]
    #            device_data = item_text.split(" ")[1]

    #            # Update Device Type label
    #            self.serialCommsLabelValue0["text"] = f"{device_type} {device_data}"
    #            children = self.treeview.get_children(selected_item)  # Get the children of the selected item
    #    if children:
    #        for child in children:
    #            child_text = self.treeview.item(child, "text")
    #            print(f"Child text: {child_text}")
    #            if "Sector: " in child_text:
    #                self.serialCommsLabelValue1["text"] = child_text.split("Sector: ")[1]
    #            elif "Sector State: " in child_text:
    #                self.serialCommsLabelValue2["text"] = child_text.split("Sector State: ")[1]
    #            elif "Channels: " in child_text:
    #                self.serialCommsLabelValue3["text"] = child_text.split("Channels: ")[1]
    #            else:
    #                self.serialCommsLabelValue1["text"] = ""
    #                self.serialCommsLabelValue2["text"] = ""
    #                self.serialCommsLabelValue3["text"] = ""
    #        else:
    #            self.serialCommsLabelValue0["text"] = ""
    #            self.serialCommsLabelValue1["text"] = ""
    #            self.serialCommsLabelValue2["text"] = ""
    #            self.serialCommsLabelValue3["text"] = ""



    def showTextboxWindow(self):
        if not hasattr(self, 'textboxWindow'):
            self.textboxWindow = Toplevel(self)
            self.textboxWindow.title("Command Terminal")
            self.textboxWindow.geometry("450x425")

            self.serialReceiveTextBox = customtkinter.CTkTextbox(self.textboxWindow, width=400, height=300)
            self.serialReceiveTextBox.pack()
            clearTextboxBtn = customtkinter.CTkButton(self.textboxWindow, text="Clear", command=self.clearTextBox)
            closeTextboxBtn = customtkinter.CTkButton(self.textboxWindow, text="Close", command=self.closeTextboxWindow)

            clearTextboxBtn.pack(side='left', padx=5)
            closeTextboxBtn.pack(side='right', padx=5)

    def closeTextboxWindow(self):
        self.textboxWindow.destroy()
        delattr(self, 'textboxWindow')

    def comboBoxsendVariables(self):
        selected_command = self.combobox_1.get()
        print("Selected Command:", selected_command)
        if selected_command:
            selected_command = selected_command[:30]
        # Create a dictionary to map each command to its corresponding entry
        command_entries = {
            "Set analogue for dev": "an <n> <c> [r]",
            "Show analogue readings for device": "ar <n>",
            "Ramp analogue channel": "ramp <n> <c> <s> <f> <d>",
            "Scale analogue channel": "scale <n> <c> <s>",
            "Show device <n> config": "dc <n>",
            "Dump eeprom of device": "de <n>",
            "Dump": "df <x> <y>",
            "Show status of device": "dd <n> [m]",
            "Show status of device (shortform)": "ds <n> [m]",
            "Write eeprom to device": "we <n> <x> <y...>",
            "Check eeprom checksums of device": "ce <n> [m]",
            "Show map": "map",
            "wiring split/join": "wiring split/join <n><p>",
            "Apply an offset to the reply time for device": "reply <n> <o>",
            "Play analogue simulation to device": "play <n> <num/file/stop>",
            "Add a new device": "device add",
            "Delete all devices": "device delete all",
            "Change a device": "device <n>",
            "Open/Close Breaker": "breaker <o/c> <n> <dev>",
            "Lose a device": "lose <n>",
            "Restore a device": "restore <n>",
            "Execute commands from file": "exec <file>",
            "Load devices backup file": "load backup <file>",
            "Save devices backup file": "save backup <file>",
            "Save devices config file/output": "save config <file/->",
            "Set debug level to n or save current to flash": "debug n/save",
            "Set the time": "time [hh:mm:ss dd/mm/yy]"
        }

        # Get the corresponding entry for the selected command
        entry = command_entries.get(selected_command, "")
        print("Entry:", entry)
        dialog = customtkinter.CTkInputDialog(text=entry, title="Send Selected Command")
        result = dialog.get_input()
        if result is None:
            print("Dialog was cancelled.")
            return
        result = result + "\r\n"
        self.mySerial.write(result.encode())
        print("Result:", result)

        try:
            self.showTextboxWindow()
            self.serialReceiveTextBox.insert('end', self.mySerial.serialDataReceived.encode())
        except tkinter.TclError:
            # Handle the error by displaying a message to the user
            print("Error:Textbox has been closed.")
            
    def loadTree(self):            
        # Send "ds" command to the serial port
            self.mySerial.commandInProgress = True
            self.mySerial.write("ds\n\r".encode())
            threadCommand = threading.Thread(target=command_handler.treeViewHandler, args=(self, self.mySerial))
            threadCommand.start()
    
    def comboBoxsend2(self):
        selected_text = self.combobox_fire.get()
        selected_item = self.treeview.selection()

        if selected_text in ["Optical Fire", "MCP"]:
            if selected_text == "Optical Fire":
                self.mySerial.write("an 1 1 60\r\n".encode())
            elif selected_text == "MCP":
                self.mySerial.write("an 1 6 MCPFIRE\r\n".encode())
                #The 2 above are whats sent - need to make the device dynamic in MCP so an [value] 6 MCP
                #Optical is device, channel then 60 - so make the deivce dynamic so an [value] 1 60
            if not hasattr(self, 'textboxWindow'):
                self.showTextboxWindow()

            self.serialReceiveTextBox.insert('end', self.mySerial.serialDataReceived)
        else:
            if selected_item:
                item_id = self.treeview.item(selected_item)["text"]
                if item_id.split(" ")[0].isdigit():
                    item_id = int(item_id.split(" ")[0])
                    selected_command = "play " + str(item_id) + " 0\r\n"
                    self.mySerial.write(selected_command.encode())
                    print("Result:", selected_command)
                    self.showTextboxWindow()
                    self.serialReceiveTextBox.insert('end', self.mySerial.serialDataReceived.encode())
                else:
                    print("Selected item does not contain a valid integer.")
            else:
                # Create the dialog window
                dialog = Toplevel(self)
                dialog.title("Select option")
                # Create the CTkComboBox widget
                options = ["Heat 1 Deg", "Heat 3 Deg", "Heat 5 Deg", "Heat 10 Deg", "Heat 20 Deg", "Heat 30 Deg", 
                           "TS1 Fire", "TS2 Fire", "TS3 Fire", "TS4 Fire", "TS5 Fire", "TS6 Fire", "TS7 Fire","TS8 Fire"]
                playFireBtn = customtkinter.CTkComboBox(dialog, values=options, command=lambda: self.sendOption(playFireBtn.get(), dialog))
                playFireBtn.pack()
                btn_other = customtkinter.CTkButton(dialog, text="Start Fire", command=lambda: self.sendOption(playFireBtn.get(), dialog))
                btn_other.pack()

    def sendOption(self, selected_text, dialog):
        if not hasattr(self, 'command_mapping'):
            error_message = "Please load the list of devices and select a device."
            messagebox.showerror("Error", error_message)
            return

        selected_command = self.command_mapping.get(selected_text, None)
        if selected_command:
            result = selected_command + "\r\n"
            self.mySerial.write(result.encode())
            print("Result:", result)
            self.showTextboxWindow()
            self.serialReceiveTextBox.insert('end', self.mySerial.serialDataReceived.encode())
            dialog.destroy()
        else:
            print("Selected text not found in command mapping.")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
       
    def stopSerCommsEvent(self):
        # Deactivate the Stop button and activate the Start button and Exit button
        self.mySerial.closePort()
      
    def openSerialPortWindow(self):
        # Create a new window
        top = tkinter.Toplevel(self)
        top.title("Serial Port Selection")

        # Create the label
        self.serialCommsLabel = customtkinter.CTkLabel(top, text="Serial Comms Connection")
        self.serialCommsLabel.grid(row=5, column=0, columnspan=1, padx=10, pady=10, sticky="")

        # Create the comportCombo combobox
        self.comportCombo = customtkinter.CTkComboBox(top, 
                                                    values=[port.device for port in serial.tools.list_ports.comports()])
        self.comportCombo.grid(row=6, column=0, pady=10, padx=20, sticky="n")

        # Create the baudrateCombo combobox
        self.baudrateCombo = customtkinter.CTkComboBox(top,
                                                    values=["115200"])
        self.baudrateCombo.grid(row=7, column=0, pady=10, padx=20, sticky="n")

        # Create the start button
        self.startButton = customtkinter.CTkButton(top, text="Start", command=lambda: self.startSerCommsEvent(top))
        self.startButton.grid(row=8, column=0, pady=10, padx=20, sticky="n")
        self.stopButton = customtkinter.CTkButton(top, text="Stop", command=self.stopSerCommsEvent)
        self.stopButton.grid(row=9, column=0, pady=10, padx=20, sticky="n")

    def startSerCommsEvent(self, top):
        global serial_is_open, ser, thread              
        selected_port = self.comportCombo.get() 
        if self.mySerial.openPort(selected_port):
            TeraTermSimulator.startThreads(self.mySerial, self)
            print("Serial communication started.")
            # Close the popup window
            top.destroy()
        else:
            tkinter.messagebox.showerror("Error", "Failed to open serial port.")

    def stopFire(self):
        self.mySerial.write("play stop\r\n".encode())
     
    def send_command_event(self):
        print("Command Sent")

    def aboutDeviceSimulator(self):
        dialog = tkinter.messagebox.showinfo(title="Loop Device Simulator", message="This is a loop device simulator that can be used to trigger events")

    def open_file_event(self):
        # return filedialog.askopenfilename() // This is to open a file
        self.destroy()

    def onExit(self):
        global running
        running = True
        if running:
            response = messagebox.askyesno("Confirmation", "The application is currently running. Are you sure you want to exit?")
            if response:
                self.destroy()

    def retrieveDevices(self):
          while True:
            data = ser.readline().decode().strip()
            if data:
                devices = data.split(',')
            for device in devices:
                self.treeview.insert('', 'end', text=device)

    def clearTextBox(self):
        if hasattr(self, 'serialReceiveTextBox'):
            self.serialReceiveTextBox.delete('1.0', END)

    def updateTextBox(self, someText):
        self.serialReceiveTextBox += someText

    def update_clear_button(self):
        if self.serialReceiveTextBox.get('1.0', 'end-1c') == '':
            self.clearTextBox.config(state="disabled")
        else:
            self.clearTextBox.config(state="normal")

    def AddToRunningTextBox(self, textToDisplay):
        if self.addToRunningFlag == True:
            if hasattr(self, 'textboxWindow'):
                self.showTextboxWindow()
                self.serialReceiveTextBox.insert('end', textToDisplay)
                
    def manageRunningTextBox(self, addFlag):
        self.addToRunningFlag = addFlag
        print(self.addToRunningFlag)