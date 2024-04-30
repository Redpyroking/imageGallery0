import os
from flask import Flask, render_template, Response
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__, template_folder='templates')

# Directory where your images are stored
IMAGE_DIR = 'static/matching_face'

class ImageEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        send_gallery()

def get_gallery_html():
    images = os.listdir(IMAGE_DIR)
    return render_template('gallery.html', images=images)

def send_gallery():
    def event_stream():
        html = get_gallery_html()
        yield f"data: {html}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/')
def index():
    return get_gallery_html()

@app.route('/stream')
def stream():
    return send_gallery()

if __name__ == '__main__':
    observer = Observer()
    event_handler = ImageEventHandler()
    observer.schedule(event_handler, IMAGE_DIR, recursive=False)
    observer.start()

    app.run(debug=True)