about = \
'''
Script Purpose: Capstone Project (CYBV498)
Script Version: 1.6 February 2021
Script Author:  Gabriel Haab, University of Arizona

Script Revision History (Python 3.8.2):
Version 1.0 February 2021, - Added serial communication
Version 1.1 February 2021, - Tkinter + Serial Connection
Version 1.2 February 2021, - Tkinter Images + about menu + some structures
Version 1.3 February 2021, - Loading window + some structures
Version 1.4 March 2021, - Fixes on previous functions + network selection
Version 1.5 March 2021 - Adjusted Assessment TKinter windows
Version 1.6 March 2021 - Added comments
Version 1.7 March 2021 - Capture Handshake + Network connect 
Version 1.8 March 2021 - Minor Adjustments 
Version 1.9 March 2021 - Cleanup and function integration
'''

#Third party imports
import serial 
from xhtml2pdf import pisa
import pandas as pd
from PIL import ImageTk, Image  
from mac_vendor_lookup import MacLookup

# Imports
import time
import tkinter as tk
from tkinter.ttk import Progressbar
from   tkinter import messagebox
import threading
import re
import base64
import csv
from datetime import datetime
import os 

serial_port = "COM4"
baud_rate = 115200

'''
================================================================
read_data(command_send)
This function will read the return data after sending a command
to the serial port. 
================================================================
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

"""
================================================================
================================================================
"""
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
    try:  
        if command_send.split()[0] == 'download':
            text.insert(tk.END,"Attempting to download the file. Please wait.\n")
            transfer_over_serial(command_send.split()[1])
            text.insert(tk.END,"File Transferred\n")
            ser.write(bytes("\n", encoding='utf8'))
            read_data(command_send)
        else:
            print("Sending command: " + command_send)
            ser.write(bytes(command_send + "\n", encoding='utf8'))
            read_data(command_send)     
    except:
        print("Sending command: " + command_send)
        ser.write(bytes(command_send + "\n", encoding='utf8'))
        read_data(command_send)    

"""
================================================================
================================================================
"""
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
            
"""
================================================================
send_command()
This function will send the command to the pi via serial connection
and return 1.
================================================================
"""
def send_command(command):
    
    # print("sending command: " + command) 
    ser.write(bytes(command + "\n", encoding='utf8'))
    
    # Clear Buffer / Wait for command to finish.
    dbstr = ""
    while 'root@raspberrypi' not in dbstr:
        dbstr = ser.readline()
        dbstr = str(dbstr.decode('ascii'))
        
    return 1

"""
================================================================
send_command2()
This function will send the command to the pi via serial connection
and return value printed in the pi to the calling function.
================================================================
"""
def send_command2(command):
    
    # print("sending command: " + command) 
    ser.write(bytes(command + "\n", encoding='utf8'))
    
    rcvd = command
    
    while (command.split()[0] in rcvd.strip()) or rcvd.strip() == '':
        received_data = ser.readline()  
        rcvd = str(received_data.decode('ascii'))
        #print("test" + str(rcvd))
    
    #print("Received: " + rcvd)
    return rcvd
"""
================================================================
read_csv() 
This function reads the .csv file generated by airodump-ng and 
parses the valuable information and saves into a dict named 
"data". The function returns this variable.
================================================================
"""
def read_csv():
    try:
        with open("Full_Scan-01.csv",'r', encoding="utf8") as f:
            with open("Full_Scan-01.csv_updated.csv",'w') as f1:
                next(f) # skip header line
                for line in f:
                    f1.write(line)
        f1.close()
        f.close()
        data = {} 
        
        with open('Full_Scan-01.csv_updated.csv', "r") as csvfile:
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
    
"""
================================================================
terminal_commands()
This function will send the command to the pi via serial connection
================================================================
"""
def terminal_commands():
    try:
        callback('<Return>')
        terminal_window.bind('<Return>', callback)
    except Exception as err:
        print("something is wrong: " + str(err))
        pass
        #close_connection()

"""
================================================================
close_connection()
This function is responsible for closing the serial connection
between the raspberry pi and this tool. 
================================================================
"""            
def close_connection():
    print("closing Serial Connection")
    try:
        ser.close()
        root.destroy()
    except:
        root.destroy()
        pass

"""
================================================================
TODO: CHANGE to auto_login().
================================================================
"""
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

"""
================================================================
start_terminal()
This function is responsible for starting a terminal window that 
communicates with the raspberry pi. 
================================================================
"""
def start_terminal():
    global text
    global terminal_window
    terminal_window = tk.Toplevel()
    terminal_window.title("Terminal")
    
    text=tk.Text(terminal_window, wrap=tk.WORD, height=25, background="black", foreground="green")
    text.pack(fill=tk.BOTH, expand = tk.YES)
    #terminal_window.protocol("WM_DELETE_WINDOW", close_connection)
    
    #wait_Login()
    terminal_commands()

"""
================================================================
transfer_over_serial()
This function transfer files from the raspberry pi to the tool.
The file is converted to base64 and transferred via serial port 
to this tool, which will then convert back to the original format.
================================================================
"""
def transfer_over_serial(file_name):
    try:
        # clean buffer
        received_data = ser.read()              #read serial port
        time.sleep(1) #check for remaining byte
        received_data += ser.read(ser.inWaiting())  
        # clean buffer
        
        b64data = send_command2("base64 " + file_name + " -w 0 | wc -c && echo") 
        int(b64data)
        print("Lenght to be transferred: " + str(b64data), flush=True)
        #loading_bar(int(int(b64data)/12000),"Transferring file\n" + file_name)
        b64data = send_command2("base64 " + file_name + " -w 0 && echo") 
        print("Received: " + str(len(b64data)))
        
        print("Creating the file...")
        
        b64data = b64data.encode()
        if '/' in file_name:
            file_name = file_name.split('/')[-1]
        try:
            with open(selected_network['ESSID'] + '/' + file_name, "wb") as fh:
                fh.write(base64.decodebytes(b64data))    
        except:
            with open(file_name, "wb") as fh:
                fh.write(base64.decodebytes(b64data))   
                
        print("Done transferring the file: " + file_name)    
        return 1
    except Exception as err:
        print("Error: " + str(err))
        return 0

"""
================================================================
loading_bar()
This function creates a thread that will hold a loading bar.
================================================================
"""    
def loading_bar(time_to_load, message):
    x_thread = threading.Thread(target=loading_bar_1, args=(time_to_load, message, root,))
    x_thread.run()

"""
================================================================
loading_bar_1()
This function creates the loading bar.
================================================================
"""    
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

"""
================================================================
rogueAP()
This function is responsible for creating a RogueAP attack.
================================================================
"""        
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

"""
================================================================
wifi_Assessment()
This is the main page for the wifi_assessment function. 
================================================================
"""
def wifi_Assessment():
    
    Assessment_window = tk.Toplevel()
    Assessment_window.title("Wireless Assessment")
    Assessment_window.resizable(False, False)     
    
    message = tk.Label(Assessment_window, text="Automated Wireless Security Assessment Tool.\n\nThis tool is intended to be used for legal security purposes only, \nYou should only use it to protect devices you own or have permission to test.\nAny other use is not the responsibility of the developer(s).\n\n", font=("Helvetica 12 bold"))
    
    back_button=tk.Button(Assessment_window,text='Back',command=Assessment_window.destroy, font=("Helvetica 16 bold")) 
    next_button=tk.Button(Assessment_window,text='Next',command=lambda: scanNetwork(Assessment_window, message, next_button,back_button), font=("Helvetica 16 bold"))

    message.grid(row=0,columnspan=2,padx=5, pady=5, ipadx=5, ipady=5)
    next_button.grid(row=2,column=1,padx=5, pady=5, ipadx=5, ipady=5)
    back_button.grid(row=2,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    Assessment_window.mainloop()    

"""
================================================================
get_password()
This function is responsible for defining if the tool will perform
an authenticated scan or not. 
================================================================
"""
def get_password(Assessment_window, message, next_button,back_button):
    
        message.config(text="Please type in the password for:\n\n ESSID: " + selected_network['ESSID'])
        password_input = tk.Entry(Assessment_window)
        var = tk.IntVar()
        next_button.config(text="Next",command= lambda: var.set(0))
        back_button.config(text="Skip",command= lambda: var.set(1))
        password_input.grid(row=1,columnspan=2,padx=5, pady=5, ipadx=5, ipady=5)
        Assessment_window.update()
        next_button.wait_variable(var)
        if var.get() == 0:
            selected_network['PASS'] = password_input.get()
        if var.get() == 1:
            selected_network['PASS'] = False
        password_input.destroy()
        traffic_analyze()

"""
================================================================
Function to perform an active scan in the network. 
================================================================
"""    
def traffic_analyze():
    if selected_network['PASS'] == False:
        return 0
    
    print("start of traffic_analyze()")

    # Decrypt File    
    print("Decrypt Network Traffic")
    # https://www.aircrack-ng.org/doku.php?id=airdecap-ng
    send_command("airdecap-ng -e '" + selected_network['ESSID'] + "' -p " + selected_network['PASS'] + " /root/temp/" + selected_network['ESSID'] + "-01.cap")
    time.sleep (10)
    
    print("PCAP to .CSV")
    send_command("tshark -r " + "/root/temp/" + selected_network['ESSID'] + "-01-dec.cap" + " -T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e _ws.col.SrcPort -e _ws.col.DstPort -e ip.dst -e _ws.col.Protocol -E header=y -E separator=, -E quote=d -E occurrence=f > tshark_file.csv")
    time.sleep(10)
    # It outputs a new file ending with -dec.cap which is the decrypted/stripped version of the input file.
    
    print("Transferring files")
    x=0
    while x == 0:
        x = transfer_over_serial('/root/temp/tshark_file.csv')
        time.sleep(5)    
    
    # ======================= Analyse File ===============
    try:
        df_dump = pd.read_csv(selected_network['ESSID'] + "/tshark_file.csv")
        
        possible_protocols = ['DHCP','ARP', 'DNS', 'TCP','UDP']
        
        df_dump = df_dump.rename(columns={'frame.number': 'Frame', 'frame.time': 'Time', 'eth.src': 'Source_Mac', 'eth.dst': 'Destination_Mac', 'ip.src': 'IP_Source', 'ip.dst':'IP_Destination', '_ws.col.Protocol':'Protocol', '_ws.col.SrcPort':'Source_Port', '_ws.col.DstPort':'Destination_Port'})
       
        df_dump = df_dump[df_dump['Protocol'].isin(possible_protocols)]
        print(df_dump.head().to_string())
        print("\n\n====================\n\n")
        
        # ======================= Protocol count =======================
        
        df_dump_prot = df_dump.groupby('Protocol').Frame.count()
        print(df_dump_prot.to_string())
        
        ax = df_dump_prot.plot(kind='bar', title='protocol by count', rot=15)
        ax.set_xlabel("Protocol")
        ax.set_ylabel("count")
    
        fig = ax.get_figure()
        fig.savefig(selected_network['ESSID'] + '/Protocol_Graph.jpeg')    
        
        # ======================= Source IP packet count =======================
        
        df_dump_srcip_count = df_dump.groupby('IP_Source').Frame.count()
        ax = df_dump_srcip_count.plot(kind='bar', title='Source IP by count', rot=15)
        ax.set_xlabel("IP")
        ax.set_ylabel("Count")
    
        fig = ax.get_figure()
        fig.savefig(selected_network['ESSID'] + '/Source_IPCount_Graph.jpeg')    
        
        # ======================= Destination IP packet count =======================
        
        df_dump_destip_count = df_dump.groupby('IP_Destination').Frame.count()
        ax = df_dump_destip_count.plot(kind='bar', title='Destination IP by count', rot=15)
        ax.set_xlabel("IP")
        ax.set_ylabel("Count")
    
        fig = ax.get_figure()
        fig.savefig(selected_network['ESSID'] + '/Dest_IPCount_Graph.jpeg')
    except Exception as err:
        print("unable to decrypt traffic: " + str(err))
    print("End of traffic_analyze()")

"""
================================================================
dump_traffic. 
This fucntion will make a dump of the network likely through tshark.
This function will perform an active scan.
This function will perform an nmap scan.
This function will also generate sobre analyses through Panda.
================================================================
"""    
def dump_traffic():
    print("starting dump_traffic()")
    
    remove_temp()
    dump_time = 120 # time in seconds to analyze the traffic
    
    print("Enabling monitor mode")
    monitor_mode("enable", "wlan1", selected_network['Channel'])
    
    print("Starting Dump")
    send_command("tmux new -s 'capture_handshake' -d")
    send_command("tmux new-window -t 'capture_handshake' -n:airodump-ng 'timeout " +  str(dump_time) + "s airodump-ng -c "  + selected_network['Channel'] + " --bssid " + selected_network['BSSID'] + " -w /root/temp/" + selected_network['ESSID'] + " wlan1mon'")
    
    
    # Capture the handshake
    time.sleep(5)
    send_command("aireplay-ng -0 10 -a " + selected_network['BSSID'] + " wlan1mon")
    time.sleep(10)
    send_command("aireplay-ng -0 10 -a " + selected_network['BSSID'] + " wlan1mon")
    time.sleep(10)
    time.sleep(5)
    
    loading_bar(dump_time-30,'Creating a network dump')
    
    send_command("tmux kill-session -t 'capture_handshake'")
    
    print("Disable monitor mode:")
    monitor_mode("disable", "wlan1", selected_network['Channel'])
    
    print("End of dump_traffic()")    

"""
================================================================
handshake_Hash()
This function is responsible for generating a hash of the handshake
This can later be used for offline password cracking.
================================================================
"""  
def handshake_Hash():
    print("Start of handshake_Hash()")
    selected_network['WPAHash'] = 'something something'
    
    print("End of handshake_Hash()")
    
"""
================================================================
encryption_Manager()
This function is responsible for managing the different attacks 
depending on the encryption method being used.
================================================================
"""    
def encryption_Manager(Assessment_window, message, next_button,back_button):
    
    #Create the folder to hold all the analysis
    try:
        os.mkdir(selected_network['ESSID']) 
    except:
        # Delete all contents of the directory
        for file in os.listdir(selected_network['ESSID']):
            os.remove(selected_network['ESSID'] + '/' + file)
        # Delete the empty folder
        os.rmdir(selected_network['ESSID'])
        # Create the folder. 
        os.mkdir(selected_network['ESSID']) 
        
    if "WEP" in selected_network['Privacy']:
        print("The Encryption is WEP") 
        dump_traffic()
        
    elif "WPA3" in selected_network['Privacy']:
        print ("The Encryption is WPA3")   
        dump_traffic()
        compare_channels(selected_network['Channel'])
        airgraph("/root/temp/" + selected_network['ESSID'] + ".csv")
        generate_report(Assessment_window, message, next_button,back_button)
        
    elif "WPA" in selected_network['Privacy']:
        print ("The Encryption is WPA or WPA2") 
        dump_traffic()
        handshake_Hash()
        get_password(Assessment_window, message, next_button,back_button)
        compare_channels(selected_network['Channel'])
        airgraph("/root/temp/" + selected_network['ESSID'] + "-01.csv")
        generate_report(Assessment_window, message, next_button,back_button)
    
    else:
        print("I don't know this encryption")
        
"""
================================================================
monitor_mode()
This function is responsible for switching the wireless card into
monitor mode. 
================================================================
"""    
def monitor_mode(mode,card,channel):
    if mode == "enable":
        print("enabling the monitor mode on " + card)
        #send_command("sudo iw dev " + card + " interface add mon0 type monitor")
        send_command("airmon-ng start " + card + " " + channel)
        time.sleep(3) # wait 3 seconds just in case.
    
    if mode == "disable": 
        print("disabling the monitor mode on " + card)
        #send_command("iw dev mon0 interface del")
        send_command("airmon-ng stop " + card + "mon")
        time.sleep(3) # wait 3 seconds just in case.
   
"""
================================================================
airgraph()
This function generates a graph of connected devices, and probing 
devices.
================================================================
"""

def airgraph(file):
    # airgraph-ng -i Jenga_2.4-01.csv -o Client_To_AP.png -g CAPR
    send_command("airgraph-ng -i " + file + " -o /root/temp/Client_To_AP.png" + " -g CAPR")
    time.sleep(20)
    
    # Transfer files:
    print("Done creating images")
    x = 0
    while x == 0:
        x = transfer_over_serial('/root/temp/Client_To_AP.png')
        time.sleep(5)
    print("Done tranferring CAPR")

"""
================================================================
remove_temp()
This function is responsible for deleting all files in the folder
/root/temp. This function is called before each scanning.
================================================================
"""
def remove_temp():
    print("Deleting the TEMP folder")
    send_command("rm /root/temp/*") 
    time.sleep(2)

"""
================================================================
scanNetwork()
This function is responsible for searching for networks in the
area. This function utilizes airodump-ng
================================================================
"""    
def scanNetwork(Assessment_window, message, next_button, back_button):
    global data

    # ==================================================
    # Performing the activities
    # ==================================================
    remove_temp() 
    monitor_mode("enable", "wlan1","")
    
    print("sending scanning command")
    send_command1("timeout 15s airodump-ng wlan1mon -w /root/temp/Full_Scan &> /root/temp/file") 
    loading_bar(20,'Scanning for Networks')
    
    #transfer over the .csv file
    print("Transferring the file")
    x = 0
    while x == 0:
        x = transfer_over_serial('/root/temp/Full_Scan-01.csv')
        time.sleep(5)
    data = read_csv()
    monitor_mode("disable", "wlan1","")
    
    # ==================================================
    # ==================================================    
    
    list_grid = Assessment_window.grid_slaves()
    for l in list_grid:
        l.destroy() 
    
    Assessment_window.update()
    network_name = tk.StringVar()
    network_name.set("Please Select a Network") # default value        
        
    message = tk.Label(Assessment_window,text="Please select the network to perform the assessment", font=("Helvetica 12 bold"))
    OptionMenu_button = tk.OptionMenu(Assessment_window, network_name, *data.keys())
    next_button=tk.Button(Assessment_window,text='Next',command= lambda: select_network(Assessment_window, message, next_button,back_button,OptionMenu_button,network_name), font=("Helvetica 16 bold"))
    
    back_button=tk.Button(Assessment_window,text="Scan again", command= lambda: scanNetwork(Assessment_window, message, next_button,back_button),font=("Helvetica 16 bold"))
    
    message.grid(row=0,columnspan=2,padx=5, pady=5, ipadx=5, ipady=5)
    OptionMenu_button.grid(row=1,columnspan=2,padx=5, pady=5, ipadx=5, ipady=5)
    next_button.grid(row=2,column=1,padx=5, pady=5, ipadx=5, ipady=5)
    back_button.grid(row=2,column=0,padx=5, pady=5, ipadx=5, ipady=5)    
    
    Assessment_window.update()

"""
================================================================
select_network()
This function is responsible for parsing the selected network
into the global variable "selected_network" that will be used by
other functions.
================================================================
"""
def select_network(Assessment_window, message, next_button,back_button,OptionMenu_button,network_name): 
    global selected_network
    
    Assessment_window.update()
    selected_network = {}
    ESSID = network_name.get()
    if network_name.get() != "Please Select a Network":
        selected_network['ESSID'] = ESSID
        selected_network['Privacy'] = data[ESSID][0]
        selected_network['BSSID'] = data[ESSID][1]
        selected_network['Channel'] = data[ESSID][2]
        
        OptionMenu_button.destroy()
        
        message.config(text="You Selected:\n\n ESSID: " + selected_network['ESSID'] + " \nEncryption: " + selected_network['Privacy'] + " \nBSSID: " + selected_network['BSSID'] + " \nChannel: " + selected_network['Channel'])
        next_button.config(text="Next",command= lambda: encryption_Manager(Assessment_window, message, next_button,back_button))
        back_button.config(text="Quit",command=Assessment_window.destroy)                   
    else:
        messagebox.showinfo("ERROR", "PLEASE SELECT A NETWORK\nFROM THE DROPDOWN MENU")
        scanNetwork(Assessment_window, message, next_button,back_button)

"""
================================================================
generate_report()
This function is responsible for generating the end-user report
The report is based on a HTML template filled with tags '[tag]'. 
Based on the information gathered from the network, the script
automatically replaces the tags.
================================================================
"""    
def generate_report(Assessment_window, message, next_button,back_button):
    print("This is the function to generate a report")  
    
    # Integrate function here
    
    # ^^
    
    Assessment_window.update()
    message.config(text="The report has been generated.")
    
    next_button.config(text="Exit", command= Assessment_window.destroy)
    back_button.config(text="Open Report", command= lambda: os.startfile("Report.pdf"))
    next_button.grid(row=2,columnspan=2,padx=5, pady=5, ipadx=5, ipady=5)
    Assessment_window.update()

"""
================================================================
compare_channels()
This function is responsible for creating the graph of channels
used in the range of this tool. This helps find overlapping 
channels.
================================================================
"""    
def compare_channels(target):
    all_channels = [1,2,3,4,5,6,7,8,9,10,11,12]
    df_channels=pd.DataFrame.from_dict(data,orient='index')
    
    hue = df_channels[2].value_counts()
    target_num = 0 
    for index, value in hue.items():
        all_channels.remove(int(index))
        if index == target:
            target_num = value
        
    print(all_channels)  
    hue3 = hue.append(hue.reindex(all_channels, fill_value=0))
    
    hue3.index = hue3.index.map(int)
    hue3 = hue3.sort_index()
    
    ax = hue3.plot(title='Channels x #APs',style='.-',xticks=range(0,14))
    ax.set_xlabel("Channels")
    ax.set_ylabel("Number of Access Points")
    ax.plot(int(target),int(target_num), marker='o',markersize=10, color="red")
    
    fig = ax.get_figure()
    fig.savefig(selected_network['ESSID'] + '/Compare_Channels.jpeg')
    print("done")

"""
================================================================
menuabout()
This function is responsible for showing relevante information 
regarding this tools usage and credits.
================================================================
"""    
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

"""
================================================================
main()
This is the main function and it is responsible for the tkinter
root window.
================================================================
"""    
if __name__ == '__main__':

    root= tk.Tk()
    root.title("CYBV 498 - Wireless Security Assessment Tool")
    root.resizable(False, False)
    
    start_Assessment_button = tk.Button(text='Start Assessment',command=wifi_Assessment, font=("Helvetica 12 bold"))
    #start_Assessment_button = tk.Button(text='Download File',command=lambda: transfer_over_serial('Client_To_AP.png'), font=("Helvetica 12 bold"))
    
    rogueAP_button = tk.Button(text='Rogue AP',command=rogueAP, font=("Helvetica 12 bold"))
    terminal_button=tk.Button(text='Serial Terminal',command=start_terminal, font=("Helvetica 12 bold"))
    power_off_button = tk.Button(text='Power Off',command=lambda: send_command1('shutdown -h now'), font=("Helvetica 12 bold"))

    image2 = Image.open("img/CYBV498.png")
    image2 = image2.resize((150, 130), Image.ANTIALIAS)    
    test2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image=test2)
    
    label2.grid(row=0,column=0,padx=5, pady=10, ipadx=15, ipady=10)
    start_Assessment_button.grid(row=1,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    rogueAP_button.grid(row=2,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    terminal_button.grid(row=3,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    power_off_button.grid(row=4,column=0,padx=5, pady=5, ipadx=5, ipady=5)
    
    menuBar = tk.Menu(root)
    toolsMenu = tk.Menu(menuBar, tearoff=0)
    
    toolsMenu.add_command(label='About', command=menuAbout, underline=0)
    toolsMenu.add_separator()
    toolsMenu.add_command(label='Exit', command=root.destroy)
    menuBar.add_cascade(label='Help', menu=toolsMenu, underline=0)  
    root.config(menu=menuBar)  # menu ends    
    
    try:
        #pass
        ser = serial.Serial(serial_port, baud_rate, timeout=5)
    except:
        messagebox.showinfo("ERROR", "Unable to connect via serial")
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", close_connection)    
    
    root.mainloop()    