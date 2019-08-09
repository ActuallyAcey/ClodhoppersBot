import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

gc = gspread.authorize(credentials)
sheet = gc.open('Clodhopper Bot')
print ("Sheet authorization successful.")

clodhopper_error_sheet = sheet.get_worksheet(0)
clodhopper_request_sheet = sheet.get_worksheet(1)
eufloria_error_sheet = sheet.get_worksheet(2)
eufloria_request_sheet = sheet.get_worksheet(3)

print ("Opening sheets successful.")

def send_error_entry(user : str, content : str, game_id):
    #Entry structure: Username/Timestamp/Ticket/Content
    if game_id == 1:
        error_sheet = clodhopper_error_sheet
    elif game_id == 2:
        error_sheet = eufloria_error_sheet
    
    error_ticket_number = int(error_sheet.acell('B1').value)
    date = time.strftime("%d %b %Y", time.gmtime())
    entry = [user, date, str(error_ticket_number), content]

    error_sheet.append_row(entry)
    
    error_sheet.update_acell('B1', str(error_ticket_number + 1))

def send_request_entry(user : str, content : str, game_id):
    #Entry structure: Username/Timestamp/Ticket/Content
    if game_id == 1:
        error_sheet = clodhopper_error_sheet
    elif game_id == 2:
        error_sheet = eufloria_error_sheet

    request_ticket_number = int(request_sheet.acell('B1').value)
    date = time.strftime("%d %b %Y", time.gmtime())
    entry = [user, date, str(error_ticket_number), content]
    
    request_sheet.append_row(entry)
    
    request_sheet.update_acell('B1', str(request_ticket_number + 1))

