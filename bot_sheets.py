import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

def initialize_sheets():
    
    gc = gspread.authorize(credentials)
    sheet = gc.open('Clodhopper Bot')
    print ("Sheet authorization successful.")

    initialize_sheets.clodhopper_error_sheet = sheet.worksheet("Clod Errors")
    initialize_sheets.clodhopper_request_sheet = sheet.worksheet("Clod Requests")
    initialize_sheets.eufloria_error_sheet = sheet.worksheet("Eufloria Errors")
    initialize_sheets.eufloria_request_sheet = sheet.worksheet("Eufloria Requests")

    # functions are also objects, so with dynamic typing, they can allow a very hacky way to access local vars from other functions

    print ("Opening sheets successful.")

def send_new_report (user, report_content, reported_game, report_type):
    
    if reported_game == 'Clodhoppers':
        if report_type == 'bug':
            working_sheet = initialize_sheets.clodhopper_error_sheet
        
        elif report_type == 'request':
            working_sheet = initialize_sheets.clodhopper_request_sheet
            
    if reported_game == 'Eufloria':
        if report_type == 'bug':
            working_sheet = initialize_sheets.eufloria_error_sheet

        elif report_type == 'request':
            working_sheet = initialize_sheets.eufloria_request_sheet

    try:
        ticket_number = int(working_sheet.acell('B1').value)
    except Exception as e:
        initialize_sheets()
        ticket_number = int(working_sheet.acell('B1').value)

    finally:
        date = time.strftime("%d %b %Y", time.gmtime())
        entry = [user, date, str(ticket_number), report_content]

        working_sheet.append_row(entry)    
        working_sheet.update_acell('B1', str(ticket_number + 1))

    return ticket_number