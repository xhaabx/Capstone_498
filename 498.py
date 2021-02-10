about = \
'''
Script Purpose: Capstone Project (CYBV498)
Script Version: 1.3 February 2021
Script Author:  Gabriel Haab, University of Arizona

Script Revision History (Python 3.8.2):
Version 1.0 February 2021, - Added serial communication
Version 1.1 February 2021, - Tkinter + Serial Connection
Version 1.2 February 2021, - Tkinter Images + about menu + some structures
Version 1.3 February 2021, - Loading window + some structures
'''

# Imports
import serial # pip3 install serial
import time
import tkinter as tk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image  
from   tkinter import messagebox
import threading
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
        if '#' in line:
            command_send = re.search('.*\# (.*)',line).group(1)
        elif ':' in line: 
            command_send = re.search('.*\: (.*)',line).group(1)
        else:
            command_send = ""
    except:
        command_send = line
    #command_send = input("")
    print("Sending command: " + command_send)
    ser.write(bytes(command_send + "\n", encoding='utf8'))
    read_data(command_send)    


def send_command(command):
    ser = serial.Serial(serial_port, baud_rate)
    ser.write(bytes(command + "\n", encoding='utf8'))

'''
This function will send the command to the pi via serial
'''
def terminal_commands():
    global ser
    try:
        ser = serial.Serial(serial_port, baud_rate)
        callback('<Return>')
        terminal_window.bind('<Return>', callback)
    except:
        messagebox.showinfo("ERROR", "Unable to connect via serial")
        close_connection()
            
def close_connection():
    print("closing Serial Connection")
    try:
        ser.close()
        terminal_window.destroy()
    except:
        terminal_window.destroy()
        pass
    
    
def wait_Login():        
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
                    terminal_commands()      
                    
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
    terminal_window.protocol("WM_DELETE_WINDOW", close_connection)
    
    #wait_Login()
    terminal_commands()

def wardriving():
    wardriving_window = tk.Toplevel()
    wardriving_window.title("About") 
    wardriving_window.resizable(False, False)      
    label1 = tk.Label(wardriving_window, text="This is the window for WarDriving.")
    
    close_button=tk.Button(wardriving_window,text='CLOSE',command=wardriving_window.destroy, font=("Helvetica 16 bold"))
    
    label1.grid(row=0,column=0)
    close_button.grid(row=1,column=0) 
    
    wardriving_window.mainloop()

def loading_bar(time_to_load, message):
    x = threading.Thread(target=loading_bar_1, args=(time_to_load, message,))
    x.start()

    
def loading_bar_1(time_to_load, message): 
    try:
        load_window = tk.Toplevel(root)
        load_window.resizable(False, False)
        load_window.title('Results')
            
        # Progress bar widget 
        label = tk.Label(load_window,text=message,font=("Helvetica 16 bold"))
        
        progress = Progressbar(load_window, orient = tk.HORIZONTAL, length = 100, mode = 'determinate') 
        label.pack(pady = 20, padx = 20,)
        progress.pack(pady = 20, padx = 20,ipady = 15, ipadx = 50) 
        load_window.update()
        
        temp = time_to_load/10
        
        for i in range(1,11):
            if i != 10:
                progress['value'] = i * 10
            load_window.update_idletasks() 
            time.sleep(temp) 
            
        progress['value'] = 100 
        load_window.destroy()
    except:
        messagebox.showinfo("ERROR", message + " Cancelled")  
        
def rogueAP():
    rogueAP_window = tk.Toplevel()
    rogueAP_window.title("About") 
    rogueAP_window.resizable(False, False)    
    
    label1 = tk.Label(rogueAP_window, text="SSID")
    label_input1 = tk.Entry(rogueAP_window)
    label2 = tk.Label(rogueAP_window, text="Channel")
    label_input2 = tk.Entry(rogueAP_window)    
    label3 = tk.Label(rogueAP_window, text="Webpage:")
    label_input3 = tk.Entry(rogueAP_window)    
    label4 = tk.Label(rogueAP_window, text="")
    label_input4 = tk.Entry(rogueAP_window)    
    
    close_button=tk.Button(rogueAP_window,text='CLOSE',command=rogueAP_window.destroy, font=("Helvetica 16 bold"))
    
    label1.grid(row=1,column=0)
    label_input1.grid(row=1,column=1)
    label2.grid(row=2,column=0)
    label_input2.grid(row=2,column=1)
    label3.grid(row=3,column=0)
    label_input3.grid(row=3,column=1)
    label4.grid(row=4,column=0)
    label_input4.grid(row=4,column=1)
    close_button.grid(row=5,columnspan=2)  
    
    rogueAP_window.mainloop()

