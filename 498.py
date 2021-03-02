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
Version 1.4 March 2021, - Fixes on previous functions + network selection
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
import base64
import multiprocessing
import csv

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

def send_command1(command):
    ser.write(bytes(command + "\n", encoding='utf8'))  
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
                elif i.strip() == command:
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

def send_command(command):
    
    # print("sending command: " + command) 
    ser.write(bytes(command + "\n", encoding='utf8'))
    
    rcvd = command
    
    while (command.split()[0] in rcvd.strip()) or rcvd.strip() == '':
        received_data = ser.readline()  
        rcvd = str(received_data.decode('ascii'))
        #print("test" + str(rcvd))

    #print("Received: " + rcvd)
    return rcvd
    
def select_network(network_name): 
    ESSID = network_name.get()
    Privacy = data[ESSID][0]
    BSSID = data[ESSID][1]
    Channel = data[ESSID][2]
    
    print("You Selected: " + ESSID + " | " + Privacy + " | " + BSSID + " | " + Channel)
    
def read_csv():
    try:
        with open("search.cap-01.csv",'r') as f:
            with open("search.cap-01.csv_updated.csv",'w') as f1:
                next(f) # skip header line
                for line in f:
                    f1.write(line)
        f1.close()
        f.close()
        data = {} 
        
        with open('search.cap-01.csv_updated.csv', "r") as csvfile:
            csv_reader  = csv.DictReader(csvfile, delimiter=',')
            for row in csv_reader:
                #print(row)
                if row[' ESSID'] != None:
                    if row[' ESSID'].strip() != "":
                        ESSID = row[' ESSID'].strip()
                        Privacy = row[' Privacy'].strip()
                        BSSID = row['BSSID'].strip()
                        Channel = row[' channel'].strip()
                        
                        #print(ESSID + " | " + Privacy + " | " + BSSID + " | " + Channel)
                        data[ESSID] = (Privacy,BSSID,Channel)
        return data
    except Exception as err:
        print("Error: " + str(err))
        return 0
'''
This function will send the command to the pi via serial
'''
def terminal_commands():
    try:
        callback('<Return>')
        terminal_window.bind('<Return>', callback)
    except:
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

def transfer_over_serial(file_name):
    try:
        b64data = send_command("base64 " + file_name + " -w 0 | wc -c && echo") 
        print("Lenght to be transferred: " + str(b64data), flush=True)
        #loading_bar(int(int(b64data)/12000),"Transferring file\n" + file_name)
        b64data = send_command("base64 " + file_name + " -w 0 && echo") 
        print("Received: " + str(len(b64data)))
        
        print("Creating the file...")
        b64data = b64data.encode()
        if '/' in file_name:
            file_name = file_name.split('/')[-1]
        with open(file_name, "wb") as fh:
            fh.write(base64.decodebytes(b64data))    
        print("Done transferring the file: " + file_name)    
        return 1
    except Exception as err:
        print("Error: " + str(err))
        return 0
    
def loading_bar(time_to_load, message):
    x_thread = threading.Thread(target=loading_bar_1, args=(time_to_load, message, root,))
    x_thread.run()
    
def loading_bar_1(time_to_load, message, root): 
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
        root.update()
        temp = time_to_load/10
        
        for i in range(1,11):
            if i != 10:
                progress['value'] = i * 10
            load_window.update_idletasks() 
            #load_window.after(int(temp * 1000))
            time.sleep(temp)
            root.update()
            
        progress['value'] = 100 
        load_window.destroy()
        print("Done with loading bar")
        
    except Exception as err:
        print("error: " + str(err))
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
    
    scan_button=tk.Button(Assessment_window,text='Scan for Networks',command=lambda: scanNetwork(Assessment_window, scan_button), font=("Helvetica 16 bold"))

    label1.grid(row=0,column=0)
    scan_button.grid(row=1,column=0) 

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
    
