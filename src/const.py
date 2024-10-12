from datetime import datetime

LOGS_FOLDER = "logs/"
SESSION_START = "{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())
UPDATE_TIME = 0.335

USE_MOCK = False
MOCK_UPDATE_TIME = 0.5
MOCK_START_STILL = True
MOCK_IGNORE_ANOMALIES = True
