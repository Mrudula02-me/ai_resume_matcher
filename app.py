from flask import Flask, render_template, request
from job_api import fetch_jobs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form['job_query']
    jobs = fetch_jobs(query)
    return render_template('results.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
