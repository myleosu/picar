
#encoding:utf-8
#!/usr/bin/env python
import time
import os
import uuid
import base64
import threading
import requests
from flask.wrappers import Response
from werkzeug.utils import secure_filename
from flask import Flask, json, render_template, jsonify, request, make_response, send_from_directory, abort
from concurrent.futures import ThreadPoolExecutor
from Move import Move
 
app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])
executor = ThreadPoolExecutor(max_workers=5)
notebook_server_url = "http://192.168.1.250:5000/solve"
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/')
def index():
    return render_template('index.html')

 
# upload file
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        new_filename = str(uuid.uuid1()) + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        return jsonify({"success": 0, "msg": "上传成功"})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})
 
@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True)
        pass
    
    
# show photo
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

car_move = Move()
cur_key_n = -1

# car move
# 0 前进 1 后退 2 左转 3 右转 4 停止
@app.route('/move', methods=['GET'])
def move():
    key_name = request.args.get('key', '')
    key_n = request.args.get('n','')
    key_n = int(key_n)
    print(key_name)
    global cur_key_n
    cur_key_n = max(cur_key_n, key_n)
    if key_n >= cur_key_n:
        if key_name == "up":
            car_move.turn_up(run_speed=20, run_time=0.1)
        elif key_name == "back":
            car_move.turn_back(run_speed=10, run_time=0.1)
        elif key_name == "left":
            car_move.turn_left(run_speed=20, run_time=0.1)
        elif key_name == "right":
            car_move.turn_right(run_speed=20, run_time=0.1)
        elif key_name == "stop":
            car_move.turn_stop()
        else:
            return jsonify({"error": "cannot support {} operator".format(key_name)})
        # car_move.reset()
    return jsonify({"success":0})

lock = True

def car_run():
    global lock
    global car_move
    while True:
        if lock is False:
            break
        response = requests.post(notebook_server_url)
        print(response.text)
        time.sleep(1)
        #480 -> 34 mm 34/480 
        #20,1s -> 50 mm 50/1
        print("小车正在运行")
        pass
    print("小车运行完毕")
    car_move.turn_stop()

# start car
@app.route('/start', methods=['GET'])
def start():
    global lock
    global executor
    flag = request.args.get('flag', '')
    if flag == '1':
        print("正在启动")
        lock = True
        # start thread to run car
        executor.submit(car_run)
        return jsonify({"success": 0, "msg": "start success"})
    elif flag == '0':
        lock = False
        print("正在暂停")
        return jsonify({"success": 0, "msg": "stop success"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)