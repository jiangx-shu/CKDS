import logging
import os
import src.constants.constants as constants


def get_logger(logger_name, log_file,formatter, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(formatter)
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(fileHandler)
    return logging.getLogger(logger_name)


def logger(logger_name):
    return logger_dict[logger_name]


logger_dict = {}
process_formatter='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
process_logger = get_logger('PROCESS', os.path.join(constants.base_path, 'process.log'),process_formatter)
logger_dict['PROCESS'] = process_logger

kds_logger = get_logger('KDS_MINUS', os.path.join(constants.base_path,'kds_minus.log'),process_formatter)
logger_dict['KDS_MINUS'] = kds_logger

result_formatter = '%(message)s'
result_logger = get_logger('RESULT', os.path.join(constants.base_path,'result.log'), result_formatter)
logger_dict['RESULT'] = result_logger
