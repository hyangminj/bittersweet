#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
import datetime, time
import logging

import tweepy

from daemon import Daemon
from data import voices
import config

lalasweet_screen_name = ['Park_ByuL','missboongboong']

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
				# Update friends at 4 am
				if datetime.datetime.now().hour == 4:
					for friend in tweepy.Cursor(api.friends).items():
						target, source = api.show_friendship(target_id=friend.id)
						if not friend.screen_name in lalasweet_screen_name and not target.followed_by:
							friend.unfollow()
							logging.info('UNFOLLOW %s' % friend.screen_name)
						time.sleep(10)
					for follower in tweepy.Cursor(api.followers).items():
						target, source = api.show_friendship(target_id=follower.id)
						if not target.following and not follower.protected:
							follower.follow()
							logging.info('FOLLOW %s' % follower.screen_name)
						time.sleep(10)
					logging.info('FOLLOWING OK')

			 	# Retweet a favorited tweet
				favs = api.favorites()
				if len(favs) > 0 and random.random() < 0.7:
					fav = random.choice(favs)
					try:
						api.retweet(fav.id)
					except Exception, e:
						logging.warning(str(e))
					api.destroy_favorite(fav.id)
					continue

				# Tweet!
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
