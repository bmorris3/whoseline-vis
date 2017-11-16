"""
Present an interactive spectrum explorer with slider widgets.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve sliders.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/slider

in your browser.

Built from example:
https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py
"""

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import widgetbox, column
from bokeh.models import ColumnDataSource, LabelSet, Slider
from bokeh.plotting import figure

from utils.io import read_file

# Get data passed in from flask
args = curdoc().session_context.request.arguments

data_path = next(iter(args.get('data_path', [''])), '')
line_list = next(iter(args.get('line_list', [''])), '')
min_wave = float(next(iter(args.get('min_wave', [0.0])), 0.0))
max_wave = float(next(iter(args.get('max_wave', [15000.0])), 150000))

##################################################################
# Use our mocked API for whoseline
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir,
                                'whoseline'))
from whoseline import query
import astropy.units as u


def render_plot():
    # Set up data
    spectrum = read_file(data_path.decode())
    wavelength = spectrum.wavelength
    flux = spectrum.flux
    flux /= flux.max()

    # Currently only implemented for table source "example"
    linelist = query(source=line_list.decode(),
                     wavelength_min=min_wave * u.Angstrom,
                     wavelength_max=max_wave * u.Angstrom)
    ##################################################################

    # Create object spectrum data source
    source = ColumnDataSource(data=dict(wavelength=wavelength, flux=flux))

    # Create line list label source
    lines = ColumnDataSource(data=dict(x=linelist.wavelength.value,
                                       top=np.zeros_like(linelist.priority),
                                       names=linelist.species))

    # Create a set of labels for each species
    labels = LabelSet(x='x', y='top', text='names', level='glyph',
                      x_offset=0, y_offset=0, source=lines, render_mode='canvas',
                      angle=np.pi/3)

    # Set up plot
    plot = figure(plot_height=600, plot_width=700, title="Example spectrum",
                  tools="wheel_zoom,box_zoom,pan,reset,save",
                  x_range=[wavelength.min(), wavelength.max()],
                  y_range=[0, flux.max()], responsive=True)

    # Add vertical bars for each line in the line list
    plot.vbar(x='x', top='top', source=lines,
              color="black", width=0.01, bottom=0, alpha=0.5)

    # Add the actual spectrum
    plot.line('wavelength', 'flux', source=source, line_width=1, line_alpha=0.8)

    # Set up widgets
    nlines_slider = Slider(title="more/less lines", value=10, start=0,
                           end=100, step=0.01)

    rv_offset = Slider(title="RV offset", value=0, start=-100,
                       end=100, step=0.01)

    def on_slider_change(attrname, old, new):
        n_lines_scale = nlines_slider.value
        rv_offset_val = rv_offset.value
        n_lines = int(n_lines_scale/100 * len(linelist.wavelength))
        condition = linelist.priority >= np.sort(linelist.priority)[-n_lines]
        label_wavelengths = linelist.wavelength.value
        label_height = condition.astype(float) * flux.max()

        label_names = linelist.species.copy()
        # Blank out some labels
        label_names[~condition] = ''

        lines.data = dict(x=label_wavelengths + rv_offset_val,
                          top=0.9*label_height*plot.y_range.end,
                          names=label_names)


    for w in [nlines_slider, rv_offset]:
        w.on_change('value', on_slider_change)

    # Set up layouts and add to document
    inputs = widgetbox(nlines_slider, rv_offset)  #nlines_text
    plot.add_layout(labels)

    curdoc().add_root(column(inputs, plot, height=1000))
    curdoc().title = "Whose line is it anyway"


if data_path:
    render_plot()