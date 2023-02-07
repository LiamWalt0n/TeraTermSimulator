#from curses.textpad import Textbox
#from curses.textpad import Textbox
from logging import root
import threading
import time
import tkinter
from tkinter import Menu, Tk, ttk
from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
import tkinter.messagebox
import customtkinter
import serial
import serial.tools.list_ports



def select_port():
  ports = [comport.device for comport in serial.tools.list_ports.comports()]
  return ports[0] # select the first available port, or let the user select a port from the list

port = select_port()
ser = serial.Serial(
    port=port,
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)
ser.isOpen() # try to open port, if possible print message and proceed with 'while True:'

print(f"port {port} is opened!")

def handle_data(data):
    print(data)

def read_from_port(ser, anApp):
    while True:
        reading = ser.readline().decode()
        handle_data(reading)
        anApp.textbox1.insert(0.1, reading)


customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
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
        item.add_command(label='Clear', command=self.clearTextBox)
        item.add_command(label='Build')
        option.add_command(label='Import')
        option.add_command(label='Exit', command=self.onExit())
        menu.add_cascade(label='File', menu=item)
        menu.add_cascade(label='Options', menu=option)
        menu.add_cascade(label='About', menu=about)
        about.add_command(label='About Device Simulator', command=self.aboutDeviceSimulator)
        
        self.config(menu=menu)

        # create sidebar frame with widgets
        self.serialCommsFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.serialCommsFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.serialCommsFrame.grid_rowconfigure(4, weight=1)
        self.startComsLabel = customtkinter.CTkLabel(self.serialCommsFrame, text="Start Comms Connection", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.startComsLabel.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.serialCommsFrame, text="Start")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.serialCommsFrame, text="Stop", command=self.stopSerCommsEvent)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        ports = [comport.device for comport in serial.tools.list_ports.comports()]

        
        self.label_radio_group = customtkinter.CTkLabel(self.serialCommsFrame, text="Serial Comms Connection")
        self.label_radio_group.grid(row=5, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.comportCombo = customtkinter.CTkComboBox(self.serialCommsFrame, 
                                                    values=ports)
        self.comportCombo.grid(row=6, column=0, pady=10, padx=20, sticky="n")
        self.baudrateCombo = customtkinter.CTkComboBox(self.serialCommsFrame,
                                                    values=["115200"])
        self.baudrateCombo.grid(row=7, column=0, pady=10, padx=20, sticky="n")
        

       # TREE VIEW ADDED HERE
        self.treeview = ttk.Treeview(self, height=6, show="tree")
        self.treeview.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(50, 50), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Exit", command = self.open_file_event, border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

       # create textbox
        self.textbox1 = customtkinter.CTkTextbox(self, width=250)
        self.textbox1.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        

        # create tabview
        self.evenOptions = customtkinter.CTkTabview(self, width=250)
        self.evenOptions.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.evenOptions.add("Command Options")
        self.evenOptions.add("Trigger Fire")
        self.evenOptions.tab("Command Options").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        
        self.combobox_1 = customtkinter.CTkComboBox(self.evenOptions.tab("Command Options"),
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
                                                            "debug n/save            : Set debug level to n or save current to flash", "time [hh:mm:ss dd/mm/yy]: Set the time"])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.evenOptions.tab("Command Options"), text="Enter Command Manually",
                                                           command=self.manualInputCommand)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.send_command_button = customtkinter.CTkButton(self.evenOptions.tab("Command Options"), text="Send Command",
                                                           command=self.comboBoxsendVariables)
        self.send_command_button.grid(row=3, column=0, padx=20, pady=(10, 10))
     
        # Trigger Fire Tab Options
        self.combobox_fire = customtkinter.CTkComboBox(self.evenOptions.tab("Trigger Fire"),
                                                    values=["help\n\r","Play 1 0\n\r"])
        self.combobox_fire.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.send_command_button1 = customtkinter.CTkButton(self.evenOptions.tab("Trigger Fire"), text="Send Command",
                                                           command=self.comboBoxsend2)
        self.send_command_button1.grid(row=3, column=0, padx=20, pady=(10, 10))




        # create uiOptions frame
        self.uiOptions_frame = customtkinter.CTkFrame(self, width=250)
        self.uiOptions_frame.grid(row=1, column=3, padx=(20, 0), pady=(20, 0))

        #self.appearance_mode_label = customtkinter.CTkLabel(self.uiOptions_frame, text="Appearance Mode:", anchor="w")
        #self.appearance_mode_label.grid(row=0, column=2, padx=20, pady=(10, 0))
        #self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.uiOptions_frame, values=["Light", "Dark"],
        #                                                               command=self.change_appearance_mode_event)
        #self.appearance_mode_optionemenu.grid(row=1, column=2, padx=20, pady=(10, 10))
        #self.scaling_label = customtkinter.CTkLabel(self.uiOptions_frame, text="UI Scaling:", anchor="w")
        #self.scaling_label.grid(row=2, column=2, padx=20, pady=(10, 10))
        #self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.uiOptions_frame, values=["80%", "90%", "100%", "110%", "120%"],
        #                                                       command=self.change_scaling_event)
        #self.scaling_optionemenu.grid(row=3, column=2, padx=20, pady=(10, 10))


        # These set the default displayed value in the corresponding widgets
        
        #self.appearance_mode_optionemenu.set("Light")
        #self.scaling_optionemenu.set("100%")
        self.combobox_1.set("Command List")
        self.combobox_fire.set("Trigger Fire")

        thread = threading.Thread(target=read_from_port, args=(ser,self))
        thread.start()



    # COMMANDS FOR FUNCTIONS


    # This function prints directly without being prompted for user input
    def comboBoxsend1(self):
       command_option = self.combobox_1.get()
       ser.write(command_option.encode())

    def comboBoxsendVariables(self):
        result = simpledialog.askstring("Input", self.combobox_1.get())
        result = result + "\r\n"
        ser.write(result.encode())
        print("Result:", result)


    def comboBoxsend2(self):
        command_option_2 = self.combobox_fire.get()
        ser.write(command_option_2.encode())

    def manualInputCommand(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a command or select from the list:", title="CTkInputDialog")
        print("Command Entered:",dialog.get_input())
        #ser.write(dialog.get_input.encode())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    #def startSerCommsEvent(self):
        

    def stopSerCommsEvent(self):
        print("Stop Selected")
     
    def send_command_event(self):
        print("Command Sent")

    def aboutDeviceSimulator(self):
        dialog = tkinter.messagebox.showinfo(title="Loop Device Simulator", message="This is a loop device simulator that can be used to trigger events")

    def open_file_event(self):
        # return filedialog.askopenfilename() // This is to open a file
        self.destroy()

    def onExit(self):
        self.quit()

    def clearTextBox(self):
        self.textbox1.delete('1.0', END)

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