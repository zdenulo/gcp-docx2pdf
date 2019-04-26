import os
import subprocess
import time
from flask import Flask, request, jsonify
import logging

from google.cloud import storage

OUT_FOLDER = '/tmp'

app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(logging.DEBUG)

OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET')

gcs = storage.Client()


def convert_to_pdf(bucket_id, file_path):
    """converts docx file to
    :param bucket_id - name of the bucket
    :param file_path - path in bucket to file (excluding bucket name)
    :return response
    """

    bucket = gcs.bucket(bucket_id)
    blob = bucket.blob(file_path)

    filename = 'tmp_{}.docx'.format(int(time.time()))
    blob.download_to_filename(filename)
    app.logger.info("downloaded docx file {}".format(file_path))

    cmd = "libreoffice --headless --convert-to pdf {}".format(filename).split(' ')
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    error = stderr.decode('utf8')

    if error:
        os.remove(filename)
        logging.error(error)
        return jsonify({'error': error}), 404
    else:
        out_filename = file_path.replace('.docx', '.pdf')
        out_temp_file = filename.replace('.docx', '.pdf')

        out_bucket_name = os.environ['OUTPUT_BUCKET']
        out_bucket = gcs.bucket(out_bucket_name)
        out_blob = out_bucket.blob(out_filename)
        out_blob.upload_from_filename(out_temp_file)

        if os.path.exists(out_temp_file):
            os.remove(out_temp_file)
        if os.path.exists(filename):
            os.remove(filename)
        app.logger.info("uploaded file: {} to bucket {}".format(out_filename, out_bucket_name))
        return jsonify({'error': ''})


@app.route('/', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':
        app.logger.info(request.get_json())
        data = request.get_json()
        message = data['message']
        attributes = message['attributes']
        bucket_id = attributes['bucketId']
        object_id = attributes['objectId']
        resp = convert_to_pdf(bucket_id, object_id)
        return resp
    elif request.method == 'GET':
        return """use POST method with JSON body {"message": {"attributes": {"bucketId": "BUCKET-ID", "objectId": "FILE-PATH"}}}"""


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
