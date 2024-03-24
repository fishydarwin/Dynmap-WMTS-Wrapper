import io
from flask import Flask, Response, render_template, request, send_file, url_for
from markupsafe import escape
from dwmtsw.util.config_parser import DWMTSWConfigParser
from dwmtsw.entity.dynmap_tile import DynmapTile
from dwmtsw.entity.dynmap_configuration import DynmapConfiguration

DWMTSWConfigParser.init("config.cfg")
config = DWMTSWConfigParser.get_config()
app = Flask(__name__)

@app.route("/")
def index():
    print("Index")
    url_for('static', filename='index.css')
    url_for('static', filename='map.png')
    return render_template('index.html')

#http://opengeospatial.github.io/e-learning/wmts/text/operations.html
@app.route('/GetCapabilities')
def get_capabilities():
    print("GetCapabilities")
    return Response(DynmapConfiguration.get_capabilities(url = config['DYNMAP']['url']), 
                    mimetype="xml")

# https://github.com/KhaledSharif/SimpleWMTS/blob/master/backend/api.py
@app.route('/GetTile')
def get_tile():
    print("GetTile")
    required_parameters = [
        'tilematrixset',
        'tilematrix',
        'tilecol',
        'tilerow',
    ]
    request_args = {k.lower():v for k, v in request.args.items()}
    required_parameters = {k:request_args[k] for k in required_parameters}

    integers = ["tilematrix", "tilecol", "tilerow"]
    for i in integers:
        required_parameters[i] = int(required_parameters[i])
    
    return send_file(
        io.BytesIO(DynmapTile(url = config['DYNMAP']['url'],
                              world = required_parameters["tilematrixset"],
                              zoom = required_parameters["tilematrix"], 
                              x = required_parameters["tilecol"],
                              y = required_parameters["tilerow"]).get_tile()
                   ),
        mimetype='image/jpg')
