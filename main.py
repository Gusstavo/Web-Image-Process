import imghdr
import os

from flask import (Blueprint, Flask, abort, redirect, render_template, request,
                   send_from_directory, url_for, current_app)
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.route('/')
def index():
    files = os.listdir(current_app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@main.route('/', methods=['POST'])
def upload_files():
    #notif_id = int(request.form.get('notif_id'))
    #accept = int(request.form.get('accept'))

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(path)

        return render_template('methods.html', filename=path)
    else:
        return redirect(url_for('main.index'))

@main.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)

@main.errorhandler(413)
def too_large(e):
    return "File is too large", 413

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')
