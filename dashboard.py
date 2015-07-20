from flask import Blueprint, render_template, request, session, flash, redirect, url_for, current_app
from models import Participant

from sqlalchemy.exc import SQLAlchemyError
from database import db


dashboard = Blueprint('dashboard', __name__,
                        template_folder='dashboard/templates', static_folder='dashboard/static')

fig = '\n\n<style>\n\n</style>\n\n<div id="fig_el149044349181609087646510"></div>\n<script>\nfunction mpld3_load_lib(url, callback){\n  var s = document.createElement(\'script\');\n  s.src = url;\n  s.async = true;\n  s.onreadystatechange = s.onload = callback;\n  s.onerror = function(){console.warn("failed to load library " + url);};\n  document.getElementsByTagName("head")[0].appendChild(s);\n}\n\nif(typeof(mpld3) !== "undefined" && mpld3._mpld3IsLoaded){\n   // already loaded: just create the figure\n   !function(mpld3){\n       \n       mpld3.draw_figure("fig_el149044349181609087646510", {"axes": [{"xlim": [0.0, 100.0], "yscale": "linear", "axesbg": "#FFFFFF", "texts": [], "zoomable": true, "images": [], "xdomain": [0.0, 100.0], "ylim": [-50.0, 250.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 12.0, "position": "bottom", "nticks": 6, "tickvalues": null}, {"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 12.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [{"color": "#0000FF", "yindex": 1, "coordinates": "data", "dasharray": "10,0", "zorder": 2, "alpha": 1, "xindex": 0, "linewidth": 1.0, "data": "data01", "id": "el14904434919120"}], "markers": [], "id": "el14904435714896", "ydomain": [-50.0, 250.0], "collections": [], "xscale": "linear", "bbox": [0.125, 0.099999999999999978, 0.77500000000000002, 0.80000000000000004]}], "height": 480.0, "width": 640.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}], "data": {"data01": [[0.0, 10.0], [1.0, -18.0], [2.0, -3.0], [3.0, -8.0], [4.0, 23.0], [5.0, 3.0], [6.0, 15.0], [7.0, 22.0], [8.0, 36.0], [9.0, 11.0], [10.0, 30.0], [11.0, 33.0], [12.0, 30.0], [13.0, 38.0], [14.0, 42.0], [15.0, 47.0], [16.0, 32.0], [17.0, 45.0], [18.0, 16.0], [19.0, 27.0], [20.0, 52.0], [21.0, 53.0], [22.0, 36.0], [23.0, 66.0], [24.0, 54.0], [25.0, 36.0], [26.0, 66.0], [27.0, 42.0], [28.0, 44.0], [29.0, 48.0], [30.0, 45.0], [31.0, 77.0], [32.0, 73.0], [33.0, 75.0], [34.0, 87.0], [35.0, 71.0], [36.0, 77.0], [37.0, 63.0], [38.0, 73.0], [39.0, 58.0], [40.0, 83.0], [41.0, 66.0], [42.0, 96.0], [43.0, 95.0], [44.0, 95.0], [45.0, 77.0], [46.0, 99.0], [47.0, 100.0], [48.0, 95.0], [49.0, 112.0], [50.0, 91.0], [51.0, 104.0], [52.0, 93.0], [53.0, 104.0], [54.0, 102.0], [55.0, 105.0], [56.0, 106.0], [57.0, 130.0], [58.0, 125.0], [59.0, 105.0], [60.0, 136.0], [61.0, 117.0], [62.0, 128.0], [63.0, 136.0], [64.0, 135.0], [65.0, 130.0], [66.0, 139.0], [67.0, 117.0], [68.0, 128.0], [69.0, 126.0], [70.0, 138.0], [71.0, 124.0], [72.0, 155.0], [73.0, 161.0], [74.0, 131.0], [75.0, 158.0], [76.0, 135.0], [77.0, 168.0], [78.0, 162.0], [79.0, 175.0], [80.0, 154.0], [81.0, 146.0], [82.0, 176.0], [83.0, 175.0], [84.0, 187.0], [85.0, 176.0], [86.0, 155.0], [87.0, 183.0], [88.0, 180.0], [89.0, 168.0], [90.0, 175.0], [91.0, 178.0], [92.0, 188.0], [93.0, 196.0], [94.0, 185.0], [95.0, 183.0], [96.0, 209.0], [97.0, 195.0], [98.0, 182.0], [99.0, 214.0]]}, "id": "el14904434918160"});\n   }(mpld3);\n}else if(typeof define === "function" && define.amd){\n   // require.js is available: use it to load d3/mpld3\n   require.config({paths: {d3: "https://mpld3.github.io/js/d3.v3.min"}});\n   require(["d3"], function(d3){\n      window.d3 = d3;\n      mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.2.js", function(){\n         \n         mpld3.draw_figure("fig_el149044349181609087646510", {"axes": [{"xlim": [0.0, 100.0], "yscale": "linear", "axesbg": "#FFFFFF", "texts": [], "zoomable": true, "images": [], "xdomain": [0.0, 100.0], "ylim": [-50.0, 250.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 12.0, "position": "bottom", "nticks": 6, "tickvalues": null}, {"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 12.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [{"color": "#0000FF", "yindex": 1, "coordinates": "data", "dasharray": "10,0", "zorder": 2, "alpha": 1, "xindex": 0, "linewidth": 1.0, "data": "data01", "id": "el14904434919120"}], "markers": [], "id": "el14904435714896", "ydomain": [-50.0, 250.0], "collections": [], "xscale": "linear", "bbox": [0.125, 0.099999999999999978, 0.77500000000000002, 0.80000000000000004]}], "height": 480.0, "width": 640.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}], "data": {"data01": [[0.0, 10.0], [1.0, -18.0], [2.0, -3.0], [3.0, -8.0], [4.0, 23.0], [5.0, 3.0], [6.0, 15.0], [7.0, 22.0], [8.0, 36.0], [9.0, 11.0], [10.0, 30.0], [11.0, 33.0], [12.0, 30.0], [13.0, 38.0], [14.0, 42.0], [15.0, 47.0], [16.0, 32.0], [17.0, 45.0], [18.0, 16.0], [19.0, 27.0], [20.0, 52.0], [21.0, 53.0], [22.0, 36.0], [23.0, 66.0], [24.0, 54.0], [25.0, 36.0], [26.0, 66.0], [27.0, 42.0], [28.0, 44.0], [29.0, 48.0], [30.0, 45.0], [31.0, 77.0], [32.0, 73.0], [33.0, 75.0], [34.0, 87.0], [35.0, 71.0], [36.0, 77.0], [37.0, 63.0], [38.0, 73.0], [39.0, 58.0], [40.0, 83.0], [41.0, 66.0], [42.0, 96.0], [43.0, 95.0], [44.0, 95.0], [45.0, 77.0], [46.0, 99.0], [47.0, 100.0], [48.0, 95.0], [49.0, 112.0], [50.0, 91.0], [51.0, 104.0], [52.0, 93.0], [53.0, 104.0], [54.0, 102.0], [55.0, 105.0], [56.0, 106.0], [57.0, 130.0], [58.0, 125.0], [59.0, 105.0], [60.0, 136.0], [61.0, 117.0], [62.0, 128.0], [63.0, 136.0], [64.0, 135.0], [65.0, 130.0], [66.0, 139.0], [67.0, 117.0], [68.0, 128.0], [69.0, 126.0], [70.0, 138.0], [71.0, 124.0], [72.0, 155.0], [73.0, 161.0], [74.0, 131.0], [75.0, 158.0], [76.0, 135.0], [77.0, 168.0], [78.0, 162.0], [79.0, 175.0], [80.0, 154.0], [81.0, 146.0], [82.0, 176.0], [83.0, 175.0], [84.0, 187.0], [85.0, 176.0], [86.0, 155.0], [87.0, 183.0], [88.0, 180.0], [89.0, 168.0], [90.0, 175.0], [91.0, 178.0], [92.0, 188.0], [93.0, 196.0], [94.0, 185.0], [95.0, 183.0], [96.0, 209.0], [97.0, 195.0], [98.0, 182.0], [99.0, 214.0]]}, "id": "el14904434918160"});\n      });\n    });\n}else{\n    // require.js not available: dynamically load d3 & mpld3\n    mpld3_load_lib("https://mpld3.github.io/js/d3.v3.min.js", function(){\n         mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.2.js", function(){\n                 \n                 mpld3.draw_figure("fig_el149044349181609087646510", {"axes": [{"xlim": [0.0, 100.0], "yscale": "linear", "axesbg": "#FFFFFF", "texts": [], "zoomable": true, "images": [], "xdomain": [0.0, 100.0], "ylim": [-50.0, 250.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 12.0, "position": "bottom", "nticks": 6, "tickvalues": null}, {"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 12.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [{"color": "#0000FF", "yindex": 1, "coordinates": "data", "dasharray": "10,0", "zorder": 2, "alpha": 1, "xindex": 0, "linewidth": 1.0, "data": "data01", "id": "el14904434919120"}], "markers": [], "id": "el14904435714896", "ydomain": [-50.0, 250.0], "collections": [], "xscale": "linear", "bbox": [0.125, 0.099999999999999978, 0.77500000000000002, 0.80000000000000004]}], "height": 480.0, "width": 640.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}], "data": {"data01": [[0.0, 10.0], [1.0, -18.0], [2.0, -3.0], [3.0, -8.0], [4.0, 23.0], [5.0, 3.0], [6.0, 15.0], [7.0, 22.0], [8.0, 36.0], [9.0, 11.0], [10.0, 30.0], [11.0, 33.0], [12.0, 30.0], [13.0, 38.0], [14.0, 42.0], [15.0, 47.0], [16.0, 32.0], [17.0, 45.0], [18.0, 16.0], [19.0, 27.0], [20.0, 52.0], [21.0, 53.0], [22.0, 36.0], [23.0, 66.0], [24.0, 54.0], [25.0, 36.0], [26.0, 66.0], [27.0, 42.0], [28.0, 44.0], [29.0, 48.0], [30.0, 45.0], [31.0, 77.0], [32.0, 73.0], [33.0, 75.0], [34.0, 87.0], [35.0, 71.0], [36.0, 77.0], [37.0, 63.0], [38.0, 73.0], [39.0, 58.0], [40.0, 83.0], [41.0, 66.0], [42.0, 96.0], [43.0, 95.0], [44.0, 95.0], [45.0, 77.0], [46.0, 99.0], [47.0, 100.0], [48.0, 95.0], [49.0, 112.0], [50.0, 91.0], [51.0, 104.0], [52.0, 93.0], [53.0, 104.0], [54.0, 102.0], [55.0, 105.0], [56.0, 106.0], [57.0, 130.0], [58.0, 125.0], [59.0, 105.0], [60.0, 136.0], [61.0, 117.0], [62.0, 128.0], [63.0, 136.0], [64.0, 135.0], [65.0, 130.0], [66.0, 139.0], [67.0, 117.0], [68.0, 128.0], [69.0, 126.0], [70.0, 138.0], [71.0, 124.0], [72.0, 155.0], [73.0, 161.0], [74.0, 131.0], [75.0, 158.0], [76.0, 135.0], [77.0, 168.0], [78.0, 162.0], [79.0, 175.0], [80.0, 154.0], [81.0, 146.0], [82.0, 176.0], [83.0, 175.0], [84.0, 187.0], [85.0, 176.0], [86.0, 155.0], [87.0, 183.0], [88.0, 180.0], [89.0, 168.0], [90.0, 175.0], [91.0, 178.0], [92.0, 188.0], [93.0, 196.0], [94.0, 185.0], [95.0, 183.0], [96.0, 209.0], [97.0, 195.0], [98.0, 182.0], [99.0, 214.0]]}, "id": "el14904434918160"});\n            })\n         });\n}\n</script>'




@dashboard.route('/', methods=['GET'])
def view():
    if not session.get('logged_in'):
        flash("You must log in to view the experimenter dashboard.")
        return redirect(url_for('.login'))
    else:

    	import numpy as np

    	from bokeh.plotting import figure, output_file
    	from bokeh.embed import file_html
    	from bokeh.resources import CDN

    	N = 4000
    	x = np.random.random(size=N) * 100
    	y = np.random.random(size=N) * 100
    	radii = np.random.random(size=N) * 1.5
    	colors = ["#%02x%02x%02x" % (r, g, 150) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]

    	output_file("color_scatter.html", title="color_scatter.py example", mode="cdn")

    	TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

    	p = figure(tools=TOOLS, x_range=(0,100), y_range=(0,100))

    	p.circle(x,y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)

    	fig = file_html(p, CDN, "dashboard")

    	return render_template('view.html', fig=fig)


@dashboard.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != current_app.config['DASHBOARD_PASS']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('.view'))
    return render_template('login.html', error=error)

@dashboard.route('/message')
def message():
    return render_template('layout.html')


@dashboard.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('.message'))