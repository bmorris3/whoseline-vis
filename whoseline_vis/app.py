from flask import Flask, render_template
from bokeh.embed import server_document
import numpy as np


app = Flask(__name__)


@app.route('/')
def home():
    script = server_document("http://localhost:5006/plot",
                             arguments={'mult': np.random.randint(4)})

    return render_template('index.html', plot_script=script)
