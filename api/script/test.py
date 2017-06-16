import sys
import os
sys.path.append(os.path.abspath('./'))
from common import logger
import logging

Log = logging.getLogger('error')
Log.error('test')