def encryption_Manager(encryption):
    if encryption == "WEP":
        print ("The Encryption is WEP") 
        
    if encryption == ("WPA" or "WPA2"):
        print ("The Encryption is WEP") 
        capture_Handshake()
        
    if encryption == "WPA3":
        print ("The Encryption is WPA3")
        capture_Handshake()
    
def monitor_mode(mode,card):
    if mode == "enable":
        print("enabling the monitor mode on " + card)
        send_command("sudo iw dev " + card + " interface add mon0 type monitor")
    if mode == "disable": 
        print("disabling the monitor mode on " + card)
        send_command("iw dev mon0 interface del")
    
def capture_handshake():
    print("capture_handshake")

def remove_temp():
    print("Deleting the TEMP folder")
    send_command1("rm /root/temp/*") 
    time.sleep(2)
    
def scanNetwork(Assessment_window,scan_button):
    global data
    
    remove_temp()
    
    monitor_mode("enable", "wlan1")
    
    print("sending scanning command")
    
    send_command1("timeout 15s airodump-ng mon0 -w /root/temp/search.cap &> file") 
    
    loading_bar(20,'Scanning for Networks')
    
    #transfer over the .csv file
    print("Transferring the file")
    x = 1
    while x == 0:
        x = transfer_over_serial('/root/temp/search.cap-01.csv')
    
    data = read_csv()
    
    variable = tk.StringVar()
    variable.set("Please Select a Network") # default value
    
    scan_button.destroy()    
    OptionMenu_button = tk.OptionMenu(Assessment_window, variable, *data.keys())
    select_button = tk.Button(Assessment_window, text='GO!',command= lambda: select_network(variable), font=("Helvetica 12 bold"))
    OptionMenu_button.grid(row=3,column=0) 
    select_button.grid(row=4,column=0) 
    Assessment_window.update()
    
def generate_report():
    print("This is the function to generate a report")
    #writing HTML Content
    heading = '<h1> Automated Report Tutorial by Abhinav Sharma</h1>'
    subheading = '<h3> Sample Report for Placement </h3>'
    # Using .now() from datetime library to add Time stamp
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
    header = '<div class="top">' + heading + subheading +'</div>'
    footer = '<div class="bottom"> <h3> This Report has been Generated on '+ current_time +'</h3> </div>'
    content = '<div class="table"> ' + pivot.to_html() + ' </div> \n <div class="chart"> '+ image_tag +'</div>'
    # Concating everything to a single string
    html = header + content + footer    
    
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
    root.title("CYBV 498 - Wireless Security Assessment Tool")
    root.resizable(False, False)
    
    start_Assessment_button = tk.Button(text='Start Assessment',command=wifi_Assessment, font=("Helvetica 12 bold"))
    #start_Assessment_button = tk.Button(text='Read_File to tkinter',command=lambda: transfer_over_serial_thread('/root/temp/search.cap-01.csv'), font=("Helvetica 12 bold"))
    
    rogueAP_button = tk.Button(text='Rogue AP',command=rogueAP, font=("Helvetica 12 bold"))
    terminal_button=tk.Button(text='Serial Terminal',command=start_terminal, font=("Helvetica 12 bold"))
    
    image2 = Image.open("img/CYBV498.png")
    image2 = image2.resize((150, 130), Image.ANTIALIAS)    
    test2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=test2)
    
    label2.grid(row=0,column=0,padx=5, pady=10, ipadx=15, ipady=10)
    start_Assessment_button.grid(row=1,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    rogueAP_button.grid(row=2,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    terminal_button.grid(row=3,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    
    menuBar = tk.Menu(root)
    toolsMenu = tk.Menu(menuBar, tearoff=0)
    
    toolsMenu.add_command(label='About', command=menuAbout, underline=0)
    toolsMenu.add_separator()
    toolsMenu.add_command(label='Exit', command=root.destroy)
    menuBar.add_cascade(label='Help', menu=toolsMenu, underline=0)  
    root.config(menu=menuBar)  # menu ends    
    
    try:
        ser = serial.Serial(serial_port, baud_rate)
    except:
        messagebox.showinfo("ERROR", "Unable to connect via serial")
        root.destroy()
        
    root.mainloop()    