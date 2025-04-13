import os
from dotenv import load_dotenv
load_dotenv()


SERVER_A_ADDRESS = os.getenv("SERVER_A_ADDRESS")
SERVER_B_ADDRESS = os.getenv("SERVER_B_ADDRESS")
SERVER_A_KEY = os.getenv("SERVER_A_KEY")
SERVER_B_KEY = os.getenv("SERVER_B_KEY")
CSV_REMOTE_PATH = "/home/stauto/network_devices.csv"
CHECK_INTERVAL = 20
USERNAME = "stauto"
SSH_SERVER_PORT = 22
