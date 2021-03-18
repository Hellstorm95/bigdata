from app import app
from flask import request, jsonify
import flask
import os
import json
import logging
import importlib
from redis import Redis
from rq import Queue

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)

        logger.setLevel(level)
    
        logger.addHandler(handler)

    return logger

# first file logger
logger = setup_logger('general_logger', '/data/general.log')
app.config.from_object("config.NormalConfig")

@app.route('/load_script', methods=['POST', 'GET'])
def upload_script_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        user = request.form['user']
        if file.filename == "clientbatchingestapp.py":
            if not os.path.exists("/data/" + str(user)):
                os.mkdir("/data/" + str(user))
            user_loggers = setup_logger(user + '_logger', "/data/" + user + "/" + user + '.log')
            file.save(os.path.join("/data/" + str(user), file.filename))
            file.close()
            resp = jsonify({'message' : 'Successfully uploaded script'})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message' : 'File name not allowed'})
            resp.status_code = 400
            return resp
    else:
        resp = jsonify({'message' : 'Not a POST request'})
        resp.status_code = 400
        return resp



@app.route('/ingest_files', methods=['POST'])
def ingest_files():
    if request.method == 'POST':
        files = request.files
        user = request.form['user'] 
        if not os.path.exists("/data/"  + str(user)):
            resp = jsonify({'message' : 'User does not exist on the platform, upload batch ingestion first'})
            resp.status_code = 400
            return resp
        files = list(files.values())
        if isinstance(files, list) : 
            if len(files) > 0 and len(files) < app.config["MAX_NUMBER_OF_FILES"]:
                filenames = []
                file_sizes = []
                for file in files:
                    file.seek(0, os.SEEK_END)
                    file_size = file.tell()
                    file_sizes.append(file_size)
                    print(file_size)
                    print(app.config["MAX_FILE_SIZE"])
                    if file_size > app.config["MAX_FILE_SIZE"]: 
                        resp = jsonify({'message' : 'file ' + file.filename + ' exceeded the maximum allowed file size'})
                        resp.status_code = 400
                        return resp
                for file in files:
                    file.seek(0, 0)
                    filenames.append(file.filename)
                    file.save(os.path.join("/data/" + str(user), file.filename))
                    file.close()
                i = importlib.import_module("run_app")
                
                q = Queue('queue', connection=Redis(host='rq-server', port=6379))
                for idx, filename in enumerate(filenames):
                    q.enqueue(i.run_ingest, args=(user, filename, file_sizes[idx]))
                
                resp = jsonify({'message' : 'Successfully started ingestion'})
                resp.status_code = 200
                return resp
            else:
                resp = jsonify({'message' : 'Empty list of files or too many files uploaded'})
                resp.status_code = 400
                return resp
        else:
            resp = jsonify({'message' : 'The files uploaded are not in a list'})
            resp.status_code = 400
            return resp
    else:
        resp = jsonify({'message' : 'Not a POST request'})
        resp.status_code = 400
        return resp
