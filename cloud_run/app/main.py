import os
import subprocess
import time
import base64
from flask import Flask, request, jsonify
import logging

OUT_FOLDER = '/tmp'

app = Flask(__name__)


def convert_to_pdf(content):
    """converts docx file to
    :param content - binary content of docx file
    :return json response with fields pdf_content and error
    """
    filename = 'tmp_{}.docx'.format(int(time.time()))
    with open(filename, 'wb') as f:
        f.write(content)

    cmd = "libreoffice --headless --convert-to pdf {}".format(filename).split(' ')
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    error = stderr.decode('utf8')

    if error:
        os.remove(filename)
        logging.error(error)
        return jsonify({'error': error, 'pdf_content': ''}), 404
    else:
        out_filename = filename.replace('.docx', '.pdf')
        with open(out_filename, 'rb') as fo:
            out_content = fo.read()
            os.remove(out_filename)
            os.remove(filename)
            content_encoded = base64.b64encode(out_content)
            return jsonify({'pdf_content': str(content_encoded, 'utf8'), 'error': ''})


@app.route('/', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':

        data = request.get_json()
        docx_content_tmp = data.get('docx_content', '')
        docx_content = base64.b64decode(docx_content_tmp)
        resp = convert_to_pdf(docx_content)
        return resp
    else:
        return jsonify({'error': 'use POST method'})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
