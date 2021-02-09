'''
Script Purpose: Capstone Project (CYBV498)
Script Version: 1.0 February 2021
Script Author:  Gabriel Haab, University of Arizona

Script Revision History:
Version 1.0 February 2021, Python 3.8.2 - Added serial communication
Version 1.1 February 2021, Python 3.8.2 - Tkinter + Serial
'''

# Imports
import serial # pip3 install serial
import time
import tkinter as tk
import re

serial_port = "COM4"
baud_rate = 115200

'''
This function will read the return data after sending the command.
'''
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
                    text.insert(tk.END,rcvd_list[-1] + " ")
                    print(rcvd_list[-1] + " ", end = "")
                    text.see(tk.END)             
                else:
                    count = True
                    text.insert(tk.END,i + "\n")
                    print(i)
            return 1
            #return 0
        except Exception as err:
            print("EXCEPTION ERROR: " + str(err))        

def callback(event):
    pos = text.index('end-1c linestart')
    pos = float(pos)-1
    line = text.get(pos, tk.END) 
    try:
        command_send = re.search('.*\# (.*)',line).group(1)
    except:
        command_send = line
    #command_send = input("")
    print("Sending command: " + command_send)
    ser.write(bytes(command_send + "\n", encoding='utf8'))
    read_data(command_send)    

'''
This function will send the command to the pi via serial
'''
def send_commands():
    print("=========== DONE WITH LOGIN ===========")
    global ser
    ser = serial.Serial(serial_port, baud_rate)
    callback('<Return>')
    terminal_window.bind('<Return>', callback)
    
def close_connection():
    print("closing Serial Connection")
    ser.close()
    terminal_window.destroy()
    
def connect_serial():        
    '''
    Connect to Serial Port
    
    '''
    global ser
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
                        text.insert(tk.END,rcvd + "\n")
                        terminal_window.update()
                        print(rcvd)
   
                if "raspberrypi login:" in rcvd:
                    startup = True
                    send_commands()      
                    
            except Exception as err:
                print("******************")
                print("ERROR: " + str(err))
                print("******************")
                pass
    except:
        print("Error reading from " + serial_port)

def start_terminal():
    global text
    global terminal_window
    terminal_window = tk.Toplevel()
    terminal_window.title("Terminal")
    
    text=tk.Text(terminal_window, wrap=tk.WORD, height=25, background="black", foreground="green")
    text.pack(fill=tk.BOTH, expand = tk.YES)
    
    send_commands()
    terminal_window.protocol("WM_DELETE_WINDOW", close_connection)
    #button=tk.Button(terminal_window,text='Connect Serial',command=send_commands)
    #button=tk.Button(text='Show End',command = lambda : text.see(tk.END))
    #button.pack(padx=5, pady=10, ipadx=15, ipady=10)
    #terminal_window.mainloop()

if __name__ == '__main__':
    root= tk.Tk()
    root.geometry("400x268")
    root.title("Terminal")
    root.resizable(False, False)
    terminal_button=tk.Button(text='Start terminal',command=start_terminal, font=("Helvetica 16 bold"))
    terminal_button.grid(padx=5, pady=10, ipadx=15, ipady=10)
    root.mainloop()