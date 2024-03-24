import os
from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION", "False")


def dev_print(*args):
    if is_production != "True":
        print(*args)
