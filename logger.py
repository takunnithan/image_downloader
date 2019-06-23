import logging

from time import strftime


datestr = strftime('%d-%m-%Y-%T')
logfile = 'image_downloader_{}.log'.format(strftime('%d_%m_%Y_%T'))
logformat = '%(asctime)s %(levelname)s %(message)s'


handler = logging.FileHandler(logfile, mode='w')

formatter = logging.Formatter(fmt=logformat, datefmt=datestr)
handler.setFormatter(formatter)

logger = logging.getLogger('image_downloader')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
