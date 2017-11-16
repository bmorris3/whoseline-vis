import os
from flask import Flask, render_template, request, redirect, flash, url_for
from bokeh.embed import server_document
import numpy as np
from werkzeug.utils import secure_filename
from .forms import SpectrumUploadForm
from whoseline import linelist_paths


UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt'])

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
        print(request.form)
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

            script = server_document("http://localhost:5006/plot",
                                     arguments={
                                         'data_path': file_path,
                                         'line_list': request.form['specSelect'],
                                         'max_wave': request.form['waveMax'],
                                         'min_wave': request.form['waveMin']
                                     })

    return render_template('index.html', plot_script=script,
                           linelists=list(linelist_paths.keys()))
