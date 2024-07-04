from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
from allocation import allocate_rooms

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        group_file = request.files['group_file']
        hostel_file = request.files['hostel_file']
        
        group_filepath = os.path.join(app.config['UPLOAD_FOLDER'], group_file.filename)
        hostel_filepath = os.path.join(app.config['UPLOAD_FOLDER'], hostel_file.filename)
        
        group_file.save(group_filepath)
        hostel_file.save(hostel_filepath)
        
        allocation_df = allocate_rooms(group_filepath, hostel_filepath)
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'room_allocation.csv')
        allocation_df.to_csv(output_filepath, index=False)
        
        return send_file(output_filepath, as_attachment=True, download_name='room_allocation.csv')

if __name__ == '__main__':
    app.run(debug=True)
