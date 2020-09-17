#!/usr/bin/python
import praw
import sys
import logging
import os
import json

from time import sleep

TOP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCORES_DIR = os.path.join(TOP_DIR, "scores")
SPIDER_FILE = os.path.join(TOP_DIR, "scores", "scores", "spiders", "charlotte.py")
OUTPUT_DIR = os.path.join(SCORES_DIR, "scrapy_output")

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
                        logging.info("Running scraper for: {}".format(mention.body))
                        self.runScraper(args)
                        logging.info("Preparing for reply")
                        reply_body = self.getStats(args)
                        logging.info("Replying to commment...")
                        mention.reply(reply_body)
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
        args_dict = {"first": args_list[1].lower(), "last": args_list[2].lower()}
        return args_dict
    
    def runScraper(self, args):
        runCommand = "scrapy crawl -a last={last_name} -a first={first_name} charlotte"
        if not os.getcwd() == SCORES_DIR:
            os.chdir("scores")
        os.system(runCommand.format(last_name=args["last"], first_name=args["first"]))

    def getStats(self, args):
        logging.info("Retreiving scraped data")
        target_file = os.path.join(OUTPUT_DIR, "{last}_{first}.json".format(last=args['last'], first=args['first']))
        with open(target_file, 'r+') as target:
            data = json.load(target)
        return data[0]['record']

if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    mybot = UFCBot()
    mybot.start()




