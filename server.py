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
        if 'file' in request.files:
            try:
                filename = upload_files.save(request.files['file'])
                return jsonify({'filename': filename})
            except UploadNotAllowed:
                print('Given extension is not in the allowed list.')
                # status codes http://www.restapitutorial.com/httpstatuscodes.html
                return jsonify({"error": 'Given extension is not in the allowed list'}), 415

        return jsonify('No file found in the request'), 400

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
