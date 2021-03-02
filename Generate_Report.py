from datetime import datetime
import os 
from xhtml2pdf import pisa
import base64 

def generate_report():
    HTMLFILE = "Report_Template.html"
    print("This is the function to generate a report")
    # Need to convert the image to base64. 
    
    #writing HTML Content
    heading = '<h1> Automated Wireless Assessment Report <br> Gabriel Haab </h1>'
    subheading = '<h3> Sample Report for Placement </h3>'
    # Using .now() from datetime library to add Time stamp
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
    with open(HTMLFILE) as file:    
        html = file.read()
    html = html.replace('[Current_Time]', current_time)
    
    with open("my_image.jpeg", "rb") as img_file:
        my_image_string = base64.b64encode(img_file.read())    
    
    html = html.replace('[Information]','<img src="data:image/png;base64,' + str(my_image_string) + '"')
    # Concating everything to a single string
    
    '''
    with open('Report.html','w+') as file:
        file.write(html)    
    '''
    # Generate the PDF
    result_file = open("Report.pdf", "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(html,dest=result_file)
    result_file.close()

    os.startfile("Report.pdf")

if __name__ == '__main__':
    generate_report()  