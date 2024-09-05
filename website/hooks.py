import subprocess
from datetime import datetime


def get_revision():
    return datetime.today().strftime("%Y.%m.%d-") + subprocess.check_output(
        ["git", "describe", "--always", "--dirty=-dev"], text=True
    )


def on_config(config):
    config["revision"] = get_revision()
    return config

