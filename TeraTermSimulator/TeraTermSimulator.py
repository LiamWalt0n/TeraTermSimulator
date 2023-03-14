from logging import root
import threading
import time
import GUI
import serial_connection
import serial
import serial.tools.list_ports

def handleIncomingText(serial, myGUI):
    while True:
        if serial.serialPort is None:
            print("Error: Serial port is not open.")
            break
        if serial.serialPort.is_open:
            if serial.serialDataReceived != "":
                print(serial.serialDataReceived)
                myGUI.serialReceiveTextBox.insert('end', serial.serialDataReceived.encode())
                serial.serialDataReceived = ""    
                myGUI.serialReceiveTextBox.see('end')  # scroll to the end of the textbox
        else:
            print("Error: Serial port is not open.")
            break
        time.sleep(0.1)



def startThreads(serial, myGUI):


    threadSerial = threading.Thread(target=serial.read_from_port, args=())
    threadSerial.start()
    
    threadHandle = threading.Thread(target=handleIncomingText, args=(serial, myGUI))
    threadHandle.start()

                    
if __name__ == "__main__":
    

    
    serial = serial_connection.SerialConnection()
    myGUI = GUI.App(serial)

    #threadSerial = threading.Thread(target=serial.read_from_port, args=())
    #threadSerial.start()
    
    #threadHandle = threading.Thread(target=handleIncomingText, args=(serial, myGUI))
    #threadHandle.start()

    myGUI.mainloop()
   