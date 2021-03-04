from datetime import datetime
import os 
from xhtml2pdf import pisa
import base64 
import csv 
import pandas as pd
from mac_vendor_lookup import MacLookup


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
    
def compare_channels(data,target):
    all_channels = [1,2,3,4,5,6,7,8,9,10,11,12]
    df=pd.DataFrame.from_dict(data,orient='index')
    
    hue = df[2].value_counts()
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
    fig.savefig('Compare_Channels.jpeg')
    print("done")
    
def generate_report(selected_network):
    # Gattering data for report: 
    
    compare_channels(data, selected_network['Channel'])
    
    HTMLFILE = "Report_Template.html"
    print("This is the function to generate a report")
    # Need to convert the image to base64. 
    
    #writing HTML Content
    heading = '<h1> Automated Wireless Assessment Report <br> Gabriel Haab </h1>'
    subheading = '<h3> Sample Report for Placement </h3>'
    # Using .now() from datetime library to add Time stamp
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y at %H:%M:%S")
    with open(HTMLFILE) as file:    
        html = file.read()
    html = html.replace('[Current_Time]', current_time)
    
    if "WEP" in selected_network['Privacy']:
        encryption_recomendation = "WEP encryption is vulnerable to reverse engineer attacks, therefore it is recommended to update it to WPA2 or WPA3"
        performed_tasks = "<ul> <li>IV Packet Capture</li><li>Korek ChopChop attack</li><li>Reverse Engineering attack</li></ul>"  
        
    if selected_network['Privacy'] == "WPA":
        encryption_recomendation = "Although WPA offers more security than WEP, it is recommmended to update it to WPA2 or WPA3."
        performed_tasks = "<ul> <li>WPA handshake capture</li><li>Denial of Service</li><li>Network Scanning</li></ul>"  
        
    if "WPA2" in selected_network['Privacy']:
        encryption_recomendation = "WPA2 offers a good ammount of security as long you are using a secure wireless password"
        performed_tasks = "<ul> <li>WPA handshake capture</li><li>Denial of Service</li><li>Network Scanning</li></ul>"    
       
    """
    ================================================================
    Information Section:
    ================================================================
    """
    information = ""
    information += "Channel/Frequency Analysis (Red dot is the targeted device.): "
    
    with open("Compare_Channels.jpeg", "rb") as img_file:
        Compare_Channels = base64.b64encode(img_file.read())        
    information += '<img src="data:image/png;base64,' + str(Compare_Channels) + '">'
    img_file.close()
    
    information += "Connected Devices: "
    with open("Connected_Devices.jpeg", "rb") as img_file:
        Connected_Devices = base64.b64encode(img_file.read())        
    information += '<img src="data:image/png;base64,' + str(Connected_Devices) + '">'
    
    """
    ================================================================
    Vulnerabilities Section:
    ================================================================
    """
    vulnerabilities = "Based on the gathered information..."
    
    """
    ================================================================
    Recomendations Section:
    ================================================================
    """
    recomendations_list = []
    if "WEP" in selected_network['Privacy']:
        recomendations_list.append("Change the encryption from WEP to WPA2 or WPA3")  
        recomendations_list.append("Change the network to a less congestionated one.")
        
    if selected_network['Privacy'] == "WPA":
        recomendations_list.append("Change the encryption from WPA to WPA2 or WPA3") 
        recomendations_list.append("Make sure the wireless follows strong password recomendations")
        recomendations_list.append("Make sure the wireless name is unique")
        recomendations_list.append("Change the network to a less congestionated one.")
        
    if "WPA2" in selected_network['Privacy']:
        recomendations_list.append("Make sure the wireless follows strong password recomendations")
        recomendations_list.append("Make sure the wireless name is unique")
        recomendations_list.append("Change the network channel to a less congestionated one.")
    
    recomendations = "<ul>"
    for i in recomendations_list:
        recomendations += '<li>' + i + '</li>'
    recomendations += '</ul>'

    """
    ================================================================
    Fill out the report by replacing tags:
    ================================================================
    """
    html = html.replace('[Information]',information)
    html = html.replace('[Vulnerabilities]',vulnerabilities)
    html = html.replace('[Recomendations]',recomendations)
    html = html.replace('[Encryption_Recommendation]',encryption_recomendation)
    html = html.replace('[Performed_tasks]',performed_tasks)
    
    
    html = html.replace('[ESSID]', selected_network['ESSID'])
    html = html.replace('[Encryption]', selected_network['Privacy'])
    try:
        html = html.replace('[BSSID]', selected_network['BSSID'] + "(" + MacLookup().lookup(str(selected_network['BSSID'])) + ")")
    except:
        html = html.replace('[BSSID]', selected_network['BSSID'])
    html = html.replace('[Channel]', selected_network['Channel'])
    
    # Generate the PDF
    result_file = open("Report.pdf", "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(html,dest=result_file)
    result_file.close()

    os.startfile("Report.pdf")


def selectnetwork (data,ESSID):
    
    selected_network = {}
    selected_network['ESSID'] = ESSID
    selected_network['Privacy'] = data[ESSID][0]
    selected_network['BSSID'] = data[ESSID][1]
    selected_network['Channel'] = data[ESSID][2]
    print(selected_network)
    
    return selected_network

if __name__ == '__main__':
    data = read_csv()
    ESSID = "Jenga_2.4"
    selected_network = selectnetwork(data,ESSID)

    generate_report(selected_network)  