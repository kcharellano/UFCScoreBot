import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
BOT_FILE = os.path.join(BASE_DIR, "redditBot", "bot.py")
command = "python %s" % BOT_FILE
os.system(command)
