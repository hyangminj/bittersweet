#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import logging

import tweepy
from pymongo import MongoClient

from daemon import Daemon

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
LOGFILE = ''
PIDFILE = ''

class CustomStreamListener(tweepy.StreamListener):
	def __init__(self):
		logging.basicConfig(filename=LOGFILE,
			format='%(asctime)s %(levelname)s %(message)s',
			level=logging.DEBUG)
		self.tweets = MongoClient().test.tweets
		super(CustomStreamListener, self).__init__()

	def on_data(self, data):
		try:
			self.tweets.insert(json.loads(data))
			logging.info('UPDATE OK')
		except Exception, e:
			logging.error(str(e))

class CrawlerDaemon(Daemon):
	def run(self):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

		streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)
		streaming_api.userstream()

if __name__ == '__main__':
	import sys

	daemon = CrawlerDaemon(PIDFILE)

	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
