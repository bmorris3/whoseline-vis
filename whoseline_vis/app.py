import os
from flask import Flask, render_template, request, redirect, flash
from bokeh.embed import server_document
from werkzeug.utils import secure_filename

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir,
                                'whoseline'))
from whoseline import linelist_paths


if os.getenv('USER') == 'dotastro':
    host = 'dotastro.muna.net'
    remote_port = 5006
else:
    host = '127.0.0.1'
    remote_port = 8000

app_port = 8000

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'fits', 'csv'])

app = Flask(__name__)
app.secret_key = '\x14\x9a\xd3AZ\xc2\x15\xe7\xbf\x08\x8c\xdb\xea\x8c\xa8\n\xb6U\xf0\xc7\x95~\xc1W'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    script = None

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            script = server_document("http://{}:{}/plot".format(host, 5006),
                                     arguments={
                                         'data_path': file_path,
                                         'line_list': request.form['specSelect'],
                                         'max_wave': request.form['waveMax'],
                                         'min_wave': request.form['waveMin']
                                     })

    return render_template('index.html', plot_script=script,
                           linelists=list(linelist_paths.keys()))
