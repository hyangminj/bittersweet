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

		step = 0
		while True:
			try:
				if step % 24 == 0:
					for friend in tweepy.Cursor(api.friends).items():
						if not api.show_friendship(target_id=friend.id)[0].followed_by:
							friend.unfollow()
					for follower in tweepy.Cursor(api.followers).items():
						if not api.show_friendship(target_id=friend.id)[0].following:
							follower.follow()
					logging.info('FOLLOWING OK')
			except Exception, e:
				logging.warning(str(e))
				pass

			try:
				favs = api.favorites()
				if len(favs) > 0 and random.random() > 0.3:
					fav = random.choice(favs)
					api.retweet(fav.id)
					api.destroy_favorite(fav.id)
				else:
					api.update_status(random.choice(voices))
				logging.info('UPDATE OK')
			except Exception, e:
				logging.warning(str(e))
				pass
				
			step = step + 1
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
