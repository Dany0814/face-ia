# from codecs import Codec
# from http import client
# from multiprocessing.connection import Client
# # from capture import capture_and_save
from os import listxattr
from pydoc import classname, cli
from flask import Flask, render_template, send_from_directory, Response
# from flask_socketio import SocketIO
from pathlib import Path
from second import codefotos
from second import findEncodings
from camera import Camera
# from main import stream
import argparse, logging, logging.config, conf

logging.config.dictConfig(conf.dictConfig)
logger = logging.getLogger(__name__)

images = []
camera = Camera()
camera.run()

app = Flask(__name__)

@app.after_request
def add_header(r):
	"""
	Add headers to both force latest IE rendering or Chrome Frame,
	and also to cache the rendered page for 10 minutes
	"""
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers["Cache-Control"] = "public, max-age=0"
	return r

@app.route("/")
def entrypoint():
	logger.debug("Requested /")
	return render_template("index.html")

@app.route("/codefotos")
def namefotos():
    logger.debug("fotos codificadas")
    codefotos()
    return render_template("index.html")
def codelocal():    
    encodeListKnown = findEncodings(images)
    return render_template("index.html", encodeListKnown)

@app.route("/initcam/last")
def last_image():
	logger.debug("Requested last image")
	p = Path("initcam/last.png")
	if p.exists():
		r = "last.png"
	else:
		logger.debug("No last image")
		r = "not_found.jpeg"
	return send_from_directory("initcam",r)

def gen(camera):
	logger.debug("Starting stream")
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route("/stream")
def stream_page():
	logger.debug("Requested stream page")
	return render_template("stream.html")

@app.route("/video_feed")
def video_feed():
	return Response(gen(camera),
		mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__=="__main__":
	# socketio.run(app,host="0.0.0.0",port="3005",threaded=True)
	parser = argparse.ArgumentParser()
	parser.add_argument('-p','--port',type=int,default=3000, help="Running port")
	parser.add_argument("-H","--host",type=str,default='0.0.0.0', help="Address to broadcast")
	args = parser.parse_args()
	logger.debug("Starting server")
	app.run(host=args.host,port=args.port)