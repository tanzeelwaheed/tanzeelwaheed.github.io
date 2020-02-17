import os
from flask import Flask, render_template, request, url_for, Response
from werkzeug.utils import redirect
from camera import Camera

app = Flask(__name__)
camera = None

def get_camera():
    global camera
    if not camera:
        camera=Camera()
    return camera

@app.route('/')
def one():
    return render_template("index.html")
@app.route('/index.html')
def other():
    return render_template("index.html")
@app.route('/about.html')
def about():
    return render_template("about.html")
@app.route('/contact.html')
def contact():
    return render_template("contact.html")
@app.route('/help.html')
def help():
    return render_template("help.html")
@app.route('/example.html')
def exa():
    return render_template("example.html")

@app.route('/upload.html')
def index():
    return render_template("upload.html")

@app.route('/upload.html', methods=['POST','GET'])
def upl(APP_ROOT = os.path.dirname(os.path.abspath(__file__))):
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("upl"):
            filename = file.filename
            destination = "/" .join([target, filename])
            file.save(destination)
    return render_template("converted.html")

@app.route('/tp.html')
def root():
    return redirect(url_for('tp'))

@app.route('/tp')
def tp():
    return render_template('tp.html')

def gen(camera):
    while True:
        frame = camera.get_feed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/cam_video')
def camopen():
    camera = get_camera()
    return Response(gen(camera),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/converted.html')
def tk_img():
    camera = get_camera()
    stamp = camera.capture()
    return render_template("converted.html")

if __name__=="__main__":
    app.run()