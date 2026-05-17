import json
from datetime import datetime


def save_json(filename, data):

    with open(filename, "w") as f:

        json.dump(data, f, indent=4)



def timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )