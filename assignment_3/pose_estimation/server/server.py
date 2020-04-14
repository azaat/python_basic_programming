import os
from pose_estimation import draw_points
from flask import Flask, request, jsonify
from flask_cors import CORS

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_img', methods=['POST'])
def upload_img():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({
            'success': False,
            'message': 'No file part in the request'
        })
        resp.status_code = 400
        return resp
    file = request.files['file']

    if allowed_file(file.filename):
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.isdir(upload_dir):
            os.mkdir(upload_dir)
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(img_path)
        try:
            result = draw_points(img_path)
            resp = jsonify({
                'success': True,
                'image': result
            })
            return resp
        except ValueError:
            resp = jsonify({
                'success': False,
                'message': "Input image is corrupt"
            })
            resp.status_code = 400
            return resp
        finally:
            os.remove(img_path)
    else:
        resp = jsonify({
            'success': False,
            'message': 'Wrong file extension'
        })
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run()
