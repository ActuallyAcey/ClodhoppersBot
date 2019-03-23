import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import gmtime, strftime 
import time

scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

gc = gspread.authorize(credentials)
sheet = gc.open('Clodhopper Bot')
print ("Sheet authorization successful.")

error_sheet = sheet.get_worksheet(0)
print ("Opening sheets successful.")

def send_error_entry(user : str, content : str):
    #Entry structure: Username/Timestamp/Ticket/Content
    error_ticket_number = int(error_sheet.acell('B1').value)
    date = time.strftime("%d %b %Y", time.gmtime())
    entry = [user, date, f'{error_ticket_number}', content]
    error_sheet.append_row(entry)
    
    error_sheet.update_acell('B1', str(error_ticket_number + 1))

