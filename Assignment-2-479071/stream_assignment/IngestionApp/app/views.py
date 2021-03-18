from app import app
from flask import request, jsonify
import flask
import os
import json
import logging
import importlib
import threading
import pika

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

def start_consumer(user, append):
    i = importlib.import_module(user + ".clientstreamingestapp")
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit-server'))
    channel = connection.channel()
    channel.queue_declare(queue=user)

    tag = channel.basic_consume(queue=user, on_message_callback=i.callback, auto_ack=True)
    write_mode = "w"
    if append:
        write_mode = "a"
    f = open(user + "/tags.txt", write_mode)
    f.write(tag + "\n")
    f.close()
    
    channel.start_consuming()
            

@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        user = request.form['user']
        if file.filename == "clientstreamingestapp.py":
            if not os.path.exists(str(user)):
                os.mkdir(str(user))
            if not os.path.exists("/data/" + str(user)):
                os.mkdir("/data/" + str(user))
            file.save(os.path.join(str(user), file.filename))
            file.close()

            thread = threading.Thread(target=start_consumer, args=(user,False,), daemon=True)
            thread.start()
            
            resp = jsonify({'message' : 'Successfully started RabbitMQ queue'})
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

@app.route('/stop', methods=['POST', 'GET'])
def stop():
    if request.method == 'POST':
        user = request.form['user']
        connection = pika.BlockingConnection(pika.ConnectionParameters(
	       'rabbit-server'))
        channel = connection.channel()
        f = open(user + "/tags.txt", "r")
        lines = f.readlines()
        for tag in lines:
            channel.basic_cancel(tag)
        channel.queue_delete(queue=user)

        connection.close()
        
        resp = jsonify({'message' : 'Successfully started RabbitMQ queue'})
        resp.status_code = 200
        return resp
        
    else:
        resp = jsonify({'message' : 'Not a POST request'})
        resp.status_code = 400
        return resp  
    
@app.route('/log', methods=['POST', 'GET'])
def log():
    if request.method == 'POST':
        user = request.form['user']
        avg_ingesttime = request.form['avg_ingesttime']
        tot_size = request.form['tot_size']
        messages = int(request.form['messages'])
        
        logger = setup_logger('general_logger', '/data/general.log')
        user_loggers = setup_logger(user + '_logger', "/data/" + user + "/" + user + '.log')
        logger.info("avg_ingesttime: " + str(avg_ingesttime) + " total_data_size: " + str(tot_size) + " num_messages: " + str(messages))
        user_loggers.info("avg_ingesttime: " + str(avg_ingesttime) + " total_data_size: " + str(tot_size) + " num_messages: " + str(messages))
        
        if messages > 400:
            thread = threading.Thread(target=start_consumer, args=(user,True,), daemon=True)
            thread.start()
        if messages < 40:
            f = open(user + "/tags.txt", "r")
            lines = f.readlines()
            f.close()
            if len(lines) >= 2:
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-server'))
                channel = connection.channel()
                channel.basic_cancel(lines[-2])
                connection.close()
                f = open(user + "/tags.txt", "w")
                for tag in lines[:-2]:
                    f.write(tag + "\n")
                f.close()
        if messages > app.config["MAX_NUMBER_OF_MESSAGES"] or tot_size > app.config["MAX_SIZE"]: 
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-server'))
            channel = connection.channel()
            f = open(user + "/tags.txt", "r")
            lines = f.readlines()
            for tag in lines:
                channel.basic_cancel(tag)
            channel.queue_delete(queue=user)

            connection.close()

        resp = jsonify({'message' : 'Successfully logged'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message' : 'Not a POST request'})
        resp.status_code = 400
        return resp  
    

@app.route('/log_error', methods=['POST', 'GET'])
def error_log():
    if request.method == 'POST':
        user = request.form['user']
        error = request.form['error']
        logger = setup_logger('general_logger', '/data/general.log')
        user_loggers = setup_logger(user + '_logger', "/data/" + user + "/" + user + '.log')
        logger.error(error)
        user_loggers.error(error)   
        resp = jsonify({'message' : 'Successfully logged'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message' : 'Not a POST request'})
        resp.status_code = 400
        return resp  
     




















