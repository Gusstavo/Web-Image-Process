#!/usr/bin/python3
# pylint: disable=missing-docstring,too-few-public-methods,invalid-name

import os
import shutil
import sys

from flask import Flask

app = Flask(__name__)

def create_app():
    
    app.config['SECRET_KEY'] = "8sd4fq19hg4yu1ioo9533c9cv4b1"
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    app.config['UPLOAD_PATH'] = 'static/uploaded_images'
    remove_all_images(app.config['UPLOAD_PATH'])

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    sys.stdout.flush()
    app.run(host='127.0.0.1', port=5000, use_reloader=False, debug=True)


def remove_all_images(dir):
    folder = dir
    for filename in os.listdir(folder):
        if ".gitkeep" in filename:
            continue
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
    create_app()
