import os
import sys
import time
import threading
from dotenv import load_dotenv

from draw.drawer import draw_loop
from pid import PidController
load_dotenv()

from api import *
from context import Context
from const import *
from interval_runner import IntervalRunner

from models import *
from strategy import *

logger = get_logger("MAIN")

def main():
    # Verify token
    print(f"Token is {os.getenv('TOKEN')}")

    # Create context to avoid doing many requests for a single iteration
    context = Context()

    # Create task planner and interval_runner that runs POST request every ITER_TIME seconds
    context_updater = IntervalRunner(UPDATE_TIME, context.update_on_time, args=[])
    context_updater.start()

    # Create drawer and launch
    drawing_thread = threading.Thread(target=draw_loop, args=[])
    drawing_thread.start()

    # Start mock server if required
    mock_updater = None
    if USE_MOCK:
        mock_updater = IntervalRunner(MOCK_UPDATE_TIME, context.mock_server.update_on_time, args=[])
        mock_updater.start()

    while not context.interrupt:
        try:
            ###
            # ADD ALL LOGIC HERE
            ###
            if context.carpets:

                if not context.pids:
                    context.pids = [PidController(carpet=c) for c in context.carpets]

                moves = []
                for (carpet, pid) in zip(context.carpets, context.pids):
                    pid.update_target(carpet)
                    attack = attack_strategy(carpet)

                    moves.append(CarpetMove(
                        acceleration=pid.get_acceleration_3(),
                        activateShield=shild_strategy(carpet),
                        attack=attack.as_int if attack is not None else None,
                        id=carpet.id
                    ))
                context.moves = moves
                # for carpet in context.carpets:
                    # print(f"carpet {carpet.id} pos = {carpet.pos}")
                # print()

        except KeyboardInterrupt:
            print("Shutting down...")
            context.interrupt = True

            if USE_MOCK:
                mock_updater.stop()
            drawing_thread.join()
            context_updater.stop()
            break

if __name__ == "__main__":
    main()