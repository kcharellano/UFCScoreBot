#!/usr/bin/python
import praw
import sys
import logging

class UFCBot:
    def __init__(self):
        logging.info("Creating reddit instance")
        self.reddit = praw.Reddit(user_agent='Bobby')
    
    def start(self):
        logging.info("Starting bot")
        while True:
            try:
                '''
                    Add things that the bot should be checking for
                '''
                pass
            except KeyboardInterrupt:
                logging.info("Exiting Bot")
                exit()



if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    mybot = UFCBot()
    mybot.start()




