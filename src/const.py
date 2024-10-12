from datetime import datetime

LOGS_FOLDER = "logs/"
SESSION_START = "{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())
UPDATE_TIME = 0.335

COLLECTED_BOUNTY_DIST = 4

USE_MOCK = False
MOCK_UPDATE_TIME = 0.1
MOCK_START_STILL = True
MOCK_IGNORE_ANOMALIES = True

P_COEF = 1
I_COEF = 0.1
D_COEF = 0.1

SERVER_UPDATE_TIME = 0.1
AVERAGE_SPEED_COEF = 0.25 # comparing to maxSpeed