import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['http://spreasheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

gc = gspread.authorize(credentials)
