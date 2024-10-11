from datetime import datetime

LOGS_FOLDER = "logs/"
SESSION_START = "{:%Y_%m_%d_%H_%M_%S}".format(datetime.now())
UPDATE_TIME = 0.335

DIM_SIDE_SIZE = 500
MAX_SPEED_ARROW_LENGTH = 50
MAX_ACCELERATION_ARROW_LENGTH = 50
MIN_DRAW_LENGTH = 10
