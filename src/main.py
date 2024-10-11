import os
import time
from dotenv import load_dotenv
load_dotenv()

from api import *
from context import Context
from const import *
from interval_runner import IntervalRunner

from models import *

logger = get_logger("MAIN")

def main():
    # Verify token and register for a round
    print(f"Token is {os.getenv('TOKEN')}")
    # msg, participating = participate()
    # print(msg)

    # while not participating:
    #     msg, participating = participate()
    #     print(msg)
    #     time.sleep(5)
    #     # print("Exiting")
    #     # return None
    
    # Create context to avoid doing many requests for a single iteration
    context = Context()

    # Create task planner and interval_runner that runs POST request every ITER_TIME seconds
    context_updater = IntervalRunner(UPDATE_TIME, context.update_on_time, args=[])
    context_updater.start()

    while True:
        try:
            ###
            # ADD ALL LOGIC HERE
            ###
            pass

        except KeyboardInterrupt:
            print("Shutting down...")
            context_updater.stop()
            break

if __name__ == "__main__":
    main()
