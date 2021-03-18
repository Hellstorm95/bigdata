import time
import importlib
import logging
import os
    
def run_ingest(user, filename, file_size):
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
        
    print(os.listdir())
    print(os.getcwd())
    i = importlib.import_module("data." + user + ".clientbatchingestapp")
    logger = setup_logger('general_logger', './data/general.log')
    user_loggers = setup_logger(user + '_logger', "./data/" + user + "/" + user + '.log')
    start = time.time()
    error = i.ingest_file("./data/" + user + "/" + filename)
    end = time.time()
    if error:
        logger.error(error)
        user_loggers.error(error)   
    else:
        logger.info("Successful ingestion!" + " Response time: " + str(end - start) + " File size: " + str(file_size))
        user_loggers.info("Successful ingestion!" + " Response time: " + str(end - start) + " File size: " + str(file_size))
