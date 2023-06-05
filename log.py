#generic/built-in
import sys
import logging

def logger_configuration():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s')
    #datefmt='%Y-%m-%d %H:%M:%S' #logging.Formatter('%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)

    #exporting formatted output to the console
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)

    #exporting logs to file
    fhandler = logging.FileHandler(filename='log.log', mode='w') #Mode: 'a' for appending / 'w' for writing a new file
    fhandler.setFormatter(formatter)
    fhandler.setLevel(logging.INFO)
    logger.addHandler(fhandler)