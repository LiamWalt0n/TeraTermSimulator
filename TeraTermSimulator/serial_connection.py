import serial
import serial.tools.list_ports

class SerialConnection:

    serial_is_open = True
    serialDataReceived = ""
    ports = [comport.device for comport in serial.tools.list_ports.comports()]

    def __init__(self):
        self.ser = None
        self.port = self.select_port()
        if self.port is not None:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"Port {self.port} is opened!")
        else:
            print("No available ports found!")

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
        if self.ser is not None:
            return self.ser.is_open
        return False

    def write(self, data):
        if self.ser is not None and self.ser.is_open:
            self.ser.write(data)

    def read_line(self):
        if self.ser is not None and self.ser.is_open:
            return self.ser.readline().decode().strip()
        return None

    #def read_from_port(self):
    #    while self.serial_is_open:
    #        if self.ser.is_open:
    #            try:
    #                reading = self.ser.readline().decode()
    #                self.serialDataReceived = self.serialDataReceived + reading                    
    #            except:
    #                pass
    #        else:
    #            pass