def wifi_Assessment():
    Assessment_window = tk.Toplevel()
    Assessment_window.title("Assessment") 
    Assessment_window.resizable(False, False)      
    label1 = tk.Label(Assessment_window, text="This is the window for the Wireless Assessment.")
    
    scan_button=tk.Button(Assessment_window,text='Scan for Networks',command=scanNetwork, font=("Helvetica 16 bold"))
    select_button=tk.Button(Assessment_window,text='Select Network',command=assessment_manager, font=("Helvetica 16 bold"))
    
    label1.grid(row=0,column=0)
    scan_button.grid(row=1,column=0) 
    select_button.grid(row=5,column=0) 
    Assessment_window.mainloop()    

def assessment_manager():
    Authentication = 0
    if Authentication:
        print("Authenticate Scanning")
        connect_to_wireless() 
        analyze_traffic()
    else:
        print("Non-Authenticate Scanning") 
        encryption_Manager()
        
def connect_to_wireless():
    # This function will connect to the wireless via WPAClient():
    print("Function to connect to the wireless network") 
    
def analyze_traffic():
    # This fucntion will make a dump of the network likely through tshark. and perform many different analysis.
    # This function will perform a passive or active scan. (Choose one)
    print("Function to analyze the network")
    
def encryption_Manager():
    encryption = open("search.cap")
    
    if encryption == "WEP":
        print ("The Encryption is WEP") 
        
    if encryption == ("WPA" or "WPA2"):
        print ("The Encryption is WEP") 
        capture_Handshake()
        
    if encryption == "WPA3":
        print ("The Encryption is WPA3")
        capture_Handshake()
    
def capture_handshake():
    print("capture_handshake")
    
def capture_handshake():
    print("capture_handshake")
    
def scanNetwork():
    # send_command("timeout 30s airodump-ng mon0 -w search.cap") 
    loading_bar(35,'Scanning Networks')
    
def generate_report():
    print("This is the function to generate a report")
    
def menuAbout():
    about_window = tk.Toplevel()
    about_window.title("About") 
    about_window.resizable(False, False)
    label1 = tk.Label(about_window, text=about, justify=tk.LEFT)
    
    image1 = Image.open("img/UA_Cyber_Operations.png")
    image1 = image1.resize((400, 70), Image.ANTIALIAS)
    test1 = ImageTk.PhotoImage(image1)
    label1_img = tk.Label(about_window, image=test1)
    
    close_button=tk.Button(about_window,text='OK',command=about_window.destroy, font=("Helvetica 10 bold"))
    
    label1_img.grid(row=0,column=0,padx=5, pady=10, ipadx=15, ipady=10)
    label1.grid(row=1,column=0,padx=5, pady=10, ipadx=15, ipady=10)
    close_button.grid(row=2,column=0,padx=5, pady=10, ipadx=15, ipady=10)
    about_window.mainloop()
    
if __name__ == '__main__':
    root= tk.Tk()
    #root.geometry("400x268")
    root.title("CYBV 498 - Wireless Security Assessment Tool")
    root.resizable(False, False)

    start_Assessment_button = tk.Button(text='Start Assessment',command=wifi_Assessment, font=("Helvetica 12 bold"))
    rogueAP_button = tk.Button(text='Rogue AP',command=rogueAP, font=("Helvetica 12 bold"))
    wardriving_button = tk.Button(text='WarDriving',command=wardriving, font=("Helvetica 12 bold"))
    terminal_button=tk.Button(text='Serial Terminal',command=start_terminal, font=("Helvetica 12 bold"))

    image2 = Image.open("img/CYBV498.png")
    image2 = image2.resize((150, 130), Image.ANTIALIAS)    
    test2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=test2)

    label2.grid(row=0,columnspan=2,padx=5, pady=10, ipadx=15, ipady=10)
    start_Assessment_button.grid(row=1,columnspan=2,padx=5, pady=5, ipadx=5, ipady=5)
    rogueAP_button.grid(row=2,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    wardriving_button.grid(row=2,column=1,padx=5, pady=5, ipadx=5, ipady=5)
    terminal_button.grid(row=3,columnspan=2,padx=5, pady=5, ipadx=5, ipady=5)
    
    menuBar = tk.Menu(root)
    toolsMenu = tk.Menu(menuBar, tearoff=0)
    
    toolsMenu.add_command(label='About', command=menuAbout, underline=0)
    toolsMenu.add_separator()
    toolsMenu.add_command(label='Exit', command=root.destroy)
    menuBar.add_cascade(label='Help', menu=toolsMenu, underline=0)  
    root.config(menu=menuBar)  # menu ends    
    
    
    root.mainloop()