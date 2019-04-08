from flask import Flask, request, Response
from flask_cors import CORS
from flask import render_template, jsonify
import uuid
import os
import requests
import time
import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def front_end():
    return render_template('upload_file_json.html')

@app.route('/test')
def test():
    return "hello world! this is for all the face services"

@app.route('/upload', methods=['POST'])
def facial_result():
    file_receive = request.files['qqfile']
    # print(type(file))
    # file_name = str(uuid.uuid1())+'.'+file.filename.split('.')[-1]
    # file_path = os.path.join('./static/uploaded_file',file_name)

    tmp_save_path = './static/uploaded_file'
    os.makedirs(tmp_save_path, exist_ok=True)
    file_path = os.path.join(tmp_save_path, 'tmp.jpg')

    file_receive.save(file_path)

    response = {}
    t = time.time()
    # without slash it will redirect when call the recognition api, but why?
    for service, port, entrypoint, postname in \
            [('attribute', 8000, 'upload', 'qqfile'), ('expression', 8002, 'upload', 'qqfile'), ('recognition', 8004, 'auth/', 'image_file')]:

        file_upload = {f'{postname}': ('filename', open(file_path, 'rb'), 'image/jpeg')}

        try:
            res = requests.post(f'http://0.0.0.0:{port}/{entrypoint}', files=file_upload)

            json_data = json.loads(res.text)

            response.update({f'{service}_response': json_data})
        except:
            response.update({f'{service}_response': {}})

    response.update({'success': True})
    print(f'use time: {time.time()-t}')

    response = jsonify(response)
    os.remove(file_path)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)



  
