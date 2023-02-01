#from curses.textpad import Textbox
#from curses.textpad import Textbox
from logging import root
import threading
import time
import tkinter
from tkinter import Menu, Tk, ttk
from tkinter import filedialog
from tkinter import *
import tkinter.messagebox
import customtkinter
import serial


try:
  ser = serial.Serial(
    port='COM9',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
  )
  ser.isOpen() # try to open port, if possible print message and proceed with 'while True:'

  #ser.write("help") # The idea is to send command - this is an example
  print ("port is opened!")

except IOError: # if port is already opened, close it and open it again and print message
  ser.close()
  ser.open()
  print ("port was already open, was closed and opened again!")

##while True: # do something...


def handle_data(data):
    print(data)
    
    

def read_from_port(ser, anApp):

        while True:
          # print("test")
          # print(textbox1.insert)
           reading = ser.readline().decode()
           handle_data(reading)
           anApp.textbox1.insert(0.1, reading)

         


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        
        # configure window
        self.title("Simulator")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create toolbar
        menu = Menu(self)
        item = Menu(menu)
        option = Menu(self)
        about = Menu(self)
        item.add_command(label='Clear')
        item.add_command(label='Build')
        option.add_command(label='Import')
        option.add_command(label='Exit', command=self.onExit())
        menu.add_cascade(label='File', menu=item)
        menu.add_cascade(label='Options', menu=option)
        menu.add_cascade(label='About', menu=about)
        about.add_command(label='About Device Simulator', command=self.about_device_simulator)
        
        self.config(menu=menu)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Start Comms Connection", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Start", command=self.startSerCommsEvent)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stop", command=self.stopSerCommsEvent)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

       # TREE VIEW ADDED HERE
        self.treeview = ttk.Treeview(self, height=6, show="tree")
        self.treeview.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(50, 50), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Exit", command = self.open_file_event, border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

       # create textbox
        self.textbox1 = customtkinter.CTkTextbox(self, width=250)
        self.textbox1.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Command Options")
        self.tabview.add("Trigger Fire")
        self.tabview.tab("Command Options").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Command Options"),
                                                    values=["an <n> <c> [r]          : Set analogue for dev <n> channel <c> [to r]",
                                                            "ar <n>                  : Show analogue readings for device <n>", "ramp <n> <c> <s> <f> <d>: Ramp analogue channel c from s to f"
                                                            "scale <n> <c> <s>       : Scale analogue channel c", "dc <n>                  : Show device <n> config", "de <n>                  : Dump eeprom of device <n>"
                                                            "df <x> <y>              : Dump <y> bytes of serial flash from address <x>", "dd <n> [m]              : Show status of device n [to m]", "ds <n> [m]              : Show status of device n [to m] (shortform)"
                                                            "we <n> <x> <y...>       : Write eeprom to device n", "ce <n> [m]              : Check eeprom checksums of device n [to m]"
                                                            "map                     : Show map", "wiring split/join <n><p>: Split/Join the wiring at L1/L2/Comm", "reply <n> <o>           : Apply an offset to the reply time for device n"
                                                            "play <n> <num/file/stop>: Play analogue simulation to device n", "device add              : Add a new device", "device delete all       : Delete all devices"
                                                            "device <n>              : Change a device", "breaker <o/c> <n> <dev> : Open/Close Breaker n at device.", "lose <n>                : Lose a device."
                                                            "restore <n>             : Restore a device.", "exec <file>             : Execute commands from file", "load backup <file>      : Load devices backup file (bin)"
                                                            "save backup <file>      : Save devices backup file (bin)", "save config <file/->    : Save devices config file/output (text)",
                                                            "debug n/save            : Set debug level to n or save current to flash", "time [hh:mm:ss dd/mm/yy]: Set the time", "Play 1 0\n\r", "help\n\r"])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Command Options"), text="Enter Command Manually",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.send_command_button = customtkinter.CTkButton(self.tabview.tab("Command Options"), text="Send Command",
                                                           command=self.comboBoxsend1)
        self.send_command_button.grid(row=3, column=0, padx=20, pady=(10, 10))
     
        # Trigger Fire Tab Options
        self.combobox_fire = customtkinter.CTkComboBox(self.tabview.tab("Trigger Fire"),
                                                    values=["help\n\r"])
        self.combobox_fire.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.send_command_button1 = customtkinter.CTkButton(self.tabview.tab("Trigger Fire"), text="Send Command",
                                                           command=self.comboBoxsend2)
        self.send_command_button1.grid(row=3, column=0, padx=20, pady=(10, 10))




        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Serial Comms Connection")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.combobox_2 = customtkinter.CTkComboBox(master=self.radiobutton_frame,
                                                    values=["COM 8", "COM 9"])
        self.combobox_2.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.combobox_3 = customtkinter.CTkComboBox(master=self.radiobutton_frame,
                                                    values=["115200", "9900"])
        self.combobox_3.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.combobox_4 = customtkinter.CTkComboBox(master=self.radiobutton_frame,
                                                    values=["Eight Bits"])
        self.combobox_4.grid(row=3, column=2, pady=10, padx=20, sticky="n")
       
        
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.combobox_1.set("Command List")
        self.combobox_fire.set("Trigger Fire")

        thread = threading.Thread(target=read_from_port, args=(ser,self))
        thread.start()



    # COMMANDS FOR FUNCTIONS

    def comboBoxsend1(self):
       command_option = self.combobox_1.get()
       ser.write(command_option.encode())

    def comboBoxsend2(self):
        command_option_2 = self.combobox_fire.get()
        ser.write(command_option_2.encode())

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a command or select from the list:", title="CTkInputDialog")
        print("Command Entered:",dialog.get_input())
        #ser.write(dialog.get_input.encode())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def startSerCommsEvent(self):
        print("Start Selected")

    def stopSerCommsEvent(self):
        print("Stop Selected")
     
    def send_command_event(self):
        print("Command Sent")

    def about_device_simulator(self):
        dialog = customtkinter.CTkInputDialog(text="Test", title="About Device Simulator")

    def open_file_event(self):
        # return filedialog.askopenfilename() // This is to open a file
        self.destroy()

    def onExit(self):
        self.quit()

    def handleIncomingText(self, reading):
        self.textbox1.insert(reading)

    def handle_data(data):
        print(data)
    
    

    def read_from_port(ser, anApp):

        while True:
          # print("test")
          # print(textbox1.insert)
           reading = ser.readline().decode()
           anApp.handleIncomingText(reading)
           handle_data(reading)
           
        


if __name__ == "__main__":
    app = App()
    app.mainloop()