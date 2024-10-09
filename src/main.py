import os
import time
from dotenv import load_dotenv
load_dotenv()

from api import *
from context import Context
from const import ITER_TIME
from interval_runner import IntervalRunner

from models import *

def main():
    # Verify token and register for a round
    print(f"Token is {os.getenv('TOKEN')}")
    msg, participating = participate()
    print(msg)

    while not participating:
        msg, participating = participate()
        print(msg)
        time.sleep(5)
        # print("Exiting")
        # return None
    
    # Create context to avoid doing many requests for a single iteration
    context = Context()

    # Create task planner and interval_runner that runs POST request every ITER_TIME seconds
    get_runner = IntervalRunner(ITER_TIME, collect_info, args=[context])
    get_runner.start()

    while True:
        try:  
            ###
            # ADD ALL LOGIC HERE
            ###
            pass

        except KeyboardInterrupt:
            print("Shutting down...")
            get_runner.stop()
            break

if __name__ == "__main__":
    main()
