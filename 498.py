# Imports
import serial # pip3 install serial
import time
import re 

serial_port = "COM4"
baud_rate = 115200

def read_data(command_send):
    count = False
    
    while count == False:
        received_data = ser.read()              #read serial port
        time.sleep(1)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        rcvd = received_data.decode('ascii')
        
        rcvd = rcvd.strip()        
        rcvd_list = rcvd.split('\r\n')
        
        if "Under-voltage detected!" in rcvd:
            pass  
        
        try:
            #print(rcvd_list)
            for i in rcvd_list: 
                if i.strip() == '':
                    pass    
                elif "Under-voltage detected!" in i:
                    pass       
                elif i.strip() == command_send:
                    pass            
                elif i == rcvd_list[-1]:
                    print(rcvd_list[-1] + " ", end = "")
                else:
                    count = True
                    print(i)

            return 1
            #return 0
        except Exception as err:
            print("EXCEPTION ERROR: " + str(err))        

def send_commands():
    print("=========== DONE WITH LOGIN ===========")
    while True:
        command_send = input("")
        ser.write(bytes(command_send + "\n", encoding='utf8'))
        read_data(command_send)


'''
Connect to Serial Port

'''
connection = False
print("Waiting for connection to: " + serial_port)
while (connection == False) :
    try:
        ser = serial.Serial (serial_port, baud_rate)    #Open port with baud rate
        connection = True      
    except:
        pass

startup = False
try:
    while (startup == False):
        received_data = ser.read()              #read serial port
        time.sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        
        try:
            #print(received_data)
            rcvd = received_data.decode('ascii').replace('[\x1b[0;32m','[').replace('\x1b[0m]',']')
            
            if "Under-voltage detected!" in rcvd:
                pass
            elif rcvd == '':
                pass            
            else:
                rcvd = rcvd.strip() 
                rcvd = rcvd.replace('\r\n','\n')
                if rcvd != '':
                    print(rcvd)  
            
            if "raspberrypi login:" in rcvd:
                startup = True
                send_commands()      
                
        except Exception as err:
            print ("error: " + str(err))
            pass
except:
    print("Error reading from " + serial_port)
    send_commands()

  