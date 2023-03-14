import tkinter
import serial
import serial.tools.list_ports


class SerialConnection:

    serialPort = None
    serialDataReceived = ""
    commandDataReceived = ""
    commandInProgress = False
    ports = [comport.device for comport in serial.tools.list_ports.comports()]

    def __init__(self):
        heheh = 0

    def openPort(self, selected_port):
        self.port = selected_port
        if self.port is not None:
            try:
                self.serialPort = serial.Serial(
                    port=self.port,
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1  # adjust this to match the expected response time from the device or software
                )
                print(f"Port {self.port} is opened!")
                return True
            except serial.SerialException:
                print(f"Failed to open port {self.port}")
                return False
        else:
            print("No available ports found!")
            return False

    def closePort(self):
        if self.serialPort and self.serialPort.is_open:
            self.serialPort.close()
            print("Serial port has closed")
        else:
            print("Serial port is already closed.")

    def select_port(self):
        ports = [comport.device for comport in serial.tools.list_ports.comports()]
        for port in ports:
            try:
                ser = serial.Serial(
                    port=port,
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE
                )
                ser.close()
                return port
            except serial.SerialException:
                pass
        return None

    def is_open(self):
        if self.serialPort is not None:
            return self.serialPort.is_open
        return False

    def write(self, data):
        if self.serialPort is not None and self.serialPort.is_open:
            self.serialPort.write(data)

    def read_line(self):
        if self.serialPort is not None and self.serialPort.is_open:
            return self.serialPort.readline().decode().strip()
        return None

   

    def read_from_port(self):

        while self.serialPort.is_open:
            if self.is_open:
                try:
                    reading = self.serialPort.readline().decode()
                    self.serialDataReceived = self.serialDataReceived + reading 
                    if self.commandInProgress == True:
                        self.commandDataReceived = self.commandDataReceived + reading
                except:
                    pass
            else:
                pass

