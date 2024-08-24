from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import plotly.express as px
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return redirect(url_for('upload_file'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('dashboard', filename=filename))
    return render_template('upload.html')

@app.route('/dashboard/<filename>')
def dashboard(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)

    # Assuming your CSV has categorical data you want to plot
    # Replace 'CategoryColumn' and 'ValueColumn' with actual column names from your CSV
    category_column = 'degree_level'
    value_column = 'age'

    # Create a bar chart using Plotly
    fig = px.bar(df, x=category_column, y=value_column, title=f"{category_column} vs {value_column}")

    # Convert Plotly figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('dashboard.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
