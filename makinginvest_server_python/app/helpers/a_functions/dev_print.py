import os
from dotenv import load_dotenv

load_dotenv()
is_production = os.getenv("PRODUCTION")


def dev_print(*args):
    if is_production != "True":
        print(*args)
