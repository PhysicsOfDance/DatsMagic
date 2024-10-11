import os
import time
import threading
from dotenv import load_dotenv

from draw.main import drawing_routine
load_dotenv()

from api import *
from context import Context
from const import *
from interval_runner import IntervalRunner

from models import *

logger = get_logger("MAIN")

def main():
    # Verify token
    print(f"Token is {os.getenv('TOKEN')}")

    # Create context to avoid doing many requests for a single iteration
    context = Context()

    # Create task planner and interval_runner that runs POST request every ITER_TIME seconds
    context_updater = IntervalRunner(UPDATE_TIME, context.update_on_time, args=[])
    context_updater.start()

    drawing_thread = threading.Thread(target=drawing_routine, args=[context])
    drawing_thread.start()
    while True:
        try:
            ###
            # ADD ALL LOGIC HERE
            ###
            if context.carpets:
                context.moves = [CarpetMove(
                    acceleration = Vec2(x=1, y=1) - carpet.anomalyAcceleration,
                    id = carpet.id,
                ) for carpet in context.carpets]

                for carpet in context.carpets:
                    print(f"carpet {carpet.id} pos = {carpet.pos}")
                print()
                time.sleep(5)

        except KeyboardInterrupt:
            print("Shutting down...")
            context_updater.stop()
            context.interrupt = True
            drawing_thread.join()
            break

if __name__ == "__main__":
    main()
