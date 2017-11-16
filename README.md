# whoseline-vis

Whose line is it anyway? A simple Python package for identifying spectral lines

# How to run a local instance of `whoseline-vis`
In one terminal, go to the `whoseline-vis` repository, and run:
```bash
bokeh serve whoseline_vis/plot.py --allow-websocket-origin=127.0.0.1:8000
```
and in another terminal, run: 
```bokeh
python run.py
```
While those two processes are running, open http://127.0.0.1:8000/ in a web browser. 

Then celebrate! 💃
