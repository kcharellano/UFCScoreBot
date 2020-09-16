#!/usr/bin/python
import praw
import sys
import logging
import os

from time import sleep

TOP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCORES_DIR = os.path.join(TOP_DIR, "scores")
SPIDER_FILE = os.path.join(TOP_DIR, "scores", "scores", "spiders", "charlotte.py")

class UFCBot:
    def __init__(self):
        logging.info("Creating reddit instance")
        self.reddit = praw.Reddit(user_agent='Bobby')
    
    def start(self):
        logging.info("Starting bot")
        logging.info("Press \'Ctrl + C\' to exit")
        while True:
            try:
                for mention in self.reddit.inbox.mentions():
                    args = self.parse(mention.body)
                    if args != None:
                        self.runScraper(args)
                logging.info("Checking for mentions again in 10 seconds...")
                sleep(10)
            except KeyboardInterrupt:
                logging.info("Exiting Bot")
                exit()

    def parse(self, comment):
        args_list = comment.split(" ")
        if len(args_list) != 3:
            logging.warning("Haven't implemented parsing for more/less than 3 words -- bot will not run spider")
            return None
        args_dict = {"first": args_list[1], "last": args_list[2]}
        return args_dict
    
    def runScraper(self, args):
        runCommand = "scrapy crawl -a last={last_name} -a first={first_name} charlotte -o scrapy_output.json"
        if not os.getcwd() == SCORES_DIR:
            os.chdir("scores")
        os.system(runCommand.format(last_name=args["last"], first_name=args["first"]))


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    mybot = UFCBot()
    mybot.start()




