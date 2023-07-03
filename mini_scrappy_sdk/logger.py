import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s: %(message)s')
# stream
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# file
# file_handler = logging.FileHandler("spider.log")
# file_handler .setFormatter(formatter)
# logger.addHandler(file_handler)
