#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
import time
import logging

import tweepy

from daemon import Daemon
from data import voices
import config

class BittersweetDaemon(Daemon):
	def run(self):
		auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
		auth.set_access_token(config.access_key, config.access_secret)
		api = tweepy.API(auth)
		logging.basicConfig(filename=config.logfile,
			format='%(asctime)s %(levelname)s %(message)s',
			level=logging.DEBUG)

		while True:
			try:
				favs = api.favorites()
				if len(favs) > 0:
					fav = random.choice(favs)
					api.retweet(fav.id)
					api.destroy_favorite(fav.id)
				else:
					api.update_status(random.choice(voices))
				logging.info('UPDATE OK')
			except Exception, e:
				logging.warning(str(e))
				pass
				
			time.sleep(3600)

if __name__ == "__main__":
	import sys

	daemon = BittersweetDaemon(config.pidfile)

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
