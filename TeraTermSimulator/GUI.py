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
        self.geometry(f"{800}x{300}")

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
        
        self.serialCommsLabel = customtkinter.CTkLabel(self.serialCommsFrame, text="Device Type: ")
        self.serialCommsLabel.grid(row=1, column=0, columnspan=1, padx=10, pady=20, sticky="")
        self.serialCommsLabel2 = customtkinter.CTkLabel(self.serialCommsFrame, text="Sector: ")
        self.serialCommsLabel2.grid(row=2, column=0, columnspan=1, padx=10, pady=20, sticky="")
        self.serialCommsLabel3 = customtkinter.CTkLabel(self.serialCommsFrame, text="Sector State: ")
        self.serialCommsLabel3.grid(row=3, column=0, columnspan=1, padx=10, pady=20, sticky="")
        self.serialCommsLabel4 = customtkinter.CTkLabel(self.serialCommsFrame, text="Channels: ")
        self.serialCommsLabel4.grid(row=4, column=0, columnspan=1, padx=10, pady=20, sticky="")
      
       # TREE VIEW ADDED HERE
        self.treeview = ttk.Treeview(self, height=6)
        self.treeview.grid(row=0, column=1, columnspan=1, padx=(20, 0), pady=(50, 30), sticky="nsew")
        
       # self.exitButton = customtkinter.CTkButton(master=self, text="Exit", width=30, height=30, command = self.onExit, border_width=2, text_color=("gray10", "#DCE4EE"))
       # self.exitButton.grid(row=3, column=3, padx=(20, 20), pady=(10, 0), sticky="nsew")
        
       # create textbox
       # self.serialReceiveTextBox = customtkinter.CTkTextbox(self, width=250)
        #self.serialReceiveTextBox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # create tabview
        self.evenOptions = customtkinter.CTkTabview(self, width=250, height=100)
        self.evenOptions.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.evenOptions.add("Command Options")
        self.evenOptions.add("Trigger Fire")
        self.evenOptions.tab("Command Options").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.combobox_1 = customtkinter.CTkComboBox(self.evenOptions.tab("Command Options"),
                                                    values=["Set analogue for dev <n> channel <c> [to r]",
                                                            "Show analogue readings for device <n>", "Ramp analogue channel c from s to f"
                                                            "Scale analogue channel c", "Show device <n> config", "Dump eeprom of device <n>"
                                                            "Dump <y> bytes of serial flash from address <x>", "Show status of device n [to m]", "Show status of device n [to m] (shortform)"
                                                            "Write eeprom to device n", "Check eeprom checksums of device n [to m]"
                                                            "Show map", "wiring split/join <n><p>: Split/Join the wiring at L1/L2/Comm", "Apply an offset to the reply time for device n"
                                                            "Play analogue simulation to device n", "Add a new device", "Delete all devices"
                                                            "Change a device", "Open/Close Breaker n at device.", "Lose a device."
                                                            "Restore a device.", "Execute commands from file", "Load devices backup file (bin)"
                                                            "Save devices backup file (bin)", "Save devices config file/output (text)",
                                                            "Set debug level to n or save current to flash", "Set the time"])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.send_command_button = customtkinter.CTkButton(self.evenOptions.tab("Command Options"), text="Send Command",
                                                           command=self.comboBoxsendVariables)
        self.send_command_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        #self.string_input_button = customtkinter.CTkButton(self.evenOptions.tab("Command Options"), text="Enter Command Manually",
        #                                                   command=self.manualInputCommand)
        #self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))
        #self.clearTextBox = customtkinter.CTkButton(self.popupwindow.tab("Command Options"), text="Clear",
        #                                                   command=self.clearTextBox)
        #self.clearTextBox.grid(row=5, column=0, padx=20, pady=(10, 10))
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
        #self.uioptions_frame = customtkinter.ctkframe(self, width=250)
        #self.uioptions_frame.grid(row=1, column=3, padx=(20, 0), pady=(20, 0))
        self.combobox_1.set("command list")
        self.combobox_fire.set("fire list")

    ## COMMANDS FOR FUNCTIONS

    def showTextboxWindow(self):
        if not hasattr(self, 'textboxWindow'):
            self.textboxWindow = Toplevel(self)
            self.textboxWindow.title("Command Terminal")
            self.textboxWindow.geometry("450x325")

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
        if selected_command:
            selected_command = selected_command[:20]
        dialog = customtkinter.CTkInputDialog(text=selected_command, title="Send Selected Command")
        result = dialog.get_input()
        if result is not None:
            result = result + "\r\n"
            self.mySerial.write(result.encode())
            print("Result:", result)
            self.showTextboxWindow()
            self.serialReceiveTextBox.insert('end', self.mySerial.serialDataReceived.encode())
        else:
            print("Dialog was cancelled.")
            return
        
    def loadTree(self):            
        # Send "ds" command to the serial port
            self.mySerial.commandInProgress = True
            self.mySerial.write("ds\n\r".encode())
            threadCommand = threading.Thread(target=command_handler.treeViewHandler, args=(self, self.mySerial))
            threadCommand.start()
    
    def comboBoxsend2(self):
        selected_command = self.combobox_fire.get()
        if selected_command in ["Optical Fire", "MCP"]:
            if selected_command == "Optical Fire":
                self.mySerial.write("Optical Fire\r\n".encode())
            elif selected_command == "MCP":
                self.mySerial.write("MCP\r\n".encode())

            if not hasattr(self, 'textboxWindow'):
                self.showTextboxWindow()
        
            self.serialReceiveTextBox.insert('end', self.mySerial.serialDataReceived)
        else:
        # Create the dialog window
            dialog = Toplevel(self)
            dialog.title("Select option")

        # Create the CTkComboBox widget
            options = ["play 1 0", "Other"]
            playFireBtn = customtkinter.CTkComboBox(dialog, values=options, command=lambda: self.sendOption(playFireBtn.get(), dialog))
            playFireBtn.pack()
            btn_other = customtkinter.CTkButton(dialog, text="Start Fire", command=lambda: self.sendOption("Other", dialog))
            btn_other.pack()

        # Show the dialog window
            dialog.grab_set()
            dialog.focus_set()
            dialog.wait_window()

    def sendOption(self, option, dialog):
        if option == "Stop":
    # Close the serial port
            self.mySerial.close()
        else:
    # Open the serial port if it's not already open
            if not self.mySerial.is_open:
                self.mySerial.open()

    # Write to the serial port
            self.mySerial.write(option.encode())

            if not hasattr(self, 'textboxWindow'):
                self.showTextboxWindow()
    
            self.serialReceiveTextBox.insert('end', self.mySerial.serialDataReceived)

    # Close the dialog window
        dialog.destroy()


            
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
       
    def stopSerCommsEvent(self):
        # Deactivate the Stop button and activate the Start button and Exit button
        self.mySerial.closePort()
        #self.startButton.configure(state="normal")
        #self.stopButton.configure(state="disabled")
        #self.exitButton.configure(state="normal")

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
            self.startButton.configure(state="disabled")
            self.stopButton.configure(state="normal")
            #self.exitButton.configure(state="disabled")

            # Close the popup window
            top.destroy()
        else:
            tkinter.messagebox.showerror("Error", "Failed to open serial port.")
            
        # Display an error message to the user here, if desired.
        
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