import sys

if __package__ is None:
    # this is needed so the script works when it's executed like this `python src/main.py`
    # it is not needed when you use `python -m src.main`
    import os

    DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, DIR)

from app import create_app
from user_cud_consumer import UserCUDEventsConsumer


if __name__ == "__main__":
    app = create_app()

    user_cud_consumer = UserCUDEventsConsumer(app)
    user_cud_consumer.start()

    app.run(host="0.0.0.0", port=5051, threaded=True, use_reloader=True)
