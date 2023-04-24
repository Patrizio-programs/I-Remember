import gspread
import uuid
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='template')

# Authenticate with the Google Sheets API using the JSON key file
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('Flask test Database').sheet1

# Define the index page route
@app.route('/')
def index():
    data = sheet.get_all_values()
    return render_template('index.html', data=data)

# Define the form submission route
@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data
    name = request.form['name']
    message = request.form['message']
    
    # Generate a unique ID for the note
    note_id = str(uuid.uuid4().hex)[:4]
    
    # Append the data to another row in the Google Sheet
    row = [note_id, name, message]
    sheet.append_row(row)
    
    # Redirect back to the index page
    return redirect('/')


@app.route('/delete/<note_id>')
def delete(note_id):
    # Get all the data from the sheet
    data = sheet.get_all_values()
    
    # Find the row index of the note with the given ID
    row_index = None
    for i, row in enumerate(data):
        if row[0] == note_id:
            row_index = i + 1  # Adjust for 1-based index in Google Sheets
            break
    
    # If the row was found, delete it
    if row_index is not None:
        sheet.delete_row(row_index)
    
    # Redirect back to the index page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
