#!/usr/bin/python
import praw
import sys
import logging

from time import sleep

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
                    print(mention.body)
                logging.info("Sleeping for 5 seconds")
                sleep(5)
            except KeyboardInterrupt:
                logging.info("Exiting Bot")
                exit()

    def parse(self, comment):
        pass
    
    def runScraper(self):
        pass


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    mybot = UFCBot()
    mybot.start()




