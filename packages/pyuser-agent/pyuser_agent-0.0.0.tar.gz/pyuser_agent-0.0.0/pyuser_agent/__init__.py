#!/usr/bin/python3

import json,os,logging
from .utility import *
import random

class UA():
    def __init__(self):
        self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.source_json = os.path.join(self.location,STORE_DUMP_JSON)
        if not os.path.isfile(self.source_json):
            logging.error("requriment file missing")
        self.list_browsers,self.jsonObj = self.getListItems()

    def __getattr__(self, __name:str):
        try:
            if __name == LIST:
                return self.list_browsers
            if __name == RANDOM:
                return self.getUA()
            if __name == CHROME:
                return self.getUA(broswer=CHROME)
            elif __name == CHROME_PLUS:
                return self.getUA(broswer=CHROME_PLUS)
            elif __name == EDGE:
                return self.getUA(broswer=EDGE)
            elif __name == FIREFOX:
                return self.getUA(broswer=FIREFOX)
            elif __name == INTERNET_EXPLORER:
                return self.getUA(broswer=INTERNET_EXPLORER)
            elif __name == MOZILLA:
                return self.getUA(broswer=MOZILLA)
            elif __name == OPERA:
                return self.getUA(broswer=OPERA)
            elif __name == SAFARI:
                return self.getUA(broswer=SAFARI)
            else:
                logging.warning(f"not match \"{__name}\". return random user agent.")
                return self.getUA()
        except Exception as e:
            logging.error(e)

    def getUA(self,platform=None,broswer=None):
        try:
            tmpUA = None
            state_ = True
            while state_:
                try:
                    if platform == None and broswer == None:
                        tmpUA = random.choice(self.jsonObj[self.random_broswer()][self.random_plaform()])
                    elif platform == None and broswer != None:
                        tmpUA = random.choice(self.jsonObj[broswer][self.random_plaform()])
                    else:
                        tmpUA = random.choice(self.jsonObj[broswer][platform])
                    if tmpUA != None:
                        state_ = False
                except Exception as e:
                    state_ = True
            return tmpUA
        except Exception as e:
            logging.error(e)

    def getListItems(self):
        try:
            with open(self.source_json,"r") as jfs:
                load_data = json.load(jfs)
            jfs.close()
            broswer = []
            for item in load_data:
                broswer.append(item)
            return broswer,load_data
        except Exception as e:
            logging.error(e)
            return None,None
    
    def random_plaform(self):
        try:
            return (
                random.choice(PLATFORM_LIST)
            )
        except Exception as e:
            logging.error(e)
    
    def random_broswer(self):
        try:
            return (
                random.choice(BROWSER_LIST)
            )
        except Exception as e:
            logging.error(e)