import os

TYM_DEV = os.getenv("TYM_DEV") == "True"
APP_NAME = "tym"
CONFIG_FILENAME = "tymconfig.ini"
FIREBASE_API_KEY = "AIzaSyCwj0rlNTlywcTcs6xEzfuMpd5eRjY04JM"
RENEW_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"
PROD_BACKEND_HOSTNAME = "https://tym-project-21.uc.r.appspot.com"
DEV_BACKEND_HOSTNAME = "http://localhost:8000"
REFS_HEAD_PREFIX = "refs/heads/"
SHADOW_BRANCH_PREFIX = "rt-backup"
SHADOW_COMMIT_MESSAGE_PREFIX = "WIP"
SHADOW_BRANCH_INITIAL_COMMIT_MESSAGE = SHADOW_COMMIT_MESSAGE_PREFIX + " initial commit"
BACKEND_HOSTNAME = DEV_BACKEND_HOSTNAME if TYM_DEV else PROD_BACKEND_HOSTNAME
MAX_TCP_PORT_NUM = 65535
MIN_TCP_PORT_NUM = 10000
LAUNCH_HOSTNAME = "https://tym.so/#"
ACCEPTED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5000",
    "https://tym.codes",
    "https://www.tym.codes",
    "https://tym.so",
    "https://www.tym.so",
]
