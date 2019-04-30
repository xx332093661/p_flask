from taobao_test import app

import traceback
import os
import logging

log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'log.txt'))

handler = logging.FileHandler(log_path, encoding='UTF-8')
handler.setLevel(logging.INFO)
logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

try:
    app.run(host='0.0.0.0', port=5001)
except Exception as e:
    app.logger.error(traceback.format_exc())