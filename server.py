from flask import Flask, request, jsonify
from flask_uploads import configure_uploads, UploadSet, UploadNotAllowed
from flask_script import Manager
from flask_cors import CORS

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config['DEBUG'] = True
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
app.config['UPLOADS_DEFAULT_URL'] = 'http://127.0.0.1:5000/'
app.url_map.strict_slashes = False

upload_files = UploadSet('files', ('csv', 'zip', 'png', 'jpg', 'jpeg', 'pdf', 'log', 'txt'))

# Flask-upload configuration
configure_uploads(app, upload_files)


@app.route('/uploads', methods=['POST'])
def upload():

    if 'file' in request.files:

        filenames = []

        for file_request in request.files.getlist("file"):
            try:
                filename = upload_files.save(file_request)
                filenames.append(filename)
            except UploadNotAllowed:
                print('Given extension is not in the allowed list.')
                # status codes http://www.restapitutorial.com/httpstatuscodes.html
                return jsonify({"error": 'Given extension is not in the allowed list'}), 415

        return jsonify({'filenames': filenames})

    return jsonify({'state': 'No file found in the request'}), 400


@app.route('/form-data', methods=['POST'])
def form_data():

    params = request.get_json()

    if 'filenames' not in params or not params['filenames']:
        return jsonify('Filename must be provided'), 406

    return jsonify(params)


manager = Manager(app)

if __name__ == "__main__":
    manager.run()
